from enum import Enum

class Codecs(Enum):
    WAV = 'wav'
    MP3 = 'mp3'
    FLAC = 'flac'
    AIFF = 'aiff'
    OGG = 'ogg'

class Bitrates(Enum):
    B_24 = 24
    B_32 = 32
    B_40 = 40
    B_48 = 48
    B_56 = 56
    B_64 = 64
    B_80 = 80
    B_96 = 96
    B_112 = 112
    B_128 = 128
    B_160 = 160
    B_192 = 192
    B_224 = 224
    B_256 = 256
    B_320 = 320

class Samplerates(Enum):
    S_8 = 8000
    S_11 = 11025
    S_12 = 12000
    S_16 = 16000
    S_22 = 22050
    S_24 = 24000
    S_32 = 32000
    S_44 = 44100
    S_48 = 48000

class Encoders(Enum):
    MP3_LIBMP3LAME = 'libmp3lame'
    FLAC_FLAC = 'flac'
    OGG_OPUS = 'libopus'
    OGG_VORPIS = 'libvorpis'
    WAV_WAVPACK = 'wavpack'
    AIFF_PCM = 'pcm_s16be'
