import ffmpeg, os

class Metadata:
    # creates a metadata object that can be returned as valid metadata for ffmpeg

    def __init__(self):
        self.title = None
        self.artist = None
        self.date = None
        self.album = None
        self.track_number = None
        self.album_artist = None
        self.comment = None

    def get(self):
        metadata = {
            'metadata:g:0':'title={}'.format(self.title), 
            'metadata:g:1':'artist={}'.format(self.artist),
            'metadata:g:2':'date={}'.format(self.date),
            'metadata:g:3':'album={}'.format(self.album),
            'metadata:g:4':'track={}'.format(self.track_number),
            'metadata:g:5':'album_artist={}'.format(self.album_artist),
            'metadata:g:6':'comment={}'.format(self.comment),
                }

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

def metadata_test():
    # testing out classes
    m = Metadata()

    m.title = "test"
    m.artist = "test"

    job = Converter('mp3', 'libmp3lame', '320k', '44100', '')

    job.convert('/Users/ringtail/dev/converter-tool/tests/songs1/1 intro.wav', '/Users/ringtail/dev/converter-tool/tests/songs1/cover art.JPG', m)

metadata_test()