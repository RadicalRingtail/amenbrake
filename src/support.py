from enum import Enum

class Codecs(Enum):
    WAV = 'wav'
    MP3 = 'mp3'
    FLAC = 'flac'
    AIFF = 'aiff'
    OGG = 'ogg'

class Bitrates(Enum):
    B_24 = '24k'
    B_32 = '32k'
    B_40 = '40k'
    B_48 = '48k'
    B_56 = '56k'
    B_64 = '64k'
    B_80 = '80v'
    B_96 = '96k'
    B_112 = '112k'
    B_128 = '128k'
    B_160 = '160k'
    B_192 = '192k'
    B_224 = '224k'
    B_256 = '256k'
    B_320 = '320k'

class Samplerates(Enum):
    S_8 = '8000'
    S_11 = '11025'
    S_12 = '12000'
    S_16 = '16000'
    S_22 = '22050'
    S_24 = '24000'
    S_32 = '32000'
    S_44 = '44100'
    S_48 = '48000'

class Encoders(Enum):
    LIBMP3LAME = 'libmp3lame'
    FLAC = 'flac'
    VORPIS = 'libvorpis'
    PCM_16 = 'pcm_s16be'

class Quality(Enum):
    # tuples of compression and quality values for each encoder within a valid range as per ffmpeg documentation

    LAME = tuple([str(i) for i in range(0, 10)])
    FLAC = tuple([str(i) for i in range(0, 13)])
    VORBIS = tuple([str(i / 10.0) for i in range(-10, 105, 5)])

def FILEDIALOG_SUPPORTED_FILES():
    # returns all valid file types for use in tkinter filedialog

    filetypes = []

    for c in Codecs:
        filetypes.append(('{} Files'.format(c.value.upper()), '*.{}'.format(c.value)))

    return(tuple(filetypes))