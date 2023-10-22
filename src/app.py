import os, ffmpeg
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

class Application():
    # instances the application, contains application functions

    def __init__(self):
        pass

    def create_objects(self, file_list):
        # creates a list of track objects

        track_objects = []

        for path in file_list:
            probe_data = ffmpeg.probe(path)['format']

            current_format = probe_data['format_name']
            track = Track(path, Codecs(current_format).name)

            if 'tags' in probe_data:
                metadata = Metadata()
                metadata.set_data(probe_data['tags'])

                track.metadata = metadata

            track_objects.append(track)

        print(track_objects)

    def input_files(self, type):
        # opens a filedialog and returns a tuple of full file paths to all valid files that the user selected or that were in a selected directory

        files = []

        if type == 'file':
            files = filedialog.askopenfilenames(title='Open file(s)', initialdir='/', filetypes=FILEDIALOG_SUPPORTED_FILES())
        elif type == 'folder':
            folder = filedialog.askdirectory(title='Open folder', initialdir='/')

            for f in os.listdir(folder):
                if f.endswith(SUPPORTED_EXT):
                    files.append(os.path.join(folder, f))

            files = tuple(files)

        self.create_objects(files)

# testing/debug
app = Application()

app.input_files('file')