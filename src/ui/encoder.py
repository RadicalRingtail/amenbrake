import tkinter as tk
from tkinter import ttk, filedialog

from support import Codecs, Samplerates

class EncoderOptions(tk.Frame):
    # widget that gives you encoding options for a transcode job in queue

    def __init__(self, root, app):
        super().__init__(master=root, bg='gainsboro')
        self.app = app

        self.codec = tk.StringVar()
        self.samplerate = tk.StringVar()
        self.output = tk.StringVar()
        
        self.common_settings()
        self.output_widget()

        self.pack(fill='x', padx=(10,10), pady=(10,10))


    def common_settings(self):
        # settings that exist in every instance of EncoderOptions regardless of codec specific settings

        codec_dropdown = ttk.Combobox(self, textvariable=self.codec, values=Codecs.as_list(), state='readonly')
        codec_dropdown.current(0)

        samplerate_dropdown = ttk.Combobox(self, textvariable=self.samplerate, values=Samplerates.as_list())
        samplerate_dropdown.current(0)

        codec_dropdown.pack(expand=True, padx=(10,10), pady=(10,10))
        samplerate_dropdown.pack(expand=True, padx=(10,10), pady=(10,10))


    def output_widget(self):
        # for selecting and viewing the output path

        frame = ttk.Frame(self)

        output_label = ttk.Label(frame, text='Output Location')
        output_entry = ttk.Entry(frame, textvariable=self.output)
        
        directory_button = ttk.Button(frame, text='Select', command=self.on_directory_button)

        output_label.pack()
        output_entry.pack(pady=12)
        directory_button.pack()
        frame.pack(fill='x', padx=(10,10), pady=(10,10))


    def on_directory_button(self):
        # opens filedialog for output_widget and sets the output directory string

        directory = filedialog.askdirectory(title='Select folder..')
        self.output.set(directory)

    def get_combobox_value(self):
        pass
