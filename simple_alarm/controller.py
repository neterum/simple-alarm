import sys, os, signal, functools

# sys.path.append(os.path.abspath(os.path.join('..', 'simple_alarm/simple_alarm')))

# print(sys.path)

from mqttdetect import Mqttdetect
from database import Database
from speech import Speech
from sensorstatemachine import SensorStateMachine
import json

class Controller:
    def __init__(self):
        self.mqtt = Mqttdetect(on_message=self.on_message)
        self.database = Database(tracked_device=self.tracked_device)
        self.speech = Speech()
        self.stateMachine = SensorStateMachine()
        self.file = open("./log.txt", 'w')
        for device in self.database.devices:
            self.stateMachine.addSensor(id=device["id"], open_callback=self.sensor_speak)

    def on_message(self, client, userdata, msg):
        print(str(msg.payload.decode()))
        self.file.write(msg.payload.decode() + "\n")
        # Might be able to just send msg, not sure yet
        self.database.sensorDetected(str(msg.payload.decode()))

    def tracked_device(self, device, data):
        if data["switch1"] == "OPEN":
            self.stateMachine.open(id=data["id"], data=data)
        else:
            self.stateMachine.close(id=data["id"])
        #self.speech.speak("device ID " + data["id"] + " " + device["voice"] + " is " + data["switch1"])

    def sensor_speak(self, data):
        self.speech.speak(self.database.getVoice(data))
        
    def close_file(self):
        self.file.close()
        
def signal_handler(c):
    print("Caught control-c, exiting...")
    c.close_file()
    
class MyClass:
    def __init__(self, controller: Controller):
        self.controller = controller
        
    def signal_handler(self, signum, frame):
        print(f"Received signal {signum}")
        self.controller.close_file()
        exit(0)

def main():
    #sys.path.append(os.path.abspath(os.path.join('..', 'simple_alarm/simple_alarm')))
    print(sys.path)
    c = Controller()
    my_object = MyClass(c)
    signal.signal(signal.SIGINT, functools.partial(my_object.signal_handler))

if __name__ == "__main__":
    main()