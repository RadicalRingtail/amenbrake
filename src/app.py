from tkinter import filedialog
from support import FILEDIALOG_SUPPORTED_FILES

class Application():
    # instances the application, contains application functions

    def __init__(self):
        self.file_list = None

    def input_files(self, type):
        filedialog_raw = None
        files = None

        if type == 'file':
            filedialog_raw = filedialog.askopenfiles(title='Open file(s)', initialdir='/', filetypes=FILEDIALOG_SUPPORTED_FILES())
        elif type == 'folder':
            filedialog_raw = filedialog.askdirectory(title='Open folder', initialdir='/')

        self.file_list = filedialog_raw
        print(self.file_list)