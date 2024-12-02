import pydub
import mutagen
from pydub import AudioSegment
from mutagen import File

def convert_mp3_to_wav(file_path): #converts to a .wav file
    audio = pydub.AudioSegment.from_mp3(file_path)
    wav_file_path = file_path.replace(".mp3", ".wav")
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def remove_metadata(file_path):
    """Removes metadata from the audio file."""
    #Loads the audio file using Mutagen
    audio = File(file_path, easy=True)

    if audio is not None:
        #Clearing metadata tags
        audio.delete()
        audio.save()

    if file_path.endswith('.wav'):
        audio_segment = AudioSegment.from_wav(file_path)
        audio_segment.export(file_path, format="wav")  #Overwrites original file without metadata

    print(f"Metadata removed from: {file_path}")