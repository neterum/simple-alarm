import paho.mqtt.client as mqtt
import threading
import logging
import strings

class Mqttdetect:
    def __init__(self, on_message):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message
        self.client.connect("127.0.0.1",1883,60)
        self.logger = logging.getLogger(strings.LOGGER_NAME)
        self.thread = threading.Thread(target=self.threadLoop)
        self.thread.start()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.debug("MQTT connected with results code "+str(rc))
        client.subscribe("door")

    def threadLoop(self):
        self.client.loop_forever()