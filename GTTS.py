# if you want to use Google TTS, you must try this
# pip install gTTS
# pip install playsound
# pip install pydub

from gtts import gTTS
from playsound import playsound

def tts(text):
    tts_kr = gTTS(text=text, lang='ko')

    f = open("tempFile.mp3", 'wb')
    tts_kr.write_to_fp(f)
    f.close()

    playsound("tempFile.mp3")

    

if __name__ == "__main__":
    text = "가스가 새고 있습니다."
    tts(text)