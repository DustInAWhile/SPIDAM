from utils import remove_metadata


class AudioController: #Intializes the audio controller class
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_audio(self, file_path):
        #Removes metadata from the file
        remove_metadata(file_path)

        #Load the audio into the model after removing metadata
        self.model.load_audio(file_path)
        self.view.plot_waveform()
        self.process_audio()

    def process_audio(self):
        #Calculates RT60 values for various frequencies
        rt60_low = self.model.compute_rt60('low')
        rt60_mid = self.model.compute_rt60('mid')
        rt60_high = self.model.compute_rt60('high')

        target_rt60 = 0.5  #RT60 value in seconds

        #Calculate the difference in RT60 values
        diff_low = rt60_low - target_rt60
        diff_mid = rt60_mid - target_rt60
        diff_high = rt60_high - target_rt60

        #Display the results 
        print(f"Current RT60 (Low): {rt60_low:.2f} seconds, Difference to 0.5s: {diff_low:.2f} seconds")
        print(f"Current RT60 (Mid): {rt60_mid:.2f} seconds, Difference to 0.5s: {diff_mid:.2f} seconds")
        print(f"Current RT60 (High): {rt60_high:.2f} seconds, Difference to 0.5s: {diff_high:.2f} seconds")

        #Update the view with RT60 values and other audio data
        rt60_values = {'low': rt60_low, 'mid': rt60_mid, 'high': rt60_high}
        self.view.update_summary_box(
            file_name=self.model.audio_file,
            duration=self.model.get_audio_length(),
            max_amplitude=self.model.get_max_amplitude(),
            rt60_values=rt60_values
        )

        self.view.update_rt60_diff(diff_low, diff_mid, diff_high)