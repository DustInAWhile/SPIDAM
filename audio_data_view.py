import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

class AudioDataView:
    def __init__(self, master, controller):
        self.master = master
        self.master.title("Audio Data Analysis and Modeling Platform")
        self.controller = controller
        
        #Button to load the audio file
        self.load_button = tk.Button(master, text="Load Audio File", command=self.load_file)
        self.load_button.pack()
        
        #Shows the loaded file
        self.file_label = tk.Labelud(master, text="No file loaded")
        self.file_label.pack()

        #Displays the waveform file
        self.show_waveform_button = tk.Button(master, text="Show Waveform", command=self.show_waveform)
        self.show_waveform_button.pack()

        #Displays the RT60 file.
        self.show_RT60_button = tk.Button(master, text="Show RT60", command=self.show_RT60)
        self.show_RT60_button.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if file_path:
            self.controller.load_audio(file_path)
            self.file_label.config(text=f"Loaded: {file_path}")

    def show_waveform(self): #Plots the wavefrm
        waveform = self.controller.get_waveform()
        plt.plot(waveform)
        plt.title("Waveform")
        plt.show()

    def show_RT60(self): #Plots the RT60 values
        RT60_values = self.controller.get_RT60()
        plt.bar(RT60_values.keys(), RT60_values.values())
        plt.title("RT60 for Frequency Ranges")
        plt.show()