from gtts import gTTS
from playsound import playsound
from time import ctime
import speech_recognition as sr
import os
import time
import webbrowser
import datetime
import pyjokes
import camelcase

r = sr.Recognizer()
c = camelcase.CamelCase()
#This method capitalizes the first letter of each word.
def speak(audio):
    voice = gTTS(text=audio, lang='en', lang_check=False, slow=False)
    voice.save("command.wav")
    os.system("command.wav")
    
def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>=0 and hour<12:
		speak("Good Morning Sir !")
	elif hour>=12 and hour<16:
		speak("Good Afternoon Sir !")
	else:
		speak("Good Evening Sir !")

def wakeUp():   
    with sr.Microphone() as source:
        while(True):
            audio=r.listen(source)
            try:
                voice_data=r.recognize_google(audio)
                if 'FRIDAY' in voice_data.upper():      
                    print('Hi')  
                    wishMe()
                    time.sleep(1.8)
                    break
            except sr.RequestError:
                print("Sorry, but you are offline right now")  
                exit()                
            except:
                continue   
wakeUp()

def voice_analyzer(ask = False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            voice_data=c.hump(voice_data)
        except sr.UnknownValueError:
            speak("You will have to speak more clearly" )
        except:
            print("Sorry but you are offline right now")
        time.sleep(1)        
        return voice_data
        
def usrname(change):
    if os.path.isfile('username.txt') and os.path.getsize('username.txt') != 0:
        file = open('username.txt')
        myname = file.read()
        speak("Welcome Mister{}".format(myname))
        print('Welcome Mr/Mrs. {}'.format(myname))
    if change:
        speak("What should I call you sir?")
        time.sleep(1.5)
        myname = voice_analyzer()
        file = open('username.txt','w')
        file.write(myname)
        speak("Welcome Mister{}".format(myname))
        print('Welcome Mr/Mrs. {}'.format(myname))
        time.sleep(2)

def respond(voice_data):
    if 'what time' in voice_data:
        speak(ctime())

    if 'search' in voice_data:
        speak("what do you want to search for")
        time.sleep(1)
        search = voice_analyzer()       
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)

    if 'find location' in voice_data:
        speak("Ok which location?")
        time.sleep(1)
        location = voice_analyzer()      
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url) 

    if 'joke' in voice_data:
        speak(pyjokes.get_joke()) 
        time.sleep(5)
        
    if 'Change Username' in voice_data:
        change=True
        usrname(change) 

    if "don't listen" in voice_data or "pause" in voice_data:
        wakeUp()

    if 'exit' in voice_data or 'close' in voice_data:
        exit()

usrname(False)
speak('How can I help you')
while 1:
    time.sleep(1.5)
    voice_data = voice_analyzer()
    print('--{}'.format(voice_data))
    respond(voice_data)

