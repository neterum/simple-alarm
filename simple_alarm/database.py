import os
import json

class Database:
    def __init__(self, tracked_device):
        self.devices = {}
        self.tracked_device = tracked_device
        file_path = os.path.expanduser("~/.config/simple-alarm/devices.json")
        if os.path.exists(file_path):
            file = open(file_path)
            content = file.read()
            self.devices = self.safelyReadJson(content)
        else:
            print("Missing devices file.  Will not trigger alarms")

    def getDevices(self):
        return self.devices

    def safelyReadJson(self, content: str):
        try:
            decoded = json.loads(content)
        except json.JSONDecodeError as e:
            print("JSONDecodeError occurred:", e)
        except TypeError as e:
            print("TypeError occurred:", e)
        except UnicodeEncodeError as e:
            print("UnicodeEncodeError occurred:", e)
        else:
            return decoded


    def sensorDetected(self, captured: str):
        """
        Receives a string containing unparsed json data, checks to see if 'id' value in captured data is
        in tracked devices, and returns device json data if found.

        Args:
            captured (string): Unparsed json data 

        Returns:
            tuple: A tuple with first object being the stored device and the second object being the 
            captured and parsed json object.
        """
        data = self.safelyReadJson(captured)
        if len(data) > 0 and len(self.devices) > 0:
            for device in self.devices:
                if device["id"] == data["id"]:
                    self.tracked_device(device, data)

    def getVoice(self, data):
        for device in self.devices:
            if device["id"] == data["id"]:
                return device["voice"]

    


# {"time":"2023-03-26 14:30:09","model":"Interlogix-Security","subtype":"contact","id":"a8abe5","battery_ok":1,"switch1":"OPEN","switch2":"OPEN","switch3":"CLOSED","switch4":"OPEN","switch5":"OPEN","raw_message":"ed152c"}