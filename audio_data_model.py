import librosa
import numpy as np
import soundfile as sf
import scipy.signal as signal
from pydub import AudioSegment

class AudioDataModel: #Class for the audio data model.
    def __init__(self):
        self.audio_file = None
        self.sample_rate = None
        self.audio_data = None
        self.duration = None
        self.RT60_values = {'low': None, 'mid': None, 'high': None} #values of the RT60.
    
    def load_audio(self, file_path): #Code to load audio file.
        self.audio_file = file_path
        self.audio_data, self.sample_rate = librosa.load(file_path, sr=None, mono=True)
        self.duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)
    
    def compute_RT60(self):
        self.RT60_values['low'] = 0.5 
        self.RT60_values['mid'] = 0.4  
        self.RT60_values['high'] = 0.3  
    
    def get_waveform(self): #gets the waveform values.
        return self.audio_data
    
    def get_RTs(self): #obtains the values of the RT60.
        return self.RT60_values

    def convert_to_wav(self, output_file=None):
        if not self.audio_file:
            raise ValueError("No audio file loaded. Please load an audio file first.")

    # If no output path is provided, create one by changing the file extension to '.wav'
        if output_file is None:
            #(this assumes only one period in the filename)
            output_file = self.audio_file.rsplit('.', 1)[0] + '.wav'

        try:
            audio = AudioSegment.from_file(self.audio_file)  # Load the audio using pydub
            audio.export(output_file, format="wav")
            print(f"File successfully converted to {output_file}")
        except Exception as e:
            print(f"Error during conversion: {e}")
