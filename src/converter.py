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

    def __init__(self, codec: Codecs, output_loc: str):

            self.output_loc = output_loc

            self.codec = codec
            self.bitrate = Bitrates.B_320
            self.samplerate = Samplerates.S_44
            self.encoder = None
            self.vbr = False
            self.quality = None

    def convert(self, input_file: str, cover_art: str, metadata: Metadata):
        output = None

        cover_data = {
            'c:v':'mjpeg',
            'metadata:s:v':'title={}'.format("cover"),
            'metadata:s:v':'comment={}'.format("Cover (front)")
                }

        options = {
            'c:a':self.encoder.value, 
            'ar':self.samplerate.value
                }

        path = os.path.join(self.output_loc, "{0}.{1}".format(metadata.title, self.codec.value))

        audio = ffmpeg.input(input_file).audio
        cover = ffmpeg.input(cover_art, pix_fmt='yuvj420p')

        match self.codec:
            case Codecs.MP3:
                if vbr:
                    options['q:a'] = self.quality.value
                elif not vbr:
                    options['b:a'] = self.bitrate.value

                output = (
                    ffmpeg
                    .output(audio, cover, path, **metadata.get(), **cover_data, **options)
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )

            case Codecs.FLAC:
                options['compression_level'] = self.quality.value

                output = (
                    ffmpeg
                    .output(audio, cover, path, **metadata.get(), **cover_data, **options)
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )

            case Codecs.AIFF:
                output = (
                    ffmpeg
                    .output(audio, path, **metadata.get(), **cover_data, **options)
                )

            case Codecs.OGG:
                if vbr:
                    options['q:a'] = self.quality.value
                elif not vbr:
                    options['b:a'] = self.bitrate.value

                output = (
                    ffmpeg
                    .output(audio, cover, path, **options)
                )

            case Codecs.WAV:
                output = (
                    ffmpeg
                    .output(audio, path, **options)
                )
            
        output.run()

def metadata_test():
    # testing out classes
    m = Metadata()

    m.title = "test"
    m.artist = "test"

    job = Converter(Codecs.MP3, 'tests')

    job.convert('/Users/ringtail/dev/converter-tool/tests/songs1/1 intro.wav', '/Users/ringtail/dev/converter-tool/tests/songs1/cover art.JPG', m)
    
metadata_test()

print(ffmpeg.probe('/Users/ringtail/dev/converter-tool/tests/test.mp3')['streams'])