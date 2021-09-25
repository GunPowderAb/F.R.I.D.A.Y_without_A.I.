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
c = camelcase.CamelCase() # This method capitalizes the first letter of each word.

def speak(audio):
    # convert the text to speech using the GoogleTTS API
    voice = gTTS(text=audio, lang='en', lang_check=False, slow=False)
    # saves the speech to a file
    voice.save("command.wav")
    # plays the audio speech file
    os.system("command.wav")

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
	speak("Good Morning Sir !")
	
    elif hour>=12 and hour<16:
	speak("Good Afternoon Sir !")
	
    else:
	speak("Good Evening Sir !")
    	
# the program will not listen to anything unless it is activated with a wake word
# it will only start responding after we call or wish it 'Friday'
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
            voice_data=c.hump(voice_data) # capitalises the first letter
        except sr.UnknownValueError:
            speak("You will have to speak more clearly" )
        except:
            print("Sorry but you are offline right now")
        time.sleep(1)        
        return voice_data
        
def usrname(change):
    if os.path.isfile('username.txt') and os.path.getsize('username.txt') != 0:
	#checks if the file exists and if it is empty or not
        file = open('username.txt')
        myname = file.read()
	#calls you by the default username that was previously stored in the file
        speak("Welcome Mister{}".format(myname))
        print('Welcome Mr/Mrs. {}'.format(myname))
    if change:
	#if the file was empty or if a request was made to change the name
        speak("What should I call you sir?")
        time.sleep(1.5)
        myname = voice_analyzer()
        file = open('username.txt','w')
        file.write(myname)
	#saves the username to the file
        speak("Welcome Mister{}".format(myname))
        print('Welcome Mr/Mrs. {}'.format(myname))
        time.sleep(2)

def respond(voice_data):
    if 'What Time' in voice_data:
        speak(ctime())

    if 'Search' in voice_data:
        speak("what do you want to search for")
        time.sleep(1)
        search = voice_analyzer()       
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)

    if 'Find Location' in voice_data:
        speak("Ok which location?")
        time.sleep(1)
        location = voice_analyzer()      
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url) 

    if 'Joke' in voice_data:
        speak(pyjokes.get_joke()) 
        time.sleep(5)
        
    if 'Change Username' in voice_data:
	# request for the change in username, 
	# it will overwrite the existing file and save the new name
        change=True
        usrname(change) 

    if "Don't Listen" in voice_data or "Pause" in voice_data:
	# program will stop listening to any commands unless the wake word is spoken again
        wakeUp()

    if 'Exit' in voice_data or 'Close' in voice_data:
	#ends the program
        exit()
	
usrname(False) # by default it assumes that the username file exists
speak('How can I help you')
while 1:
    time.sleep(1.5)
    voice_data = voice_analyzer()
    # Listen to the voice, analyze it and print whatever could be understood 
    # and respond to it if it matches to a predefined command in respond()
    print('--{}'.format(voice_data))
    respond(voice_data)
