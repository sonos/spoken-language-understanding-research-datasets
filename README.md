# spoken-language-understanding-research-datasets

## Overview

This repository contains the license and instructions relative to the open
Data Sets mentioned in this publication:

```
LINK TO PAPER
```

These Data Sets are made publicly available in the interest of
reproducibility and in the hope that they can prove useful to the SLU community.

More specifically, they contain up to a few thousand text queries with their
supervision, i.e. intent and slots, collected using an in-house data
generation pipeline. Recordings of these sentences are then crowdsourced and
 one spoken utterance is collected for each text query in the dataset.
Far-field datasets are created by playing these utterances with a neutral
speaker and recording them using a microphone array positioned at a distance
of 2 meters.

WARNING: For various reasons, some text queries might not have recordings.
Handlers are provided in `dataset.py` to deal with this special case.

The Data Sets cover two domains of increasing complexity:

- a `SmartLights` assistant meant to be used in *cross validation*,
comprising 6
intents allowing to turn on or off the light, or change its brightness or
color, with a vocabulary size of approximately 400 words:
    * `DecreaseBrightness` (296 queries, slots: `room`),
    * `IncreaseBrightness` (296 queries, slots: `room`),
    * `SetLightBrightness` (296 queries, slots: `room`, `brightness`),
    * `SetLightColor` (300 queries, slots: `room`, `color`),
    * `SwitchLightOff` (299 queries, slots: `room`),
    * `SwitchLightOn` (278 queries, slots: `room`)

- two `SmartSpeaker` assistants in English and French meant to be used in
 *train/test*. The training set comprises 9
intents (8 in French) allowing to control a smart speaker through playback
 control (volume control, track navigation, etc), but also play music from
 large libraries of artists, tracks and albums. The assistants have a
 vocabulary size of more than 65k words in English and 70k words in French.
 The English ontology is the following:
    * `NextSong` (200 queries, no slot),
    * `PreviousSong` (199 queries, no slot),
    * `SpeakerInterrupt` (172 queries, no slot),
    * `ResumeMusic` (200 queries, no slot),
    * `VolumeDown` (215 queries, slots: `volume_level_absolute`),
    * `VolumeUp` (260 queries, slots: `volume_level_absolute`),
    * `VolumeSet` (100 queries, slots: `volume_level_absolute`, `volume_level_percent`),
    * `GetInfos` (199 queries, slots: `music_item`),
    * `PlayMusic` (1508 queries, slots: `song_name`, `artist_name`,
    `album_name`, `playlist_mode`, `playlist_name`)

  The French ontology slightly differs for the volume control intents:
    * `NextSong` (126 queries, no slot),
    * `PreviousSong` (62 queries, no slot),
    * `SpeakerInterrupt` (421 queries, no slot),
    * `ResumeMusic` (107 queries, no slot),
    * `VolumeShift` (437 queries, slots: `volume_action`)
    * `VolumeSet` (229 queries, slots: `volume_level_absolute`,
    `volume_level_percent`, `volume_level_relative`),
    * `GetInfos` (62 queries, no slot),
    * `PlayMusic` (548 queries in train, 1500 queries in test, slots:
    `song_name`, `artist_name`, `album_name`, `playlist_mode`, `playlist_name`)

  The English and French test sets consist in 1,500 queries of the form ``play
    some music by #ARTIST'', where we sample `#ARTIST` from a publicly available
     list of the most streamed artists on Spotify, updated based on daily and
     weekly statistics (from https://kworb.net/spotify/artists.html, visited on 9/10/18). The list, divided in 3 tiers of
     popularity, will be available with the Data Sets.

## License summary

Use only for academic and/or research purposes. No commercial use.
Publication permitted only if the Data Sets are unmodified and subject to the same license terms.
Any publication must include a full citation to the paper in which the Data Sets were initially published by Snips.

Please read the full License Terms before accessing the Data Sets.

## Data Set access

To access the data, please write an email mentioning your affiliation to

```
research-datasets@snips.ai
```

You will be granted access shortly.
