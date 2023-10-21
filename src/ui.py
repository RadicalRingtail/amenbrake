import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from support import SUPPORTED_FILES

class Application(tk.Tk):
    # instances ui and application, contains ui logic and things related to the main window

    def __init__(self):
        super().__init__()
        self.title('converter tool')
        self.geometry('800x600')

        self.create_menu()
        
        self.mainloop()
    
    def create_menu(self):
        menu = tk.Menu(self)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Open file', command=lambda: self.input_files('file'))
        file_menu.add_command(label='Open folder', command=lambda: self.input_files('folder'))
        
        menu.add_cascade(label='File', menu=file_menu)

        self.configure(menu=menu)

    def input_files(self, type):
        filedialog_raw = None
        files = None

        if type == 'file':
            filedialog_raw = filedialog.askopenfiles(title='Open file(s)', initialdir='/', filetypes=FILEDIALOG_SUPPORTED_FILES())
        elif type == 'folder':
            filedialog_raw = filedialog.askdirectory(title='Open folder', initialdir='/')