import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class AudioDataView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Set up the load button
        self.load_button = tk.Button(root, text="Load Audio", command=self.load_audio)
        self.load_button.grid(row=0, column=0, padx=10, pady=10)

        # Set up the plot button to cycle through plots
        self.plot_button = tk.Button(root, text="Next Plot", command=self.next_plot)
        self.plot_button.grid(row=0, column=1, padx=10, pady=10)

        # Add the new button for combining RT60 graphs
        self.combine_rt60_button = tk.Button(root, text="Combine RT60 Graphs", command=self.combine_rt60)
        self.combine_rt60_button.grid(row=0, column=2, padx=10, pady=10)

        self.summary_label = tk.Label(root, text="Audio Summary")
        self.summary_label.grid(row=1, column=0, columnspan=2)

        # Creating a frame for summary information below the graphs
        self.summary_box = tk.LabelFrame(root, text="Audio File Summary", padx=10, pady=10)
        self.summary_box.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")

        # Labels inside the summary box
        self.file_name_label = tk.Label(self.summary_box, text="File: Not Loaded")
        self.file_name_label.grid(row=0, column=0, sticky="w")

        self.duration_label = tk.Label(self.summary_box, text="Duration: Not Loaded")
        self.duration_label.grid(row=1, column=0, sticky="w")

        self.max_amplitude_label = tk.Label(self.summary_box, text="Max Amplitude: Not Loaded")
        self.max_amplitude_label.grid(row=2, column=0, sticky="w")

        self.rt60_label = tk.Label(self.summary_box, text="RT60 Low: Not Loaded")
        self.rt60_label.grid(row=3, column=0, sticky="w")

        # Create a frame for displaying plots
        self.plot_frame = tk.Frame(root)
        self.plot_frame.grid(row=3, column=0, columnspan=2)

        # Initialize the plot
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = None

        # Plot counter to cycle through different plots
        self.plot_counter = 0

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
        self.controller.load_audio(file_path)

    def next_plot(self):
        """Cycle through different plots."""
        if self.controller.model.audio_data is not None:
            if self.plot_counter == 0:
                self.plot_waveform()
            elif self.plot_counter == 1:
                self.plot_spectrogram()
            elif self.plot_counter == 2:
                self.plot_resonant_frequency_spectrum()
            elif self.plot_counter == 3:
                self.plot_rt60()
            elif self.plot_counter == 4:
                self.plot_combined_rt60()
            elif self.plot_counter == 5:
                self.plot_amplitude_envelope()

            self.plot_counter = (self.plot_counter + 1) % 6  # Code to cycle back to the beginning of the plots

    def plot_waveform(self):
        """Plot the audio waveform."""
        self.ax.cla()  # Clear the axis
        self.ax.plot(self.controller.model.audio_data)
        self.ax.set_title("Audio Waveform")
        self.ax.set_xlabel("Time (samples)")
        self.ax.set_ylabel("Amplitude")
        self.display_plot()

    def plot_spectrogram(self):
        """Plot the spectrogram."""
        spectrogram = self.controller.model.get_spectrogram()
        self.ax.cla()  # Clear the axis
        self.ax.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')
        self.ax.set_title("Spectrogram")
        self.ax.set_ylabel("Frequency bins")
        self.ax.set_xlabel("Time frames")
        self.display_plot()

    def plot_resonant_frequency_spectrum(self):
        """Plot the resonant frequency spectrum (FFT)."""
        if len(self.controller.model.audio_data) > 1:  # Ensure audio data is not empty
            spectrum = np.abs(np.fft.fft(self.controller.model.audio_data))
            self.ax.cla()  # Clear the axis
            self.ax.plot(np.fft.fftfreq(len(spectrum)), spectrum)
            self.ax.set_title("Resonant Frequency Spectrum")
            self.ax.set_xlabel("Frequency (Hz)")
            self.ax.set_ylabel("Amplitude")
        else:
            self.ax.cla()  # Clear the axis
            self.ax.text(0.5, 0.5, "Insufficient Data for FFT", ha='center', va='center')
            self.ax.set_title("Resonant Frequency Spectrum")
        self.display_plot()

    def plot_rt60(self):
        """Plot the RT60 values for different frequency ranges."""
        rt60_low = self.controller.model.compute_rt60('low')
        rt60_mid = self.controller.model.compute_rt60('mid')
        rt60_high = self.controller.model.compute_rt60('high')

        self.ax.cla()  # Clear the axis
        self.ax.bar(['Low', 'Mid', 'High'], [rt60_low, rt60_mid, rt60_high])
        self.ax.set_title("RT60 Values")
        self.ax.set_ylabel("RT60 (sec)")
        self.display_plot()

    def plot_combined_rt60(self): #Shows the three RT60 plots in one graph
        """Plot the combined RT60 values in a single graph."""
        rt60_low = self.controller.model.compute_rt60('low')
        rt60_mid = self.controller.model.compute_rt60('mid')
        rt60_high = self.controller.model.compute_rt60('high')

        # Combine RT60 values into one bar plot
        self.ax.cla()  # Clear the axis
        self.ax.bar(['Low', 'Mid', 'High'], [rt60_low, rt60_mid, rt60_high])
        self.ax.set_title("Combined RT60 Values")
        self.ax.set_ylabel("RT60 (sec)")
        self.display_plot()

    def plot_amplitude_envelope(self):
        """Plot the amplitude envelope of the audio signal."""
        # Calculate the envelope by taking the absolute value of the audio signal
        envelope = np.abs(self.controller.model.audio_data)
        self.ax.cla()  # Clear the axis
        self.ax.plot(envelope)
        self.ax.set_title("Amplitude Envelope")
        self.ax.set_xlabel("Time (samples)")
        self.ax.set_ylabel("Amplitude")
        self.display_plot() 

    def display_plot(self):
        """Display the plot on the Tkinter window."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def update_summary_box(self, file_name, duration, max_amplitude, rt60_values): # summary box to display values
        """Update the summary box with audio details."""
        self.file_name_label.config(text=f"File: {file_name}")
        self.duration_label.config(text=f"Duration: {duration:.2f} seconds")
        self.max_amplitude_label.config(text=f"Max Amplitude: {max_amplitude:.2f}")
        self.rt60_label.config(
            text=f"RT60 Low: {rt60_values['low']:.2f}, Mid: {rt60_values['mid']:.2f}, High: {rt60_values['high']:.2f}")

    def combine_rt60(self):
        """Combine RT60 values for low, mid, and high frequencies into one plot."""
        rt60_low = self.controller.model.compute_rt60('low')
        rt60_mid = self.controller.model.compute_rt60('mid')
        rt60_high = self.controller.model.compute_rt60('high')

        # Plot the combined RT60 values in a single graph
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(['Low', 'Mid', 'High'], [rt60_low, rt60_mid, rt60_high])
        ax.set_title("Combined RT60 Values")
        ax.set_ylabel("RT60 (sec)")

        # Display the combined RT60 plot
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)
