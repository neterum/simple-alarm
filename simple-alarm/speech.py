import pyttsx3
import threading

class Speech:
    def __init__(self):
        """
        Creates the voice engine, sets the voice rate, and assigns an
        english speaking voice.
        """
        self.rate = 150
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voices', voices[17].id) # English voice
        
        # How to display current rate
        # rate = self.engine.getProperty('rate')    # getting details of current speaking rate
        # print (rate)                              # printing current voice rate
        self.engine.setProperty('rate', self.rate)  # setting up new voice rate
        # uncomment below code to see different voices
        # voices = engine2.getProperty('voices')
        # for voice in voices:
        #    print(voice.id)

    def runAndWait(self):
        """
        Starts the voice engine
        """
        self.engine.runAndWait()

    def speak(self, speech : str):
        """
        Calls voice engine to output the speech parameter.
        
        Parameters:
        speech (str) : To be spoken by voice engine
        """
        print(speech)
        self.engine.say(speech)
        self.engine.runAndWait()