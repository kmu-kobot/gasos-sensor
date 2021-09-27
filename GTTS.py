# if you want to use Google TTS, you must try this
# pip install gTTS
# pip install pygame
# pip install pydub

from gtts import gTTS
import pygame

def tts(text):
    tts_kr = gTTS(text=text, lang='ko')

    f = open("/home/pi/GASOS/tempFile.mp3", 'wb')
    tts_kr.write_to_fp(f)
    f.close()
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/GASOS/tempFile.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    

if __name__ == "__main__":
    text = "가스가 새고 있습니다."
    tts(text)
