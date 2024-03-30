import sys, os, signal, functools

# sys.path.append(os.path.abspath(os.path.join('..', 'simple_alarm/simple_alarm')))

# print(sys.path)

from mqttdetect import Mqttdetect
from database import Database
from speech import Speech
from sensorstatemachine import SensorStateMachine
import json
import logging
import logging.config
import configparser
import strings

class Alarm:
    def __init__(self):
        """
        Most other objects will be instantiated within this main "controller"
        class.
        """

        config_file = 'logging.ini'
        config = configparser.ConfigParser()
        config.read(config_file)

        home_directory = os.path.expanduser("~")

        log_folder_path = os.path.join(home_directory, strings.LOG_FOLDER_LOCATION_INSIDE_HOME)

        exists = os.path.exists(log_folder_path)

        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)

        log_file_path = os.path.join(log_folder_path, strings.LOG_FILENAME)
        config.set('handler_file', 'args', f'("{log_file_path}",)')

        with open(config_file, 'w') as configfile:
            config.write(configfile)

        logging.config.fileConfig("logging.ini")

        self.logger = logging.getLogger("mainLogger")
        self.logger.debug('debug message')
        self.logger.critical("critical message")
        self.logger.propagate = False

        # Create an MQTT object. Initialize it by passing a method from this
        # object to be called after receiving an MQTT message.
        self.mqtt = Mqttdetect(on_message=self.on_message)

        # Create a database object that will read in a file located at
        # "~/.config/simple-alarm/devices.json" containing tracked devices.
        # All received MQTT messages will be passed to database object and will
        # call self.tracked_devices if a MQTT message is from tracked device.
        self.database = Database(tracked_device=self.tracked_device)

        # The speech object will speak the name of the sensor that was
        # captured by this application
        self.speech = Speech()

        # A sensor will output not a single but several "open" MQTT messages.
        # This state machine was added to make sure only this application only
        # "speaks" the sensor's name one time after a captured MQTT message, 
        # and not after every "open" MQTT message.
        self.stateMachine = SensorStateMachine()

        # All received MQTT messages are outputted to a log.txt file located
        # in same directory of application.  ToDo: Improve this
        self.file = open("./log.txt", 'w')
        for device in self.database.devices:
            self.stateMachine.addSensor(id=device["id"], open_callback=self.sensor_speak)

    def on_message(self, client, userdata, msg):
        """
        This method is called inside MQTT object.  The message will be sent to
        the database object to determine if it came from a tracked sensor.
        """
        print(str(msg.payload.decode()))
        # self.file.write(msg.payload.decode() + "\n")
        self.logger.debug(msg.payload.decode())
        # Might be able to just send msg, not sure yet
        self.database.sensorDetected(str(msg.payload.decode()))

    def tracked_device(self, data):
        """
        Sends the tracked device to the state machine to decide where or not
        to speak a sound.
        """
        if data["switch1"] == "OPEN":
            self.stateMachine.open(id=data["id"], data=data)
        else:
            self.stateMachine.close(id=data["id"])

    def sensor_speak(self, data):
        """Sends the device to the """
        self.speech.speak(self.database.getVoice(data))
        
    def close_file(self):
        self.file.close()
        
def signal_handler(c):
    print("Caught control-c, exiting...")
    c.close_file()
    
class MyClass:
    def __init__(self, alarm: Alarm):
        self.alarm = alarm
        
    def signal_handler(self, signum, frame):
        print(f"Received signal {signum}")
        self.alarm.close_file()
        exit(0)

def main():
    #sys.path.append(os.path.abspath(os.path.join('..', 'simple_alarm/simple_alarm')))
    print(sys.path)
    alarm = Alarm()
    my_object = MyClass(alarm)
    signal.signal(signal.SIGINT, functools.partial(my_object.signal_handler))

if __name__ == "__main__":
    main()