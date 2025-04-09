import tkinter as tk

class View:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.label = tk.Label(self.frame, text = "Bem vindo")
        self.label.pack()
        self.text_entry = tk.Entry(self.frame)
        self.text_entry.pack()