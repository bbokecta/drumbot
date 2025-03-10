import os
from gtts import gTTS
from playsound import playsound
from pydub.effects import speedup
from pydub import AudioSegment

import soundfile as sf
import pyrubberband as pyrb

def get_speech(answer):
    tts = gTTS(answer, lang='en', tld="com.ng")
    speech_file_path = os.path.join("voices/", "audio.wav")
    lowspeech_file_path = os.path.join("voices/", "low_audio.wav")
    tts.save(speech_file_path)

    # y, sr = sf.read(speech_file_path)
    # y_stretch = pyrb.time_stretch(y, sr, 1.5)
    # sf.write(speech_file_path, y_stretch, sr, format="mp3")

    sound = AudioSegment.from_file(speech_file_path)
    # sound.export(speech_file_path, format="mp3")
    
    
    octaves = -0.75
    # for octaves in np.linspace(-1,1,21):
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    hipitch_sound = sound._spawn(sound.raw_data, overrides=
                                    {'frame_rate': new_sample_rate})
    hipitch_sound = hipitch_sound.set_frame_rate(44100)
    hipitch_sound.export(lowspeech_file_path, format="wav")

    # playsound(lowspeech_file_path) #disable this when streaming to Omniverse
    # os.remove(lowspeech_file_path)