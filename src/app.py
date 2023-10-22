import os, ffmpeg, tempfile
from pathlib import Path
from tkinter import filedialog
from support import FILEDIALOG_SUPPORTED_FILES, SUPPORTED_EXT, Codecs
from converter import Metadata
import helpers

class Track:
    # instances a track object

    def __init__(self, path, codec: Codecs):
        self.path = path
        self.codec = codec
        self.cover_art = None
        self.metadata = None

class Group:
    # instances a group object (album)

    def __init__(self):
        self.album = None
        self.album_artist = None
        self.date = None
        self.cover_art = None
        self.tracks = None
        self.temp_path = None

class Application():
    # instances the application, contains application functions

    def __init__(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        self.queue = []
    

    def exit(self):
        # runs when app is closed

        self.temp_folder.cleanup()
        exit()
    

    def import_files(self, type):
        # opens a filedialog and creates a tuple of file paths which are then turned into track objects and added to a group object

        files = []

        if type == 'file':
            files = filedialog.askopenfilenames(title='Open file(s)', initialdir='/', filetypes=FILEDIALOG_SUPPORTED_FILES())
        elif type == 'folder':
            folder = filedialog.askdirectory(title='Open folder', initialdir='/')

            for f in os.listdir(folder):
                if f.endswith(SUPPORTED_EXT):
                    files.append(os.path.join(folder, f))

            files = tuple(files)

        imported_tracks = self.create_track_objects(files)
        self.create_group(imported_tracks)

        self.debug_groups()


    def create_track_objects(self, paths):
        # creates a list of track objects

        track_objects = []

        for path in paths:
            probe_data = ffmpeg.probe(path)['format']

            current_format = probe_data['format_name']
            track = Track(path, Codecs(current_format))

            if 'tags' in probe_data:
                metadata = Metadata()
                metadata.set_data(probe_data['tags'])

                track.metadata = metadata

            track_objects.append(track)

        return track_objects


    def create_group(self, tracks):
        # instaces a new group object and appends it to the queue

        group = Group()
        group.tracks = tracks
        group.temp_path = os.path.join(self.temp_folder.name, str(id(self)))
        os.mkdir(group.temp_path)

        self.get_cover_art(group)
        images = Path(group.temp_path).glob('*.jpg')
        group.cover_art = os.path.join(group.temp_path, list(img.name for img in images)[0])

        self.queue.append(group)


    def add_to_group(self, index, tracks):
        # adds tracks to an existing group

        group = queue[index]

        for new_track in tracks:
            group.tracks.append(new_track)


    def get_cover_art(self, group):
        # retrieves cover art from the track(s) in a group
        # todo: remove duplicates of cover art while still assigning the correct images to tracks
        
        index = 0

        for track in group.tracks:
            
            file_name = '{0}_{1}.jpg'.format(Path(track.path).stem, str(index))
            file_output = os.path.join(group.temp_path, file_name)

            command = (
                ffmpeg
                .input(track.path)
                .output(file_output, **{'c:v':'copy', 'frames:v':'1'})
                .global_args('-an')
                .run(overwrite_output=True, quiet=True)
            )

            track.cover_art = file_output

            index += 1


    def debug_groups(self):
        # just to check if all the data is correct
        for group in self.queue:
            print(group.__dict__)

            for track in group.tracks:

                print(track.__dict__)
                print(track.__dict__['metadata'].__dict__)

app = Application()
app.import_files('file')