import numpy as np
import librosa
import scipy.signal as signal
import matplotlib.pyplot as plt
from pydub import AudioSegment
import os

class AudioDataModel:
    def __init__(self):
        self.audio_data = None
        self.sampling_rate = None
        self.length = 0
        self.waveform = None
        self.rt60 = {'low': None, 'mid': None, 'high': None}
        self.resonant_frequency = None

    def load_audio(self, filepath):
        if not filepath.lower().endswith('.wav'):
            filepath = self.convert_to_wav(filepath)
        
        self.audio_data, self.sampling_rate = librosa.load(filepath, sr=None)
        self.length = librosa.get_duration(y=self.audio_data, sr=self.sampling_rate)
        self.waveform = self.audio_data

    def convert_to_wav(self, filepath):
        audio = AudioSegment.from_file(filepath)
        wav_filepath = "temp_audio.wav"
        audio.export(wav_filepath, format="wav")
        return wav_filepath

    def get_resonant_frequency(self):
        freq_data = np.fft.fft(self.audio_data)
        freqs = np.fft.fftfreq(len(self.audio_data), 1/self.sampling_rate)
        abs_freq_data = np.abs(freq_data)
        peak_freq_index = np.argmax(abs_freq_data)
        self.resonant_frequency = abs(freqs[peak_freq_index])
        return self.resonant_frequency

    def compute_rt60(self, frequency_range='low'):
        if frequency_range == 'low':
            data_range = self.audio_data[:int(len(self.audio_data)/3)]
        elif frequency_range == 'mid':
            data_range = self.audio_data[int(len(self.audio_data)/3):int(len(self.audio_data)*2/3)]
        elif frequency_range == 'high':
            data_range = self.audio_data[int(len(self.audio_data)*2/3):]

        decay = np.abs(data_range)  
        time = np.linspace(0, len(data_range)/self.sampling_rate, len(data_range))  
        decay_log = np.log(decay + 1e-5) 
        slope, _ = np.polyfit(time[:len(time)//2], decay_log[:len(time)//2], 1)
        rt60 = -60 / slope 
        self.rt60[frequency_range] = rt60
        return rt60
