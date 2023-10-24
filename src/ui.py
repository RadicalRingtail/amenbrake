import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

from app import Application
from support import Codecs, Samplerates


class Window(tk.Tk):
    # instances ui, contains things related to the main window

    def __init__(self):
        super().__init__()
        self.app = Application()

        self.title('AmenBrake')
        self.geometry('800x600')
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
        
        self.app.import_files(import_type)
        self.main.input_view.tree.update_tree()
    

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

        self.style = ttk.Style()
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
        self.tree = ImportTree(self, app)

        self.pack()


class EditorWidget(tk.Frame):
    # widget that contains metadata editing tools

    def __init__(self, root, app):
        super().__init__(master=root)
        self.rowconfigure(4)
        self.columnconfigure(4)
        self.app = app

        self.title = tk.StringVar()
        self.artist = tk.StringVar()
        self.date = tk.StringVar()
        self.album = tk.StringVar()
        self.track_number = tk.StringVar()
        self.album_artist = tk.StringVar()
        self.comment = tk.StringVar()

        label_title = tk.Label(text='Title')
        entry_title = tk.Entry(self, textvariable=self.title)

        label_artist = tk.Label(text='Artist')
        entry_artist = tk.Entry(self, textvariable=self.artist)

        label_date = tk.Label(text='Date')
        entry_date = tk.Entry(self, textvariable=self.date)

        label_album = tk.Label(text='Album')
        entry_album = tk.Entry(self, textvariable=self.album)

        label_track = tk.Label(text='Track Number')
        entry_track = tk.Entry(self, textvariable=self.track_number)

        label_album_artist = tk.Label(text='Album Artist')
        entry_album_artist = tk.Entry(self, textvariable=self.album_artist)

        label_comment = tk.Label(text='Comment')
        entry_comment = tk.Text(self, height=5)


        entry_artist.grid(column=1, row=1, sticky='nsew')
        entry_album_artist.grid(column=2, row=1, sticky='nsew')
        entry_date.grid(column=3, row=1, sticky='nsew')

        entry_album.grid(column=1, row=2, sticky='nsew')
        entry_track.grid(column=2, row=2, sticky='nsew')
        entry_title.grid(column=3, row=2, sticky='nsew')

        entry_comment.grid(column=1, row=3, columnspan=3, rowspan=2, sticky='nsew')

        self.pack(expand=False, fill='x')


class ImportTree(ttk.Treeview):
    # widget that shows imported tracks and groups

    def __init__(self, root, app):
        super().__init__(master=root)
        self.app = app
        self.current_selected_item = None

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

        print(self.current_selected_item)


    def update_tree(self):
        # removes all entries and re-adds them every time this is called (probably not efficient)

        index = 0
        track_index = 0

        for entry in self.get_children():
            self.delete(entry)
            index = 0
            track_index = 0

        for key, item in self.app.group_queue.items():
            group_item = self.insert(parent='', index='end', iid=key, open=True, values=['({0}) {1} - {2}'.format(index, item.album_artist, item.album), ''], tags=('group',))
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
        output_entry = tk.Entry(frame, textvariable=self.output)
        directory_button = tk.Button(frame, text='Select', command=self.on_directory_button)


        output_label.pack()
        output_entry.pack()
        directory_button.pack()
        frame.pack(fill='x', padx=(10,10), pady=(10,10))


    def on_directory_button(self):
        # opens filedialog for output_widget and sets the output directory string

        directory = filedialog.askdirectory(title='Select folder..')
        self.output.set(directory)
