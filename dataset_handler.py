#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import io
import json
import os
from abc import ABCMeta, abstractproperty, abstractmethod
from copy import deepcopy
from future.utils import iteritems, itervalues
from pathlib import Path

class Dataset(object):
    __metaclass__ = ABCMeta
    """
        Abstract data set class to inherit from when implementing a new
        data set handler
    """

    @classmethod
    @abstractmethod
    def from_dir(cls, _dir):
        """
            Instantiates a dataset from a folder
        """
        raise NotImplementedError

    @abstractproperty
    def training_dataset(self):
        raise NotImplementedError

    @abstractproperty
    def test_dataset(self):
        raise NotImplementedError

    @abstractmethod
    def get_audio_file(self, text):
        raise NotImplementedError


class TrainTestDataset(Dataset):
    """Interface for train/test metrics
    """

    def __init__(self, data_list, training_dataset, test_dataset):
        self.data = data_list
        self._training_dataset = training_dataset
        self._test_dataset = test_dataset
        self._normalized_training_dataset = None
        self._normalized_test_dataset = None
        self.language = self._training_dataset["language"]

        # text -> wav mapping
        self.audio_corpus = {}
        for entry in self.data:
            text = entry['text']
            wav_file = entry['path_file']
            self.audio_corpus[text] = wav_file

        # clean up the dataset by removing utterances that don't have an audio
        self._test_dataset = keep_only_utterances_with_audio(
            self._test_dataset, self.audio_corpus
        )

        # wav -> text mapping
        self.wav_to_text = {
            Path(wav).name: text for text, wav in self.audio_corpus.items()
        }

        # labels
        self.utterances_labels = retrieve_utterances_labels(self._test_dataset)

    @classmethod
    def from_dir(cls, _dir):
        metadata_path = os.path.join(_dir, "metadata.json")
        json_data = load_json(metadata_path)

        training_dataset_path = os.path.join(_dir, "training_dataset.json")
        training_dataset = load_json(training_dataset_path)

        test_dataset_path = os.path.join(_dir, "test_dataset.json")
        test_dataset = load_json(test_dataset_path)

        for entry in json_data:
            entry["path_file"] = os.path.join(_dir, entry["path_file"])

        return cls(json_data, training_dataset, test_dataset)

    def get_audio_file(self, text):
        wav = self.audio_corpus.get(text)
        if wav is None:
            raise KeyError("Text {} is absent from audio dataset".format(text))
        return wav

    def get_labels_from_text(self, text):
        labels = self.utterances_labels.get(text)
        if labels is None:
            raise KeyError("Text {} is absent from audio dataset".format(text))
        return labels

    def get_labels_from_wav(self, wav):
        text = self.wav_to_text.get(wav)
        if text is None:
            raise KeyError("File {} does not exist".format(wav))
        return self.utterances_labels.get(text)

    def get_transcript(self, wav):
        text = self.wav_to_text.get(wav)
        if text is None:
            raise KeyError("File {} does not exist".format(wav))
        return text

    @property
    def training_dataset(self):
        return self._training_dataset

    @property
    def test_dataset(self):
        return self._test_dataset


class CrossValDataset(Dataset):
    """Interface for cross validation metrics
    """

    def __init__(self, config, dataset, audio_corpus):
        self.config = config

        # text -> wav mapping
        self.audio_corpus = {}
        for sentence, wav_file in iteritems(audio_corpus):
            self.audio_corpus[sentence] = wav_file

        # clean up the data set by removing utterances that don't have an audio
        self._dataset = keep_only_utterances_with_audio(
            dataset, self.audio_corpus
        )

        # wav -> text mapping
        self.wav_to_text = {
            Path(wav).name: text for text, wav in self.audio_corpus.items()
        }

        # labels
        self.utterances_labels = retrieve_utterances_labels(self._dataset)

    @classmethod
    def from_dir(cls, _dir):
        config = load_json(os.path.join(_dir, "config.json"))
        dataset = load_json(os.path.join(_dir, config['dataset']))
        speech_corpus_dir = os.path.join(_dir, config['speech_corpus'])
        metadata = load_json(os.path.join(speech_corpus_dir, "metadata.json"))

        audio_corpus = {
            item['text']: os.path.abspath(
                os.path.join(speech_corpus_dir, 'audio', item['filename'])) for
            item in itervalues(metadata)
        }
        return cls(config, dataset, audio_corpus)

    def get_audio_file(self, text):
        wav = self.audio_corpus.get(text)
        if wav is None:
            raise KeyError("Text {} is absent from audio dataset".format(text))
        return wav

    def get_transcript(self, wav):
        text = self.wav_to_text.get(wav)
        if text is None:
            raise KeyError("File {} does not exist".format(wav))
        return text

    def get_labels_from_text(self, text):
        labels = self.utterances_labels.get(text)
        if labels is None:
            raise KeyError("Text {} is absent from audio dataset".format(text))
        return labels

    def get_labels_from_wav(self, wav):
        text = self.wav_to_text.get(wav)
        if text is None:
            raise KeyError("File {} does not exist".format(wav))
        return self.utterances_labels.get(text)

    @property
    def training_dataset(self):
        return self._dataset

    @property
    def test_dataset(self):
        raise TypeError(
            "CrossValDataset is not meant to be used with train test metrics"
        )


def load_json(filename, encoding='utf-8'):
    """
        Load the content of filename
    """
    with io.open(filename, 'r', encoding=encoding) as _file:
        return json.load(_file)


def retrieve_utterances_labels(dataset):
    utterances_labels = {}
    for intent, intent_data in iteritems(dataset['intents']):
        for idx, utt in enumerate(intent_data['utterances']):
            sentence = "".join(chunk['text'] for chunk in utt['data'])
            slots = [chunk for chunk in utt['data'] if 'entity' in chunk]
            utterances_labels[sentence] = {
                "text": sentence,
                "intent": intent,
                "slots": slots
            }
    return utterances_labels


def keep_only_utterances_with_audio(dataset, audio_corpus):
    cleaned_up_dataset = deepcopy(dataset)
    n_skipped = 0
    total = 0
    for intent, intent_data in iteritems(dataset['intents']):
        cleaned_up_dataset['intents'][intent]['utterances'] = []
        for idx, utt in enumerate(intent_data['utterances']):
            total += 1
            sentence = "".join(chunk['text'] for chunk in utt['data'])
            if sentence in audio_corpus:
                cleaned_up_dataset['intents'][intent]['utterances'].append(utt)
            else:
                n_skipped += 1
                print(
                    "Skipping sentence {} from dataset because it does not "
                    "have an audio file".format(sentence)
                )
    print(
        "{} utterancces skipped out of {}".format(n_skipped, total)
    )

    return cleaned_up_dataset
