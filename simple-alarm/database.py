import os
import json
import strings
import logging

class Database:
    def __init__(self, tracked_device):
        """
        Attempts to read in a JSON file of tracked wireless devices.

        Parameters:
        tracked_device: callable that is triggered when self receives a JSON
        in self.sensorDetected that matches a device ID in self.devices.
        """

        self.logger = logging.getLogger(strings.LOGGER_NAME)
        self.devices = {}
        self.tracked_device = tracked_device
        file_path = os.path.expanduser(strings.CONFIG_FILE_LOCATION)
        if os.path.exists(file_path):
            return # FIXME THERE IS A DATABASE ERROR HERE
            file = open(file_path)
            content = file.read()
            self.devices = self.readJson(content)
        else:
            print("Missing devices file.  Will not trigger alarms")

    def getDevices(self):
        """
        Returns the local JSON object containing all devices.  Properties
        include "id" "device" and "voice".

        Returns:
        JSON Object : All tracked devices in JSON.  
        """
        return self.devices

    def readJson(self, content: str):
        """
        Attempts to load unparsed JSON data from content argument in a safe
        manor.  If successful, will return a JSON object.

        Parameters:
        content (str) : A string containing possible JSON data.

        Returns:
        JSON Object : Parsed JSON object or null if unsuccessful attempt.
        """

        """
        ChatGPT recommends:
        with open('your_json_file.json', 'r') as file:
            self.database = json.load(file)
        """
        try:
            decoded = json.loads(content)
            self.logger.debug(f"Database read success {decoded}")
            return decoded
        except (json.JSONDecodeError, TypeError, UnicodeEncodeError) as e:
            self.logger.error(f"Database readerror: {e}")
            return None


    def sensorDetected(self, captured: str):
        """
        Creates a JSON object from unparsed data in captured argument and calls
        the tracked_data saved method if 'id' value from the captured data
        matches a tracked device.
        
        Parameters:
        captured (str): Unparsed json data 
        """
        data = self.readJson(captured)
        if len(data) > 0 and len(self.devices) > 0:
            for device in self.devices:
                if device[strings.JSON_KEY_ID] == data[strings.JSON_KEY_ID]:
                    self.tracked_device(data)

    def getVoice(self, data):
        """
        Matches id from the data JSON object argument against the local JSON
        object and returns the matched speak phrase.  Returns null if not 
        found.

        Parmeters:
        data (JSON Object): A JSON object representing a tracked device

        Returns:
        str: The string assigned to be spoken by application or None
        if not found
        """
        for device in self.devices:
            if device[strings.JSON_KEY_ID] == data[strings.JSON_KEY_ID]:
                return device[strings.JSON_KEY_SPEAK]
        return None

# An MQTT data example. Will all be in the same line.  Broken
# up here for readability
# {"time":"2023-03-26 14:30:09","model":"Interlogix-Security",
# "subtype":"contact","id":"a8abe5","battery_ok":1,"switch1":"OPEN",
# "switch2":"OPEN","switch3":"CLOSED","switch4":"OPEN","switch5":"OPEN",
# "raw_message":"ed152c"}