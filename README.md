# AmenBrake
[![GitHub](https://img.shields.io/github/license/RadicalRingtail/css-reset)](https://github.com/RadicalRingtail/converter-tool/blob/main/LICENSE.md)

A simple audio transcoder and metadata editor.

----------------

## Motivation

With Bandcamp's future seeming uncertain at the moment, i wanted to upload my music somewhere else as a backup alternative so that even if Bandcamp suddenly disappears, people can still download my music. I decided on using itch.io as my alternative of choice since it was very customizable, however, specifically for music, there was one big draw back. A slightly underrated feature of Bandcamp is the ability to download a purchased item in a selection of different formats (flac, mp3, wav, etc.), which is super convenient. itch.io does not have that feature, what you upload is what will be downloaded.

This of course was going to be an issue, since all my masters are wav files, which dont allow for metadata or cover art and are quite large, so i would have to transcode and add metadata to a *lot* of files, something that would be tedious to do with a program like audacity. so thats why i created this program, to make the process of transcoding and adding metadata to batches of audio files much more simple and streamlined, similar to something like HandBrake (hence the name!)

----------------

## Requirements 
- ``python@3.12``
- ``python-tk@3.12``
- ``ffmpeg``

To install dependencies, run ``pip install -r requirements.txt``

----------------