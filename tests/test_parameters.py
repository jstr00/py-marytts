from marytts import MaryTTS
import subprocess
import platform
import tempfile
import os

marytts = MaryTTS()

text_to_speak = "Some sample text"


wav_audio = marytts.synth_wav(text_to_speak, whisper_effect=True)


with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
    temp_wav_filename = temp_wav_file.name
    temp_wav_file.write(wav_audio)

system = platform.system().lower()

if system == 'linux':
    subprocess.run(['aplay', temp_wav_filename])
else:
    print("OS currently not supported")

os.remove(temp_wav_filename)