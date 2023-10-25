from shutil import which
from tkinter import messagebox
import os, argparse, cProfile, pstats
from datetime import datetime

from ui import Window

# command line args
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    # initialize application

    if which('ffmpeg') is not None:

        if args.debug:
            if os.path.exists('debug'):
                pass
            else:
                os.mkdir('debug')

            dump_folder = os.path.join('debug', datetime.today().strftime("%d-%m-%y"))

            if os.path.exists(dump_folder):
                pass
            else:
                os.mkdir(dump_folder)

            debug_output = os.path.join(dump_folder, datetime.now().strftime("%d-%m-%y-%H-%M-%S.prof"))

            profiler = cProfile.run('Window()', debug_output)
            p = pstats.Stats(debug_output).sort_stats('cumtime')
            p.print_stats(20)
        else:
            Window()
    else:
        messagebox.showerror(title='Erorr', message='No ffmpeg installation found!')