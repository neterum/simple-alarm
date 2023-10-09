import pyttsx3
import threading

class Speech:
    def __init__(self):
        self.rate = 150
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voices', voices[17].id) # English voice
        
        """ RATE"""
        rate = self.engine.getProperty('rate')       # getting details of current speaking rate
        print (rate)                            # printing current voice rate
        self.engine.setProperty('rate', self.rate)   # setting up new voice rate
        # self.thread = threading.Thread(target=self.runAndWait)
        # self.thread.start()

        # uncomment below code to see different voices
        # voices = engine2.getProperty('voices')
        # for voice in voices:
        #    print(voice.id)

    def runAndWait(self):
        self.engine.runAndWait()

    def speak(self, speech):
        print(speech)
        self.engine.say(speech)
        self.engine.runAndWait()