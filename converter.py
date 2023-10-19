import ffmpeg, os

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

    def __init__(self, codec, encoder, bitrate, samplerate, output_loc):
            self.codec = codec
            self.encoder = encoder
            self.bitrate = bitrate
            self.samplerate = samplerate
            self.output_loc = output_loc

    def convert(self, input_file, cover_art, metadata: Metadata):
        output = None

        audio = ffmpeg.input(input_file).audio
        cover = ffmpeg.input(cover_art)

        cover_data = {
            'codec:v:1':'mjpeg',
            'metadata:s:v':'title={}'.format("cover"),
            'metadata:s:v':'comment={}'.format("Cover (front)")
                }

        file_format = "{0}.{1}".format(metadata.title, self.codec)

        match self.codec:
            case 'mp3':
                output = (
                    ffmpeg
                    .output(audio, cover, os.path.join(self.output_loc, file_format), 
                            **metadata.get(), **cover_data, **{'acodec':self.encoder, 'b:a':self.bitrate, 'ar':self.samplerate})
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )
            case 'wav':
                output = (
                    ffmpeg
                    .output(audio, os.path.join(output_loc, self.metadata.title))
                )
            case 'flac':
                output = (
                    ffmpeg
                    .output(audio, cover, os.path.join(self.output_loc, file_format), 
                            **metadata.get(), **cover_data, **{'acodec':self.encoder, 'ar':self.samplerate})
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )
            case 'aiff':
                output = (
                    ffmpeg
                    .output(audio, cover, os.path.join(self.output_loc, file_format), 
                            **metadata.get(), **cover_data, **{'acodec':self.encoder, 'b:a':self.bitrate, 'ar':self.samplerate})
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )
            
        output.run()