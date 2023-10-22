import os, ffmpeg, tempfile, filecmp
from tkinter import filedialog
from support import FILEDIALOG_SUPPORTED_FILES, SUPPORTED_EXT, Codecs
from converter import Metadata

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

class Application():
    # instances the application, contains application functions

    def __init__(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        self.queue = []

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

        self.queue.append(group)


    def add_to_group(self, index, tracks):
        # adds tracks to an existing group

        group = queue[index]

        for new_track in tracks:
            group.tracks.append(new_track)
        
        self.debug_groups()


    def get_cover_art(self, path):
        # retrieves cover art from a imported track

        file_output = os.path.join(self.temp_folder.name + 'cover.jpg')

        command = (
            ffmpeg
            .input(path)
            .output(file_output, **{'c:v':'copy', 'frames:v':'1'})
            .global_args('-an')
            .run(overwrite_output=False)
        )


    def exit(self):
        # runs when app is closed

        self.temp_folder.cleanup()
        exit()
    
    
    def debug_groups(self):
        # just to check if all the data is correct
        for group in self.groups:
            print(group.__dict__)

            for track in group.tracks:

                print(track.__dict__)
                print(track.__dict__['metadata'].__dict__)
