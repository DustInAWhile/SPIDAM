import pydub

def convert_mp3_to_wav(file_path): #converts to a .wav file
    audio = pydub.AudioSegment.from_mp3(file_path)
    wav_file_path = file_path.replace(".mp3", ".wav")
    audio.export(wav_file_path, format="wav")
    return wav_file_path
