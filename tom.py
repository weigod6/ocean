# pyttsx3
# import pyttsx3
# pyttsx3.speak("Hello World")

# # gTTS
# pip install gTTS
from gtts import gTTS
tts = gTTS('你好',lang='zh-tw')
tts.save('hello.mp3')
#
# # IBM Watson TTS
# pip install tts-watson
# from tts_watson.TtsWatson import TtsWatson
# ttsWatson = TtsWatson('watson_user', 'watson_password', 'en-US_AllisonVoice') ttsWatson.play("Hello World")
#
# # win32com（Windows 平台）
# import win32com.client as wincl
# speak = wincl.Dispatch("SAPI.SpVoice")
# speak.Speak("Hello World")
