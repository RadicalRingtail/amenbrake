import tkinter as tk
from tkinter import ttk, filedialog
import platform

from support import Codecs, Samplerates, Bitrates, Quality, Encoders

# at this point i was so sick of ui programming that i basically was just fumbling through the code to get it working, this needs to be cleaned up

class OutputView(ttk.Frame):
    # instances the Output view frame

    def __init__(self, app):
        super().__init__(style='MainFrames.TFrame')
        self.app = app
        self.encoder_widgets = {}

        self.file_name = tk.StringVar()
        self.folder_name = tk.StringVar()
        self.parent_name = tk.StringVar()

        self.file_name.set(self.app.file_name_format)
        self.folder_name.set(self.app.sub_folder_name_format)
        self.parent_name.set(self.app.parent_folder_name_format)

        top_frame = ttk.Frame(self)

        ttk.Label(top_frame, text='Filename format').pack()
        ttk.Entry(top_frame, textvariable=self.file_name).pack(pady=(0,5))

        ttk.Label(top_frame, text='Folder name format').pack()
        ttk.Entry(top_frame, textvariable=self.folder_name).pack(pady=(0,5))

        ttk.Label(top_frame, text='Parent folder name format').pack()
        ttk.Entry(top_frame, textvariable=self.parent_name).pack(pady=(0,5))

        add_job_button = ttk.Button(top_frame, text='Add format..', command=self.create_encoder_options)
        add_job_button.pack()

        top_frame.pack()

        self.create_encoder_widget_canvas()

    def create_encoder_widget_canvas(self):
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas, width=1000)

        self.canvas.bind("<Configure>", self.canvas_resize)
        self.canvas.bind_all('<MouseWheel>', self.canvas_scroll)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.c_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def canvas_resize(self, event):
        self.canvas.itemconfig(self.c_window, width=event.width)

    def canvas_scroll(self, event):

        if platform.system() == 'Darwin':
            self.canvas.yview_scroll(-1 * event.delta, 'units')

    def create_encoder_options(self):
        job = self.app.add_transcode_job({})
        option = EncoderOptions(self.scroll_frame, self.app, job, self)

        self.encoder_widgets[job] = option
    
    def remove_widget(self, widget_id):
        del self.app.transcode_queue[widget_id]
        self.encoder_widgets[widget_id].destroy()
        del self.encoder_widgets[widget_id]

    def set_transcode_data(self):

        for key, item in self.encoder_widgets.items():

            job = self.app.transcode_queue[key]

            job.codec = item.codec.get()
            job.samplerate = item.samplerate.get()
            job.encoder = item.encoder.get()
            job.vbr = item.vbr.get()
            job.quality = item.quality.get()
            job.output_loc = item.output.get()
            job.parent_dir = item.parent_dir.get()
            job.zip_folder = item.zip_folder.get()

            print(job.__dict__)

        self.app.file_name_format = self.file_name.get()
        self.app.sub_folder_name_format = self.folder_name.get()
        self.app.parent_folder_name_format = self.parent_name.get()


class EncoderOptions(tk.Frame):
    # widget that gives you encoding options for a transcode job in queue

    def __init__(self, root, app, widget_id, master):
        super().__init__(master=root, bg='gainsboro')
        self.app = app
        self.width = 1000
        self.master = master
        self.widget_id = widget_id

        self.codec = tk.StringVar()
        self.samplerate = tk.StringVar()
        self.bitrate = tk.StringVar()
        self.output = tk.StringVar()
        self.encoder = tk.StringVar()
        self.vbr = tk.BooleanVar()
        self.quality = tk.StringVar()
        self.parent_dir = tk.BooleanVar()
        self.zip_folder = tk.BooleanVar()

        self.create_settings_widget()

        self.pack(fill='x', padx=(10,10), pady=(10,10))


    def create_settings_widget(self):
        # settings that exist in every instance of EncoderOptions regardless of codec specific settings

        codec_dropdown = ttk.OptionMenu(self, self.codec, 'Select a codec..', *Codecs.as_list())

        codec_dropdown.pack(expand=True, padx=(10,10), pady=(10,10))

        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(expand=True, fill='x', padx=(10,10), pady=(10,10))

        self.widgets = []

        self.codec.trace("w", self.get_format_type)

        ttk.Separator(self, orient='horizontal').pack(expand=True, fill='x', padx=(10,10),)

        self.output_widget()

        ttk.Button(self, text='Remove..', command=lambda: self.master.remove_widget(self.widget_id)).pack()


    def output_widget(self):
        # for selecting and viewing the output path

        frame = ttk.Frame(self)

        output_label = ttk.Label(frame, text='Output Location')
        output_entry = ttk.Entry(frame, textvariable=self.output)
        
        directory_button = ttk.Button(frame, text='Select', command=self.on_directory_button)

        parent_dir_check = ttk.Checkbutton(frame, text='Use parent folder for group', variable=self.parent_dir)
        zip_check = ttk.Checkbutton(frame, text='Zip folders', variable=self.zip_folder)

        output_label.pack()
        output_entry.pack(pady=12)
        directory_button.pack()
        parent_dir_check.pack()
        zip_check.pack()
        frame.pack(fill='x', expand=True, padx=(10,10), pady=(10,10))


    def on_directory_button(self):
        # opens filedialog for output_widget and sets the output directory string
        # fix no cover art causing error

        directory = filedialog.askdirectory(title='Select folder..')
        self.output.set(directory)

    def get_format_type(self, *args):

        for w in self.widgets:
            w.destroy()
        
        match self.codec.get():
            
            case 'mp3':
                self.widgets = [
                    ttk.Label(self.options_frame, text='Bitrate:'),
                    ttk.OptionMenu(self.options_frame, self.bitrate, Bitrates.as_list()[0], *Bitrates.as_list()),
                    ttk.Checkbutton(self.options_frame, text='VBR (Variable Birate)', onvalue=True, offvalue=False, variable=self.vbr),
                    ttk.OptionMenu(self.options_frame, self.quality, Quality.LAME.value[0], *Quality.LAME.value)
                ]
                self.encoder.set(Encoders.LIBMP3LAME.value)
            case 'flac':
                self.widgets = [
                    ttk.Label(self.options_frame, text='Compression:'),
                    ttk.OptionMenu(self.options_frame, self.quality, Quality.LAME.value[0], *Quality.FLAC.value)
                ]
                self.encoder.set(Encoders.FLAC.value)
            case 'wav':
                self.encoder.set(Encoders.PCM_16.value)
            case 'ogg':
                self.widgets = [
                    ttk.Label(self.options_frame, text='Bitrate:'),
                    ttk.OptionMenu(self.options_frame, self.bitrate, Bitrates.as_list()[0], *Bitrates.as_list()),
                    ttk.Checkbutton(self.options_frame, text='VBR (Variable Birate)', onvalue=True, offvalue=False, variable=self.vbr),
                    ttk.OptionMenu(self.options_frame, self.quality, Quality.LAME.value[0], *Quality.VORBIS.value)
                ]
                self.encoder.set(Encoders.VORBIS.value)
            case 'aiff':
                self.encoder.set(Encoders.PCM_16.value)
        self.widgets.insert(0, ttk.Label(self.options_frame, text='Samplerate:'))
        self.widgets.insert(1, ttk.OptionMenu(self.options_frame, self.samplerate, Samplerates.as_list()[0], *Samplerates.as_list()))

        for w in self.widgets:
            w.pack(pady=5)

