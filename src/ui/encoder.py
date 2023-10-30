import tkinter as tk
from tkinter import ttk, filedialog

from support import Codecs, Samplerates, Quality

# at this point i was so sick of ui programming that i basically was just fumbling through the code to get it working, this needs to be cleaned up

class OutputView(ttk.Frame):
    # instances the Output view frame

    def __init__(self, app):
        super().__init__(style='MainFrames.TFrame')
        self.app = app
        self.encoder_widgets = {}

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=self.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)

        add_job_button = ttk.Button(self, text='Add format..', command=self.create_encoder_options)
        add_job_button.pack()

        add_job_button = ttk.Button(self, text='Set data', command=self.set_transcode_data)
        add_job_button.pack()

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.pack(fill="both", expand=True)
        


    def create_encoder_options(self):
        option = EncoderOptions(self.scroll_frame, self.app)
        job = self.app.add_transcode_job({})

        self.encoder_widgets[job] = option
        print(self.encoder_widgets)

    def set_transcode_data(self):

        for key, item in self.encoder_widgets.items():

            job = self.app.transcode_queue[key]

            job.codec = item.codec.get()
            job.samplerate = item.samplerate.get()
            job.encoder = item.encoder.get()
            job.vbr = item.vbr.get()
            job.quality = item.quality.get()
            job.output_loc = item.output.get()

            print(job.__dict__)


class EncoderOptions(tk.Frame):
    # widget that gives you encoding options for a transcode job in queue

    def __init__(self, root, app):
        super().__init__(master=root, bg='gainsboro')
        self.app = app

        self.codec = tk.StringVar()
        self.samplerate = tk.StringVar()
        self.output = tk.StringVar()
        self.encoder = tk.StringVar()
        self.vbr = tk.BooleanVar()
        self.quality = tk.StringVar()

        self.create_settings_widget()

        self.pack(fill='x', padx=(10,10), pady=(10,10))


    def create_settings_widget(self):
        # settings that exist in every instance of EncoderOptions regardless of codec specific settings

        codec_dropdown = ttk.OptionMenu(self, self.codec, 'Select a codec..', *Codecs.as_list())

        codec_dropdown.pack(expand=True, padx=(10,10), pady=(10,10))

        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(expand=True)

        self.widgets = []

        self.codec.trace("w", self.get_format_type)

        self.output_widget()


    def output_widget(self):
        # for selecting and viewing the output path

        frame = ttk.Frame(self)

        output_label = ttk.Label(frame, text='Output Location')
        output_entry = ttk.Entry(frame, textvariable=self.output)
        
        directory_button = ttk.Button(frame, text='Select', command=self.on_directory_button)

        output_label.pack()
        output_entry.pack(pady=12)
        directory_button.pack()
        frame.pack(fill='x', expand=True, padx=(10,10), pady=(10,10))


    def on_directory_button(self):
        # opens filedialog for output_widget and sets the output directory string

        directory = filedialog.askdirectory(title='Select folder..')
        self.output.set(directory)

    def get_format_type(self, *args):

        for w in self.widgets:
            w.destroy()
        
        match self.codec.get():
            
            case 'mp3':
                self.widgets = [
                    ttk.OptionMenu(self.options_frame, self.samplerate, Samplerates.as_list()[0], *Samplerates.as_list()),
                    ttk.Checkbutton(self.options_frame, text='VBR (Variable Birate)', onvalue=True, offvalue=False, variable=self.vbr),
                    ttk.OptionMenu(self.options_frame, self.quality, Quality.LAME.value[0], *Quality.LAME.value)
                ]
            case 'flac':
                self.widgets = [
                    ttk.OptionMenu(self.options_frame, self.samplerate, Samplerates.as_list()[0], *Samplerates.as_list()),
                    ttk.OptionMenu(self.options_frame, self.quality, Quality.LAME.value[0], *Quality.FLAC.value)
                ]
            case 'wav':
                self.widgets = [
                    ttk.OptionMenu(self.options_frame, self.samplerate, Samplerates.as_list()[0], *Samplerates.as_list())
                ]
            case 'ogg':
                self.widgets = [
                    ttk.OptionMenu(self.options_frame, self.samplerate, Samplerates.as_list()[0], *Samplerates.as_list()),
                    ttk.Checkbutton(self.options_frame, text='VBR (Variable Birate)', onvalue=True, offvalue=False, variable=self.vbr),
                    ttk.OptionMenu(self.options_frame, self.quality, Quality.LAME.value[0], *Quality.VORBIS.value)
                ]
            case 'aiff':
                self.widgets = [
                    ttk.OptionMenu(self.options_frame, self.samplerate, Samplerates.as_list()[0], *Samplerates.as_list())
                ]

        for w in self.widgets:
            w.pack()

