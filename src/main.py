from shutil import which
from tkinter import messagebox
from ui import Window

if __name__ == '__main__':
    # check if theres a valid ffmpeg install present, if so, initialize the application

    if which('ffmpeg') is not None:
        Window()
    else:
        messagebox.showerror(title='Erorr', message='No ffmpeg installation found!', command=exit)

    