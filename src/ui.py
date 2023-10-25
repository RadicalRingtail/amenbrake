import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import platform
from PIL import Image, ImageTk

from app import Application
from support import Codecs, Samplerates


class Window(tk.Tk):
    # instances ui, contains things related to the main window

    def __init__(self):
        super().__init__()
        self.app = Application()

        self.title('AmenBrake')
        self.geometry('800x600')
        self.minsize(800,600)
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        
        self.create_style()
        self.create_menu()
        self.create_layout()
        
        self.mainloop()


    def on_close(self):
        # closes app

        self.app.exit()


    def on_import_file(self, import_type):
        # file importer
        tree = self.main.input_view.editor.tree
        self.app.import_files(import_type)
        tree.update_tree()
    

    def create_menu(self):
        # creates the top bar menu

        menu = tk.Menu(self)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Open file(s)', command=lambda: self.on_import_file('file'))
        file_menu.add_command(label='Open folder', command=lambda: self.on_import_file('folder'))
        
        menu.add_cascade(label='File', menu=file_menu)

        self.configure(menu=menu)


    def create_layout(self):
        # might do more with this later

        self.main = Tabs(self, self.app)


    def create_style(self):
        # slightly edits the default style
        # todo: fix windows ui theme

        self.style = ttk.Style()

        if platform.system() == 'Windows':
            self.style.theme_use('vista')

        self.style.configure('TNotebook', tabposition='n', padx=10, pady=10)
        self.style.configure('Treeview', rowheight=30)


class Tabs(ttk.Notebook):
    # instaces the widget for the main window tabs

    def __init__(self, root, app):
        super().__init__()

        self.input_view = InputView(app)
        self.output_view = OutputView(app)

        self.add(self.input_view, text='Import')
        self.add(self.output_view, text='Encoder')

        self.bind('<<NotebookTabChanged>>', lambda update: root.update_idletasks())

        self.pack(expand=True, fill='both')


class InputView(tk.Frame):
    # instances the input view frame

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.editor = EditorWidget(self, app)

        self.pack()


class EditorWidget(tk.Frame):
    # widget that contains metadata editing tools

    def __init__(self, root, app):
        super().__init__(master=root)
        self.app = app

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        self.title = tk.StringVar()
        self.artist = tk.StringVar()
        self.date = tk.StringVar()
        self.album = tk.StringVar()
        self.track_number = tk.StringVar()
        self.album_artist = tk.StringVar()
        self.comment = tk.StringVar()

        self.current_art = ImageTk.PhotoImage(Image.open('image.png').resize((128,128)))

        self.create_entry_widget('Title:', self.title)
        self.create_entry_widget('Artist:', self.artist)
        self.create_entry_widget('Date:', self.date)
        self.create_entry_widget('Album:', self.album)
        self.create_entry_widget('Track Number:', self.track_number)
        self.create_entry_widget('Album Artist:', self.album_artist)

        self.art_frame = tk.Frame(self, padx=10, pady=10)

        self.art_preview = tk.Label(self.art_frame, image=self.current_art)
        self.art_preview.pack(fill='both')
        edit_art_button = ttk.Button(self.art_frame, text='Choose image..').pack(fill='both', expand=True)

        self.art_frame.grid(column=1, row=0, rowspan=6, sticky='nsew')

        self.pack(fill='x')

        # moved this here for now
        self.tree = ImportTree(root, app, self)

    def create_entry_widget(self, name, textvariable):
        widget_frame = tk.Frame(self)
        widget_frame.columnconfigure(0, weight=1)
        widget_frame.columnconfigure(1, weight=1)
        widget_frame.rowconfigure(0, weight=1)

        label = ttk.Label(widget_frame, text=name).grid(column=0,row=0, sticky='w')
        entry = ttk.Entry(widget_frame, textvariable=textvariable, width=38).grid(column=1, row=0, sticky='e')

        widget_frame.grid(column=0, sticky='nsew')

    def get_data(self):
        # gets all metadata from current selected object and fills in the entry feilds with it
        print(self.tree.current_selected_item.cover_art)

        self.current_art = ImageTk.PhotoImage(Image.open(self.tree.current_selected_item.cover_art).resize((200,200)))

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

        elif 'track' in selected_data['tags']:
            self.current_selected_item = self.app.group_queue[current_group].tracks[current_selection]

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


class OutputView(tk.Frame):
    # instances the Output view frame

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.encoder_widgets = {}

        add_job_button = tk.Button(self, text='Add format..', command=self.create_encoder_options)
        add_job_button.pack()

        self.pack()


    def create_encoder_options(self):
        option = EncoderOptions(self, self.app)
        job = self.app.add_transcode_job({})

        self.encoder_widgets[job] = option
        print(self.encoder_widgets)


class EncoderOptions(tk.Frame):
    # widget that gives you encoding options for a transcode job in queue

    def __init__(self, root, app):
        super().__init__(master=root, bg='gainsboro')
        self.app = app

        self.codec = tk.StringVar()
        self.samplerate = tk.StringVar()
        self.output = tk.StringVar()
        
        self.common_settings()
        self.output_widget()

        self.pack(fill='x', padx=(10,10), pady=(10,10))


    def common_settings(self):
        # settings that exist in every instance of EncoderOptions regardless of codec specific settings

        codec_dropdown = ttk.Combobox(self, textvariable=self.codec, values=Codecs.as_list(), state='readonly')
        codec_dropdown.current(0)

        samplerate_dropdown = ttk.Combobox(self, textvariable=self.samplerate, values=Samplerates.as_list())
        samplerate_dropdown.current(0)

        codec_dropdown.pack(expand=True, padx=(10,10), pady=(10,10))
        samplerate_dropdown.pack(expand=True, padx=(10,10), pady=(10,10))


    def output_widget(self):
        # for selecting and viewing the output path

        frame = tk.Frame(self)

        output_label = tk.Label(frame, text='Output Location')
        output_entry = ttk.Entry(frame, textvariable=self.output)
        directory_button = tk.Button(frame, text='Select', command=self.on_directory_button)


        output_label.pack()
        output_entry.pack()
        directory_button.pack()
        frame.pack(fill='x', padx=(10,10), pady=(10,10))


    def on_directory_button(self):
        # opens filedialog for output_widget and sets the output directory string

        directory = filedialog.askdirectory(title='Select folder..')
        self.output.set(directory)

    def get_combobox_value(self):
        pass
