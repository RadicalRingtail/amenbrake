import os, ffmpeg, tempfile
from pathlib import Path
from tkinter import filedialog
from support import FILEDIALOG_SUPPORTED_FILES, SUPPORTED_EXT, Codecs
from converter import Converter, Metadata
import helpers
import tkinter as tk
from tkinter import ttk
from PIL import Image


class Track:
    # instances a track object

    def __init__(self, path, codec: Codecs):
        self.path = path
        self.codec = codec
        self.cover_art = None
        self.preview_art = None
        self.metadata = None


class Group(helpers.Common):
    # instances a group object

    def __init__(self):
        self.tracks = {}
        self.temp_path = None
        self.cover_art = None
        self.preview_art = None
        self.metadata = None


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
        self.file_name_format = '{track} - {title}'
        self.sub_folder_name_format = '{album_artist} - {album} ({codec})'
        self.parent_folder_name_format = '{album_artist} - {album}'
        self.progress_window = None

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
            self.folder = filedialog.askdirectory(title='Open folder', initialdir='/')

            try:
                for f in os.listdir(self.folder):
                    if f.endswith(SUPPORTED_EXT):
                        files.append(os.path.join(self.folder, f))

                files = tuple(files)
            except FileNotFoundError:
                print('File or folder "{}" does not exist'.format(self.folder))
        
        if files:
        
            self.progress_window = ProgressWindow()

            imported_tracks = self.create_track_objects(files)
            self.create_group(imported_tracks, type)

            self.progress_window.close()
        
        else:
            pass


    def create_track_objects(self, paths):
        # creates a list of track objects

        track_objects = {}

        if self.progress_window is None:
            self.progress_window = ProgressWindow()

        for path in paths:
            self.progress_window.current_item.set('Importing:\n' + Path(path).name)
            self.progress_window.update()

            probe_data = ffmpeg.probe(path)['format']

            current_format = probe_data['format_name']
            track = Track(path, Codecs(current_format))

            metadata = Metadata()

            if 'tags' in probe_data:
                metadata.set_data(probe_data['tags'])
            else:
                metadata.title = Path(path).stem

            track.metadata = metadata

            track_objects[str(id(track))] = track

        return track_objects


    def create_group(self, tracks, import_type):
        # instaces a new group object and adds it to the group_queue

        group = Group()
        group_id = str(id(group))
        group.temp_path = os.path.join(self.temp_folder.name, group_id)
        metadata = Metadata()

        os.mkdir(group.temp_path)

        if tracks:

            group.tracks = tracks

            if import_type == 'folder':
                metadata.album = os.path.basename(self.folder)

            self.get_cover_art(group)

            images = Path(group.temp_path).glob('*.jpg')
            image_list = list(i for i in images)

            # gets first image gotten in temp cover art folder
            if not image_list:
                pass
            else:
                group.cover_art = os.path.join(group.temp_path, image_list[0].name)

        group.metadata = metadata
        self.group_queue[group_id] = group


    def add_to_group(self, id):
        # adds tracks to an existing group

        files = filedialog.askopenfilenames(title='Open file(s)', initialdir='/', filetypes=FILEDIALOG_SUPPORTED_FILES())

        if files:
            tracks = self.create_track_objects(files)
            group = self.group_queue[id]

            group.tracks.update(tracks)
            self.get_cover_art(group)


    def get_cover_art(self, group):
        # retrieves cover art from the track(s) in a group
        # todo: remove duplicates of cover art while still assigning the correct images to tracks
        
        index = 0

        for key, track in group.tracks.items():
            self.progress_window.current_item.set('Getting cover art for:\n' + Path(track.path).name)
            self.progress_window.update()

            
            file_name_rip = '{0}_{1}.jpg'.format(Path(track.path).stem, str(index))
            file_name_resize = '{0}_{1}_resize.jpg'.format(Path(track.path).stem, str(index))

            file_output_rip = os.path.join(group.temp_path, file_name_rip)
            file_output_resize = os.path.join(group.temp_path, file_name_resize)

            try:
                command = (
                    ffmpeg
                    .input(track.path)
                    .output(file_output_rip, **{'c:v':'copy', 'frames:v':'1'})
                    .global_args('-an')
                    .run(overwrite_output=True, quiet=True)
                )

                resize = Image.open(file_output_rip).resize((128,128))
                resize.convert('RGB')
                resize.save(file_output_resize)

                track.cover_art = file_output_rip
                track.preview_art = file_output_resize

                index += 1
            except ffmpeg.Error as e:
                print('error retrieving cover art: ' + str(e))

    def create_preview(self, img_path, item_id):

        file_output = os.path.join(self.temp_folder.name, '{0}_{1}_resize.jpg'.format(Path(img_path).stem, str(item_id)))

        resize = Image.open(img_path).resize((128,128))
        jpg = resize.convert('RGB')
        jpg.save(file_output)

        return(file_output)


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
                        self.file_name_format,
                        self.sub_folder_name_format,
                        self.parent_folder_name_format
                    )


    def debug_groups(self):
        # just to check if all the data is correct
        print(self.group_queue)
        for key, group in self.group_queue.items():
            print(group.__dict__)

            for key, track in group.tracks.items():

                print(track.__dict__)