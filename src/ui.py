import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from app import Application

class Window(tk.Tk):
    # instances ui, contains things related to the main window

    def __init__(self):
        super().__init__()
        self.app = Application()

        self.title('converter tool')
        self.geometry('800x600')

        self.create_menu()
        
        self.mainloop()
    
    def create_menu(self):
        menu = tk.Menu(self)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Open file(s)', command=lambda: self.app.input_files('file'))
        file_menu.add_command(label='Open folder', command=lambda: self.app.input_files('folder'))
        
        menu.add_cascade(label='File', menu=file_menu)

        self.configure(menu=menu)