import ffmpeg, os
from support import Codecs, Bitrates, Samplerates, Encoders

class Metadata:
    # creates a metadata object that can be returned as valid metadata for ffmpeg

    def __init__(self):
        self.title = None
        self.artist = None
        self.date = None
        self.album = None
        self.track = None
        self.album_artist = None
        self.comment = None

    def get(self):
        metadata = {}
        index = 0

        for key, tag in self.__dict__.items():
            if tag is not None:
                metadata['metadata:g:{}'.format(str(index))] = '{0}={1}'.format(key, str(tag))
                index += 1

        return metadata


class Converter:
    # creates a new conversion job with specified settings that can be executed on multiple files

    def __init__(self, codec: Codecs, encoder: Encoders, bitrate: Bitrates, samplerate: Samplerates, output_loc: str):
        # todo: make encoder, bitrate, and samplerate optional, have a default value to set them at
        # todo: possibly remove encoder argument all together, just have encoders set by default

            self.codec = codec
            self.encoder = encoder
            self.bitrate = bitrate
            self.samplerate = samplerate
            self.output_loc = output_loc

    def convert(self, input_file: str, cover_art: str, metadata: Metadata):
        output = None

        audio = ffmpeg.input(input_file).audio
        cover = ffmpeg.input(cover_art)

        cover_data = {
            'codec:v:1':'mjpeg',
            'metadata:s:v':'title={}'.format("cover"),
            'metadata:s:v':'comment={}'.format("Cover (front)")
                }

        path = os.path.join(self.output_loc, "{0}.{1}".format(metadata.title, self.codec.value))

        match self.codec:
            case Codecs.MP3:
                output = (
                    ffmpeg
                    .output(audio, cover, path, 
                            **metadata.get(), **cover_data, **{'acodec':self.encoder.value, 'b:a':'{}k'.format(str(self.bitrate.value)), 'ar':str(self.samplerate.value)})
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )
            case Codecs.WAV:
                output = (
                    ffmpeg
                    .output(audio, path, **{'acodec':self.encoder.value, 'ar':str(self.samplerate.value)})
                )
            case _:
                pass
            
        output.run()

def metadata_test():
    # testing out classes
    m = Metadata()

    m.title = "test"
    m.artist = "test"

    job = Converter(Codecs.MP3, Encoders.MP3_LIBMP3LAME, Bitrates.B_320, Samplerates.S_44, 'tests')

    job.convert('/Users/ringtail/dev/converter-tool/tests/songs1/1 intro.wav', '/Users/ringtail/dev/converter-tool/tests/songs1/cover art.JPG', m)

metadata_test()