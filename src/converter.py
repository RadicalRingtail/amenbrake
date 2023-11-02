import ffmpeg, os
from pathlib import Path
from support import Codecs, Bitrates, Samplerates, Encoders, Quality
import helpers
from zipfile import ZipFile


class Metadata(helpers.Common):
    # instances a metadata object that can be returned as valid metadata for ffmpeg

    def __init__(self):
        self.title = ''
        self.artist = ''
        self.date = ''
        self.album = ''
        self.track = ''
        self.album_artist = ''
        self.comment = ''


    def get_data(self):
        metadata = {}
        index = 0

        for key, tag in self.__dict__.items():
            if tag is not '':
                metadata['metadata:g:{}'.format(str(index))] = '{0}={1}'.format(key, str(tag))
                index += 1

        return metadata


class Converter(helpers.Common):
    # creates a new conversion job with specified settings that can be executed on multiple files
    # wav is borked, fix that
    # files not recieving metadata when converted in large batches for some reason

    def __init__(self):

            self.output_loc = ''
            self.parent_dir = False
            self.zip_folder = False
            self.codec = Codecs.MP3.value
            self.bitrate = Bitrates.B_320.value
            self.samplerate = Samplerates.S_44.value
            self.encoder = Encoders.LIBMP3LAME.value
            self.vbr = False
            self.quality = None


    def convert(self, input_file, cover_art, metadata: Metadata, file_out_name, folder_out_name, parent_folder_name):
        # transcodes, adds metadata/cover art, sets encoding options

        # todo: aac support

        output = None
        
        valid_tags = metadata.__dict__
        valid_tags.update(super().__dict__)

        cover_data = {
            'c:v':'mjpeg',
            'metadata:s:v':'title={}'.format("cover"),
            'metadata:s:v':'comment={}'.format("Cover (front)")
                }

        options = {
            'c:a':self.encoder, 
            'ar':self.samplerate
                }
        
        folder_name = ''

        if metadata.title == '':
            name_format = Path(input_file).stem + '.' + self.codec
        else:
            name_format = file_out_name.format_map(helpers.FormatFilter(valid_tags)) + '.' + self.codec

            folder_name = folder_out_name.format_map(helpers.FormatFilter(valid_tags))

        if self.parent_dir:
            group_folder = os.path.join(self.output_loc, parent_folder_name.format_map(helpers.FormatFilter(valid_tags)))
            if os.path.exists(group_folder):
                pass
            else:
                os.mkdir(group_folder)

            full_folder_path = os.path.join(group_folder, folder_name)

        else:
            full_folder_path = os.path.join(self.output_loc, folder_name)

        path = os.path.join(full_folder_path, name_format)

        print(path)

        if os.path.exists(full_folder_path):
            pass
        else:
            os.mkdir(full_folder_path)

        audio = ffmpeg.input(input_file).audio
        cover = ffmpeg.input(cover_art, pix_fmt='yuvj420p')

        match self.codec:
            case 'mp3':
                if self.vbr:
                    options['q:a'] = self.quality
                elif not self.vbr:
                    options['b:a'] = self.bitrate

                output = (
                    ffmpeg
                    .output(audio, cover, path, **metadata.get_data(), **cover_data, **options)
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )

            case 'flac':
                options['compression_level'] = self.quality

                output = (
                    ffmpeg
                    .output(audio, cover, path, **metadata.get_data(), **cover_data, **options)
                    .global_args('-map', '0')
                    .global_args('-map', '1')
                )

            case 'aiff':
                output = (
                    ffmpeg
                    .output(audio, path, **metadata.get_data(), **cover_data, **options)
                )

            case 'ogg':
                if self.vbr:
                    options['q:a'] = self.quality
                elif not self.vbr:
                    options['b:a'] = self.bitrate

                output = (
                    ffmpeg
                    .output(audio, cover, path, **options)
                )

            case 'wav':
                output = (
                    ffmpeg
                    .output(audio, path, **options)
                )
            
        output.run(overwrite_output=True, quiet=True)

        if self.zip_folder:
            zip_path = full_folder_path + '.zip'
            folder_in_zip = os.path.join(folder_name, os.path.basename(path))

            if os.path.exists(zip_path):
                with ZipFile(zip_path, 'a') as z:
                    z.write(path, folder_in_zip)
            else:
                with ZipFile(zip_path, 'w') as z:
                    z.write(path, folder_in_zip)