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
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.create_menu()
        self.create_layout()
        
        self.mainloop()


    def on_close(self):
        self.app.exit()
    

    def create_menu(self):
        menu = tk.Menu(self)

        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Open file(s)', command=lambda: self.app.import_files('file'))
        file_menu.add_command(label='Open folder', command=lambda: self.app.import_files('folder'))
        
        menu.add_cascade(label='File', menu=file_menu)

        self.configure(menu=menu)


    def create_layout(self):
        Tabs(self)


class Tabs(ttk.Notebook):
    # instaces the widget for the main window tabs

    def __init__(self, root):
        super().__init__()
        self.add(InputView(), text='Input')
        self.add(OutputView(), text='Output')

        self.pack()


class InputView(tk.Frame):
    # instances the input view frame

    def __init__(self):
        super().__init__()
        self.pack()


class OutputView(tk.Frame):
    # instances the Output view frame

    def __init__(self):
        super().__init__()
        self.pack()