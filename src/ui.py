import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

from app import Application
from support import Codecs


class Window(tk.Tk):
    # instances ui, contains things related to the main window

    def __init__(self):
        super().__init__()
        self.app = Application()

        self.title('converter tool')
        self.geometry('800x600')
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.create_menu()
        self.create_layout()
        
        self.mainloop()


    def on_close(self):
        self.app.exit()

    def on_import_file(self, import_type):
        self.app.import_files(import_type)
        self.main.input_view.update_tree()
    

    def create_menu(self):
        menu = tk.Menu(self)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Open file(s)', command=lambda: self.on_import_file('file'))
        file_menu.add_command(label='Open folder', command=lambda: self.on_import_file('folder'))
        
        menu.add_cascade(label='File', menu=file_menu)

        self.configure(menu=menu)


    def create_layout(self):
        self.main = Tabs(self, self.app)


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

        self.tree = ImportTree(self, app)

        button2 = tk.Button(self, text='start queue', command=self.app.start_queue).pack()

        self.pack()


class OutputView(tk.Frame):
    # instances the Output view frame

    def __init__(self, app):
        super().__init__()
        self.app = app

        add_job_button = tk.Button(self, text='Add transcode job..', command=self.create_encoder_options)
        add_job_button.pack()

        self.pack()

    def create_encoder_options(self):
        option = EncoderOptions(self, self.app)


class ImportTree(ttk.Treeview):
    # widget that shows imported tracks and groups

    def __init__(self, root, app):
        super().__init__(master=root)
        self.app = app

        self['columns'] = ('filename', 'location')

        self.column('#0', width=20, stretch=False)

        self.heading('filename', text='Filename')
        self.heading('location', text='Location')

        self.pack(expand=True, fill='both')

    def update_tree(self):
        for key, item in self.app.group_queue.items():
            item_index = str(key)
            group_item = self.insert(parent='', index='end', values=[item_index, ''])

            for track in item.tracks:

                track_filename = Path(track.path).name
                self.insert(parent=group_item, index='end', values=[track_filename, track.path])


class EncoderOptions(tk.Frame):
    # widget that gives you encoding options for a transcode job in queue

    def __init__(self, root, app):
        super().__init__(master=root, bg='gainsboro')
        self.app = app

        self.app.add_transcode_job({})
        
        self.codec = ttk.Combobox(self, values=tuple(item.value for item in Codecs), state='readonly')
        self.codec.pack(expand=True, padx=(10,10), pady=(10,10))

        self.pack(fill='x', padx=(10,10), pady=(10,10))