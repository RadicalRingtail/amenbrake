import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
from PIL import Image, ImageTk


class EditorWidget(ttk.Frame):
    # widget that contains metadata editing tools
    # a lot of the code here is very sloppy and not very efficient, probably needs to be redone

    def __init__(self, root, app):
        super().__init__(master=root, padding=10)
        self.app = app

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)


        self.title = tk.StringVar()
        self.artist = tk.StringVar()
        self.date = tk.StringVar()
        self.album = tk.StringVar()
        self.track_number = tk.StringVar()
        self.album_artist = tk.StringVar()
        self.comment = tk.StringVar()

        self.entry_widgets = []
        self.current_art = ImageTk.PhotoImage(Image.open('src/images/ui_art_placeholder.png'))

        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(column=0, row=0, rowspan=6, sticky='nsew')

        for i in self.entry_widgets:
            i.grid(column=0, sticky='nsew')

        ttk.Separator(self, orient='vertical').grid(column=1, row=0, rowspan=6, sticky='ns')

        self.art_frame = ttk.Frame(self)

        self.art_preview = tk.Label(self.art_frame, image=self.current_art)
        self.art_preview.pack(fill='both')
        clear_art_button = ttk.Button(self.art_frame, text='Clear image..').pack(fill='both', expand=True)
        edit_art_button = ttk.Button(self.art_frame, text='Choose image..').pack(fill='both', expand=True)

        self.art_frame.grid(column=2, row=0, rowspan=6, sticky='nsew')

        self.pack(fill='x')

        # moved this here for now
        self.tree = ImportTree(root, app, self)

    def create_track_entry(self):
        for i in self.entry_widgets:
            i.destroy()

        self.entry_widgets = [
            self.create_entry_widget(self.input_frame, 'Title:', self.title),
            self.create_entry_widget(self.input_frame, 'Artist:', self.artist),
            self.create_entry_widget(self.input_frame, 'Year:', self.date),
            self.create_entry_widget(self.input_frame, 'Album:', self.album),
            self.create_entry_widget(self.input_frame, 'Track Number:', self.track_number),
            self.create_entry_widget(self.input_frame, 'Album Artist:', self.album_artist)
            ]
        for i in self.entry_widgets:
            i.grid(column=0, sticky='nsew')

    def create_album_entry(self):
        for i in self.entry_widgets:
            i.destroy()

        self.entry_widgets = [
            self.create_entry_widget(self.input_frame, 'Artist:', self.album_artist),
            self.create_entry_widget(self.input_frame, 'Album:', self.album),
            self.create_entry_widget(self.input_frame, 'Year:', self.date)
            ]
        for i in self.entry_widgets:
            i.grid(column=0, sticky='nsew')

    def create_entry_widget(self, root, name, textvariable):
        widget_frame = ttk.Frame(root)
        widget_frame.columnconfigure(0, weight=1)
        widget_frame.columnconfigure(1, weight=1)
        widget_frame.rowconfigure(0, weight=1)

        label = ttk.Label(widget_frame, text=name).grid(column=0,row=0, sticky='w')
        entry = ttk.Entry(widget_frame, textvariable=textvariable, width=38).grid(column=1, row=0, sticky='e')

        return(widget_frame)

    def get_data(self):
        # gets all metadata from current selected object and fills in the entry feilds with it

        preview_image = os.path.splitext(self.tree.current_selected_item.cover_art)[0] + '_resize.jpg'

        self.current_art = ImageTk.PhotoImage(Image.open(preview_image))

        self.art_preview.configure(image=self.current_art)

        self.title.set(self.tree.current_selected_item.metadata.title)
        self.artist.set(self.tree.current_selected_item.metadata.artist)
        self.date.set(self.tree.current_selected_item.metadata.date)
        self.album.set(self.tree.current_selected_item.metadata.album)
        self.track_number.set(self.tree.current_selected_item.metadata.track)
        self.album_artist.set(self.tree.current_selected_item.metadata.album_artist)
        self.comment.set(self.tree.current_selected_item.metadata.comment)

    
    def set_data(self):
        # sets the metadata of an item to the current field data

        self.tree.current_selected_item.metadata.title = self.title.get()
        self.tree.current_selected_item.metadata.artist = self.artist.get()
        self.tree.current_selected_item.metadata.date = self.date.get()
        self.tree.current_selected_item.metadata.album = self.album.get()
        self.tree.current_selected_item.metadata.track = self.track_number.get()
        self.tree.current_selected_item.metadata.album_artist = self.album_artist.get()
        self.tree.current_selected_item.metadata.comment = self.comment.get()
        

class ImportTree(ttk.Treeview):
    # widget that shows imported tracks and groups

    def __init__(self, root, app, editor):
        super().__init__(master=root)
        self.app = app
        self.editor = editor
        self.current_selected_item = None
        self.previous_selected_item = None

        self.tag_configure('even', background='white smoke')
        self.tag_configure('odd', background='gainsboro')

        self['columns'] = ('filename', 'location')

        self.column('#0', width=20, stretch=False)

        self.heading('filename', text='Filename')
        self.heading('location', text='Location')

        self.bind('<<TreeviewSelect>>', self.select_item)

        self.pack(expand=True, fill='both')


    def select_item(self, event):
        # gets current selected item and returns the correct corresponding data from the backend (probably over engineered)

        current_selection = self.selection()[0]
        selected_data = self.item(self.focus())
        current_group = self.parent(current_selection)

        if 'group' in selected_data['tags']:
            self.current_selected_item = self.app.group_queue[current_selection]
            self.editor.create_album_entry()

        elif 'track' in selected_data['tags']:
            self.current_selected_item = self.app.group_queue[current_group].tracks[current_selection]
            self.editor.create_track_entry()

        print(str(self.current_selected_item) + ' , ' + str(self.previous_selected_item))
        self.editor.get_data()
        self.previous_selected_item = self.current_selected_item


    def update_tree(self):
        # removes all entries and re-adds them every time this is called (probably not efficient)

        index = 0
        track_index = 0

        for entry in self.get_children():
            self.delete(entry)
            index = 0
            track_index = 0

        for key, item in self.app.group_queue.items():
            group_item = self.insert(parent='', index='end', iid=key, open=True, values=['({0}) {1} - {2}'.format(index, item.metadata.album_artist, item.metadata.album), ''], tags=('group',))
            index += 1
            print(self.index(group_item))

            for key, track in item.tracks.items():
                track_filename = Path(track.path).name

                if track_index % 2 == 0:
                    self.insert(parent=group_item, index='end', iid=key, values=[track_filename, track.path], tags=('even', 'track',))
                else:
                    self.insert(parent=group_item, index='end', iid=key, values=[track_filename, track.path], tags=('odd', 'track',))

                track_index += 1
