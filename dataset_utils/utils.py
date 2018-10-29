#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import io
import json
from copy import deepcopy

import logging

logger = logging.getLogger(__name__)


def load_json(filename, encoding='utf-8'):
    """
        Load the content of filename
    """
    with io.open(filename, 'r', encoding=encoding) as _file:
        return json.load(_file)


def keep_only_utterances_with_audio(dataset, audio_corpus):
    cleaned_up_dataset = deepcopy(dataset)
    n_skipped = 0
    total = 0
    for intent, intent_data in dataset['intents'].iteritems():
        cleaned_up_dataset['intents'][intent]['utterances'] = []
        for idx, utt in enumerate(intent_data['utterances']):
            total += 1
            sentence = "".join(chunk['text'] for chunk in utt['data'])
            if sentence in audio_corpus:
                cleaned_up_dataset['intents'][intent]['utterances'].append(utt)
            else:
                n_skipped += 1
                logger.warning(
                    "Skipping sentence {} from dataset because it does not "
                    "have an audio file".format(sentence)
                )
    logger.warning(
        "{} utterancces skipped out of {}".format(n_skipped, total)
    )

    return cleaned_up_dataset
