import os, ffmpeg
from tkinter import filedialog
from support import FILEDIALOG_SUPPORTED_FILES, SUPPORTED_EXT, Codecs

class Application():
    # instances the application, contains application functions

    def __init__(self):
        self.file_list = None

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

        self.file_list = files
        print(self.file_list)

class Track:
    # instances a track object

    def __init__(self, path, codec: Codecs):
        self.path = path
        self.Codecs = Codecs

        self.cover_art = None
        self.metadata = None

# testing/debug
app = Application()

app.input_files('folder')