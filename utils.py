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
    """Remove metadata from the audio file."""
    # Load the audio file using Mutagen
    audio = File(file_path, easy=True)

    if audio is not None:
        # Clear all metadata tags
        audio.delete()
        audio.save()

    # If it's a WAV file, we can also just re-save the audio without metadata
    if file_path.endswith('.wav'):
        # Re-load the audio using pydub to save it again without metadata
        audio_segment = AudioSegment.from_wav(file_path)
        audio_segment.export(file_path, format="wav")  # This will overwrite the original file without metadata

    print(f"Metadata removed from: {file_path}")