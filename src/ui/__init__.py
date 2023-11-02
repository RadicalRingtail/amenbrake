import tkinter as tk
from tkinter import ttk, messagebox
import platform
from PIL import Image, ImageTk

from app import Application
from ui import editor, encoder


class Window(tk.Tk):
    # instances ui, contains things related to the main window

    def __init__(self):
        super().__init__()
        self.app = Application()

        self.title('AmenBrake')
        self.geometry('800x800')
        self.minsize(800,700)
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
        self.bottombar = BottomBar(self, self.app)


    def create_style(self):
        # slightly edits the default style
        # todo: fix windows ui theme

        self.style = ttk.Style()

        if platform.system() == 'Windows':
            self.style.theme_use('vista')
            self.style.configure('TNotebook', tabposition='n', padding=[10,0,10])
            self.style.configure('TNotebook.Tab', padding=5)
            self.style.configure('TButton', padding=5)
            self.style.configure('TEntry', padding=5)

        self.style.configure('Treeview', rowheight=30)


class BottomBar(ttk.Frame):
    # bottom bar widget

    def __init__(self, root, app):
        super().__init__(master=root)
        self.app = app
        self.root = root

        self.ui_button_start = ImageTk.PhotoImage(Image.open('src/images/ui_button_start.png').resize((16,16)))
        self.ui_button_stop = ImageTk.PhotoImage(Image.open('src/images/ui_button_stop.png').resize((16,16)))
        self.ui_button_log = ImageTk.PhotoImage(Image.open('src/images/ui_button_log.png').resize((16,16)))
        
        start_queue_button = ttk.Button(self, text='Start queue', image=self.ui_button_start, compound='left', command=self.confirm)
        stop_queue_button = ttk.Button(self, text='Stop queue', image=self.ui_button_stop, compound='left')
        show_log_button = ttk.Button(self, text='Show log', image=self.ui_button_log, compound='left')

        start_queue_button.pack(padx=10, pady=10, side='left', fill="none", expand=True)
        stop_queue_button.pack(padx=10, pady=10, side='left', fill="none", expand=True)
        show_log_button.pack(padx=10, pady=10, side='left', fill="none", expand=True)

        self.pack(fill='x', expand=False)

    def confirm(self):
        # asks user before continuing

        confirmation = messagebox.askokcancel(message="Are you sure you want to start the queue?")
        
        if confirmation:

            if self.app.transcode_queue:
                self.root.main.output_view.set_transcode_data()
                self.app.start_queue()
                self.bell()
            else:
                messagebox.showerror(message='No output format specified!')
        else:
            pass


class Tabs(ttk.Notebook):
    # instaces the widget for the main window tabs

    def __init__(self, root, app):
        super().__init__()

        self.input_view = InputView(app)
        self.output_view = encoder.OutputView(app)

        self.add(self.input_view, text='Import')
        self.add(self.output_view, text='Encoder')

        self.bind('<<NotebookTabChanged>>', lambda e: root.update_idletasks())

        # this is hacky
        self.bind('<<NotebookTabChanged>>', self.save_metadata)

        self.pack(expand=True, fill='both')

    def save_metadata(self, event):
        # hacky workaround for now to get metadata to stop a bug where the metadata doesnt get saved if you only have one track selected idk man

        e = self.input_view.editor

        e.tree.previous_selected_item = e.tree.current_selected_item
        e.set_data()



class InputView(ttk.Frame):
    # instances the input view frame

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.editor = editor.EditorWidget(self, app)

        self.pack(pady=50, padx=50)