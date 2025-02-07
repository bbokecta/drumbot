import os
from gtts import gTTS
from playsound import playsound

def get_speech(answer):
    tts = gTTS(answer, lang='en', tld="com.ng")
    speech_file_path = os.path.join("voices/", "audio.mp3")
    tts.save(speech_file_path)

    # subprocess.run(['ffmpeg', '-y' '-i', 'voices/initial_audio.mp3', '-filter:a', "atempo=5.0", 'voices/audio.mp3'])
    playsound(speech_file_path) #disable this when streaming to Omniverse
    os.remove(speech_file_path)