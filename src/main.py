from shutil import which
from ui import Application
from tkinter import messagebox

if __name__ == '__main__':
    # check if theres a valid ffmpeg install present, if so, initialize the application

    if which('ffmpeg') is not None:
        Application()
    else:
        messagebox.showerror(title='Erorr', message='No ffmpeg installation found!', command=exit)
