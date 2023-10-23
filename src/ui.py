import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path

from app import Application


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

        self.add(self.input_view, text='Input')
        self.add(self.output_view, text='Output')

        self.bind('<<NotebookTabChanged>>', lambda update: root.update_idletasks())

        self.pack(expand=True, fill='both')


class InputView(tk.Frame):
    # instances the input view frame

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.create_tree()

        button = tk.Button(self, text='add job', command=lambda: self.app.add_transcode_job({})).pack()
        button2 = tk.Button(self, text='start queue', command=self.app.start_queue).pack()

        self.pack()

    def create_tree(self):
        columns = ('filename', 'location')

        self.tree = ttk.Treeview(self, columns=columns)

        self.tree.column('#0', width=20, stretch=False)

        self.tree.heading('filename', text='Filename')
        self.tree.heading('location', text='Location')

        self.tree.pack(expand=True, fill='both')
    
    def update_tree(self):
        for key, item in self.app.group_queue.items():
            item_index = str(key)
            group_item = self.tree.insert(parent='', index='end', values=[item_index, ''])

            for track in item.tracks:

                track_filename = Path(track.path).name
                self.tree.insert(parent=group_item, index='end', values=[track_filename, track.path])

class OutputView(tk.Frame):
    # instances the Output view frame

    def __init__(self, app):
        super().__init__()
        self.pack()
        self.app = app