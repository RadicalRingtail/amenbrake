import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('converter tool')
        self.geometry('800x600')
        
        self.mainloop()

        