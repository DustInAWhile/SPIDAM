import librosa
import numpy as np
import os
import soundfile as sf
from scipy.signal import butter, lfilter

class AudioDataModel: #initializing class
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.audio_file = None

    def load_audio(self, file_path): #loads the given audio file
        if not file_path.endswith('.wav'): #checks if it is .wav and converts it if not, converts them
            file_path = self.convert_to_wav(file_path)

        # Load the audio file
        self.audio_data, self.sample_rate = librosa.load(file_path, sr=None, mono=True)
        self.audio_file = file_path

    def convert_to_wav(self, file_path):
        """Converts an audio file to wav format if it's not already."""
        output_file = file_path.replace(file_path.split('.')[-1], 'wav')
        os.system(f"ffmpeg -i {file_path} {output_file}")
        return output_file

    def bandpass_filter(self, data, lowcut, highcut):
        """Applies a bandpass filter to the audio data."""
        nyquist = 0.5 * self.sample_rate
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(4, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

    def compute_rt60(self, frequency_range):
        """Calculates the RT60 for low, mid, and high frequency ranges."""
        if frequency_range == 'low':
            band = (20, 250)  # Low frequencies
        elif frequency_range == 'mid':
            band = (250, 2000)  # Mid frequencies
        elif frequency_range == 'high':
            band = (2000, 20000)  # High frequencies
        else:
            raise ValueError("Invalid frequency range specified. Choose 'low', 'mid', or 'high'.")

        # Apply the bandpass filter to the audio data
        filtered_audio = self.bandpass_filter(self.audio_data, band[0], band[1])

        # Estimate RT60 for the filtered audio
        rt60 = self.estimate_rt60(filtered_audio)
        return rt60

    def estimate_rt60(self, audio_signal):
        """Estimate RT60 by calculating the decay rate of the energy over time."""
        # Compute the signal's energy over time
        energy = np.square(audio_signal)
        energy_db = 10 * np.log10(energy + np.finfo(float).eps)  # Convert to decibels

        start_idx = np.argmax(energy_db > -40)  
        if start_idx == 0:
            return 0  

        # Find the time when the energy has decayed by 60 dB
        end_idx = np.argmax(energy_db[start_idx:] < (energy_db[start_idx] - 60))
        if end_idx == 0:
            return 0 


        decay_time = (end_idx + start_idx) / self.sample_rate
        return decay_time

    def get_resonant_frequency(self): #Obtains the resonant frequency value
        spectrum = np.abs(np.fft.fft(self.audio_data))
        freqs = np.fft.fftfreq(len(spectrum))
        resonant_freq = np.abs(freqs[np.argmax(spectrum)])
        return resonant_freq

    def get_audio_length(self): #Obtains length of the audio file
        return len(self.audio_data) / self.sample_rate

    def get_max_amplitude(self): #Obtains max amplitude
        """Returns the maximum amplitude in the audio data."""
        return np.max(np.abs(self.audio_data))

    def get_spectrogram(self): #obtains spectrogram
        """Returns a spectrogram of the audio."""
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.audio_data)), ref=np.max)
        return D
