class AudioController: #initializes the class
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_audio(self, file_path): #loads the audio file provided
        self.model.load_audio(file_path)
        self.view.plot_waveform()
        self.process_audio()

    def process_audio(self):
        # Calculate RT60 values for low, mid, and high frequencies
        rt60_low = self.model.compute_rt60('low')
        rt60_mid = self.model.compute_rt60('mid')
        rt60_high = self.model.compute_rt60('high')

        # Get additional audio data
        max_amplitude = self.model.get_max_amplitude()
        audio_length = self.model.get_audio_length()

        # Update the view with RT60 values and other audio data
        rt60_values = {'low': rt60_low, 'mid': rt60_mid, 'high': rt60_high}
        self.view.update_summary_box(
            file_name=self.model.audio_file,
            duration=audio_length,
            max_amplitude=max_amplitude,
            rt60_values=rt60_values
        )