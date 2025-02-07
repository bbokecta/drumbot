import os
from gtts import gTTS
from playsound import playsound
from pydub.effects import speedup
from pydub import AudioSegment

def get_speech(answer):
    tts = gTTS(answer, lang='en', tld="com.ng")
    speech_file_path = os.path.join("voices/", "audio.mp3")
    tts.save(speech_file_path)

    sound = AudioSegment.from_file(speech_file_path)
    fast_audio = sound.speedup(1.4)
    fast_audio.export(speech_file_path, format="mp3")

    # subprocess.run(['ffmpeg', '-y' '-i', 'voices/initial_audio.mp3', '-filter:a', "atempo=5.0", 'voices/audio.mp3'])
    playsound(speech_file_path) #disable this when streaming to Omniverse
    os.remove(speech_file_path)