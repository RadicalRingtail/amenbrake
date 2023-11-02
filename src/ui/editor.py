import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip
from tkinter import filedialog
from pathlib import Path
from PIL import Image, ImageTk

from support import FILEDIALOG_SUPPORTED_ART


class EditorWidget(ttk.Frame):
    # widget that contains metadata editing tools
    # a lot of the code here is very sloppy and not very efficient, probably needs to be redone or at least cleaned up

    def __init__(self, root, app):
        super().__init__(master=root, padding=10)
        self.app = app
        self.tree = ImportTree(root, app, self)

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

        self.copy_artist = tk.BooleanVar()
        self.copy_album = tk.BooleanVar()
        self.copy_album_artist = tk.BooleanVar()
        self.copy_year = tk.BooleanVar()
        self.copy_comment = tk.BooleanVar()
        self.copy_art = tk.BooleanVar()
        self.track_indexing = tk.BooleanVar()

        self.entry_widgets = []
        self.current_art = None

        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(column=0, row=0, rowspan=6, sticky='nsew')

        for i in self.entry_widgets:
            i.grid(column=0, sticky='nsew')

        ttk.Separator(self, orient='vertical').grid(column=1, row=0, rowspan=6, sticky='ns')

        self.art_frame = ttk.Frame(self)

        self.art_preview = tk.Label(self.art_frame, image=self.current_art)
        self.art_preview.pack(fill='both')

        self.edit_art_button = ttk.Button(self.art_frame, text='Choose image..', state='disabled', command=self.choose_art)
        self.edit_art_button.pack(fill='both', expand=True)
        self.clear_art_button = ttk.Button(self.art_frame, text='Clear image..', state='disabled', command=self.clear_art)
        self.clear_art_button.pack(fill='both', expand=True)

        self.art_frame.grid(column=2, row=0, rowspan=6, sticky='nsew')

        self.update_preview()

        self.pack(fill='x')
        self.tree.pack(fill='both', expand=True)


    def create_track_entry(self):
        # creates album entry widgets

        for i in self.entry_widgets:
            i.destroy()

        self.entry_widgets = [
            self.create_entry_widget(self.input_frame, 'Title:', self.title),
            self.create_entry_widget(self.input_frame, 'Artist:', self.artist),
            self.create_entry_widget(self.input_frame, 'Year:', self.date),
            self.create_entry_widget(self.input_frame, 'Album:', self.album),
            self.create_entry_widget(self.input_frame, 'Track Number:', self.track_number),
            self.create_entry_widget(self.input_frame, 'Album Artist:', self.album_artist),
            self.create_entry_widget(self.input_frame, 'Comment:', self.comment)
            ]
        for i in self.entry_widgets:
            i.grid(column=0, sticky='nsew')


    def create_album_entry(self):
        # creates album entry widgets

        for i in self.entry_widgets:
            i.destroy()

        copy_button = ttk.Button(self.input_frame, text='Copy group data to tracks', command=self.copy_group_data)

        self.entry_widgets = [
            self.create_entry_widget(self.input_frame, 'Artist:', self.album_artist),
            self.create_entry_widget(self.input_frame, 'Album:', self.album),
            self.create_entry_widget(self.input_frame, 'Year:', self.date),
            self.create_entry_widget(self.input_frame, 'Comment:', self.comment),
            ttk.Checkbutton(self.input_frame, text='Copy artist data', variable=self.copy_artist, onvalue=True, offvalue=False),
            ttk.Checkbutton(self.input_frame, text='Copy album data', variable=self.copy_album, onvalue=True, offvalue=False),
            ttk.Checkbutton(self.input_frame, text='Copy year data', variable=self.copy_year, onvalue=True, offvalue=False),
            ttk.Checkbutton(self.input_frame, text='Copy album artist data', variable=self.copy_album_artist, onvalue=True, offvalue=False),
            ttk.Checkbutton(self.input_frame, text='Copy comment data', variable=self.copy_comment, onvalue=True, offvalue=False),
            ttk.Checkbutton(self.input_frame, text='Copy cover art', variable=self.copy_art, onvalue=True, offvalue=False),
            ttk.Checkbutton(self.input_frame, text='Assign track number by order in group', variable=self.track_indexing, onvalue=True, offvalue=False),
            copy_button
            ]
        for i in self.entry_widgets:
            i.grid(column=0, sticky='nsew')


    def create_entry_widget(self, root, name, textvariable):
        # creates premade labeled entry widgets

        widget_frame = ttk.Frame(root)
        widget_frame.columnconfigure(0, weight=1)
        widget_frame.columnconfigure(1, weight=1)
        widget_frame.rowconfigure(0, weight=1)

        label = ttk.Label(widget_frame, text=name).grid(column=0,row=0, sticky='w')
        entry = ttk.Entry(widget_frame, textvariable=textvariable, width=38).grid(column=1, row=0, sticky='e')

        return(widget_frame)


    def set_feilds(self):
        # gets all metadata from current selected object and fills in the entry feilds with it
        
        self.update_preview()

        self.title.set(self.tree.current_selected_item.metadata.title)
        self.artist.set(self.tree.current_selected_item.metadata.artist)
        self.date.set(self.tree.current_selected_item.metadata.date)
        self.album.set(self.tree.current_selected_item.metadata.album)
        self.track_number.set(self.tree.current_selected_item.metadata.track)
        self.album_artist.set(self.tree.current_selected_item.metadata.album_artist)
        self.comment.set(self.tree.current_selected_item.metadata.comment)

    
    def set_data(self):
        # sets the metadata of an item to the current field data

        self.tree.previous_selected_item.metadata.title = self.title.get()
        self.tree.previous_selected_item.metadata.artist = self.artist.get()
        self.tree.previous_selected_item.metadata.date = self.date.get()
        self.tree.previous_selected_item.metadata.album = self.album.get()
        self.tree.previous_selected_item.metadata.track = self.track_number.get()
        self.tree.previous_selected_item.metadata.album_artist = self.album_artist.get()
        self.tree.previous_selected_item.metadata.comment = self.comment.get()


    def copy_group_data(self):
        # copies data to tracks in a group dependin on if checkboxes are enabled or not

        for key, track in self.tree.current_selected_item.tracks.items():

            if self.copy_artist.get():
                track.metadata.artist = self.album_artist.get()

            if self.copy_album_artist.get():
                track.metadata.album_artist = self.album_artist.get()

            if self.copy_album.get():
                track.metadata.album = self.album.get()
                
            if self.copy_year.get():
                track.metadata.date = self.date.get()

            if self.copy_year.get():
                track.metadata.comment = self.comment.get()

            if self.copy_art.get():
                track.cover_art = self.tree.current_selected_item.cover_art
                track.preview_art = self.tree.current_selected_item.preview_art

        if self.track_indexing.get():
            for index, item in enumerate(self.tree.current_selected_item.tracks.items(), start=1):
                item[1].metadata.track = str(index)


    def choose_art(self):
        # opens filedialog to get cover art, then sets the cover art path for the selected item and updates the preview

        art_path = filedialog.askopenfilename(title='Choose cover art..', initialdir='/', filetypes=FILEDIALOG_SUPPORTED_ART)
        preview_image = self.app.create_preview(art_path, self.tree.selection()[0])

        self.tree.current_selected_item.cover_art = art_path
        self.tree.current_selected_item.preview_art = preview_image

        self.update_preview()


    def update_preview(self):
        # will changes the cover art preview to either the items preview thumbnail, or a placeholder if there is none

        if self.tree.current_selected_item is not None:
            if self.tree.current_selected_item.cover_art is not None and self.tree.current_selected_item.preview_art is not None:
                self.current_art = ImageTk.PhotoImage(Image.open(self.tree.current_selected_item.preview_art))
            else:
                self.current_art = ImageTk.PhotoImage(Image.open('src/images/ui_art_placeholder.png'))
        else:
            self.current_art = ImageTk.PhotoImage(Image.open('src/images/ui_art_placeholder.png'))

        self.art_preview.configure(image=self.current_art)


    def clear_art(self):
        # removes cover art from a selected item

        self.tree.current_selected_item.cover_art = None
        self.tree.current_selected_item.preview_art = None

        self.update_preview()
        

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

        self.bind('<Button-2>', self.create_right_click_menu)
        self.bind('<Button-3>', self.create_right_click_menu)


    def select_item(self, event):
        # gets current selected item and returns the correct corresponding data from the backend (probably over engineered)

        current_selection = self.selection()[0]
        selected_data = self.item(self.focus())
        current_group = self.parent(current_selection)

        if self.previous_selected_item is not None:
            self.editor.set_data()

        if 'group' in selected_data['tags']:
            self.current_selected_item = self.app.group_queue[current_selection]
            self.editor.create_album_entry()

        elif 'track' in selected_data['tags']:
            self.current_selected_item = self.app.group_queue[current_group].tracks[current_selection]
            self.editor.create_track_entry()

        self.editor.set_feilds()
        self.previous_selected_item = self.current_selected_item

        self.editor.clear_art_button['state'] = 'enabled'
        self.editor.edit_art_button['state'] = 'enabled'


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

        selection_id = self.get_children()[0]
        self.focus(selection_id)
        self.selection_set(selection_id)
    
    def remove_items(self):
        # removes all selected tree items

        for item in self.selection():

            if 'group' in self.item(item)['tags']:
                del self.app.group_queue[item]
            elif 'track' in self.item(item)['tags']:
                del self.app.group_queue[self.parent(item)].tracks[item]
            
            self.delete(item)
            
            for widget in self.editor.entry_widgets:
                widget.destroy()


    def add_itmes(self, selected_item):

        if 'group' in selected_item['tags']:
            self.app.add_to_group(self.selection()[0])
            self.update_tree()
        elif 'track' in selected_item['tags']:
            self.app.add_to_group(self.parent(selected_item))
            self.update_tree()


    def create_right_click_menu(self, event):
        # creates a right click menu on the tree

        selected_item = self.item(self.identify_row(event.y))

        menu = tk.Menu(self, tearoff=0)

        if 'group' in selected_item['tags']:
            menu.add_command(label='Add tracks..', command=lambda: self.add_itmes(selected_item))
            menu.add_command(label='Remove..', command=self.remove_items)
        elif 'track' in selected_item['tags']:
            menu.add_command(label='Remove..', command=self.remove_items)
        else:
            menu.add_command(label='Import track(s)..', command=lambda: self.right_click_import('file'))
            menu.add_command(label='Import folder..', command=lambda: self.right_click_import('folder'))

        try: 
            menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            menu.grab_release() 


    def right_click_import(self, filedialog_type):
        # imports files and updates tree

        self.app.import_files(filedialog_type)
        self.update_tree()