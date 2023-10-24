import os, ffmpeg, tempfile
from pathlib import Path
from tkinter import filedialog
from support import FILEDIALOG_SUPPORTED_FILES, SUPPORTED_EXT, Codecs
from converter import Converter, Metadata
import helpers
import tkinter as tk
from tkinter import ttk


class Track:
    # instances a track object

    def __init__(self, path, codec: Codecs):
        self.path = path
        self.codec = codec
        self.cover_art = None
        self.metadata = None


class Group(helpers.Common):
    # instances a group object

    def __init__(self):
        self.album = None
        self.album_artist = None
        self.date = None
        self.cover_art = None
        self.tracks = None
        self.temp_path = None


class ProgressWindow(tk.Toplevel):
    # creates a new toplevel window with a progress bar

    def __init__(self):
        super().__init__()
        self.title('Importing items..')
        self.geometry('400x100')

        self.current_item = tk.StringVar()
        
        self.current_status = tk.Label(self, textvariable=self.current_item)
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length='300', mode='indeterminate')

        self.current_status.pack(expand=True, fill='y')
        self.progress_bar.pack(expand=True, fill='y')
        self.update()

    def close(self):
        self.destroy()
        self.update()


class Application():
    # instances the application, contains application functions

    def __init__(self):
        self.temp_folder = tempfile.TemporaryDirectory()
        self.group_queue = {}
        self.transcode_queue = {}
        self.file_name_format = '{title}'
    

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
        
        if files:
        
            self.progress_window = ProgressWindow()

            imported_tracks = self.create_track_objects(files)
            self.create_group(imported_tracks)

            self.debug_groups()

            self.progress_window.close()
        
        else:
            pass


    def create_track_objects(self, paths):
        # creates a list of track objects

        track_objects = {}

        for path in paths:
            self.progress_window.current_item.set('Importing ' + Path(path).name)
            self.progress_window.update()

            probe_data = ffmpeg.probe(path)['format']

            current_format = probe_data['format_name']
            track = Track(path, Codecs(current_format))

            metadata = Metadata()

            if 'tags' in probe_data:
                metadata.set_data(probe_data['tags'])

            track.metadata = metadata

            track_objects[str(id(track))] = track

        return track_objects


    def create_group(self, tracks):
        # instaces a new group object and adds it to the group_queue

        group = Group()
        group_id = str(id(group))

        group.tracks = tracks
        group.temp_path = os.path.join(self.temp_folder.name, group_id)
        os.mkdir(group.temp_path)

        self.get_cover_art(group)

        images = Path(group.temp_path).glob('*.jpg')
        image_list = list(i for i in images)

        if not image_list:
            pass
        else:
           group.cover_art = os.path.join(group.temp_path, image_list[0].name)

        self.group_queue[group_id] = group


    def add_to_group(self, id, tracks):
        # adds tracks to an existing group

        group = group_queue[id]

        for new_track in tracks:
            group.tracks.append(new_track)


    def get_cover_art(self, group):
        # retrieves cover art from the track(s) in a group
        # todo: remove duplicates of cover art while still assigning the correct images to tracks
        
        index = 0

        for key, track in group.tracks.items():
            
            file_name = '{0}_{1}.jpg'.format(Path(track.path).stem, str(index))
            file_output = os.path.join(group.temp_path, file_name)

            try:
                command = (
                    ffmpeg
                    .input(track.path)
                    .output(file_output, **{'c:v':'copy', 'frames:v':'1'})
                    .global_args('-an')
                    .run(overwrite_output=True, capture_stderr=True, quiet=True)
                )

                track.cover_art = file_output

                index += 1
            except ffmpeg.Error as e:
                print(e.stderr.decode('utf8'))


    def add_transcode_job(self, settings):
        # takes in settings from the front end and instances a converter object, then adds it to the queue

        job = Converter()
        job_id = str(id(job))
        job.set_data(settings)

        self.transcode_queue[job_id] = job
        
        return(job_id)


    def start_queue(self):
        # starts transcode queue

        for group_id, group in self.group_queue.items():
            for job_id, job in self.transcode_queue.items():

                for key, track in group.tracks.items():

                    job.convert(
                        track.path,
                        track.cover_art,
                        track.metadata,
                        self.file_name_format
                    )


    def debug_groups(self):
        # just to check if all the data is correct
        print(self.group_queue)
        for key, group in self.group_queue.items():
            print(group.__dict__)

            for key, track in group.tracks.items():

                print(track.__dict__)