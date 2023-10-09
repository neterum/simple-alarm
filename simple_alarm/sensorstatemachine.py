import threading
import time

class SensorState:
    '''Parent class.  '''
    def enter(self):
        pass

    def exit(self):
        pass

class OpenState(SensorState):
    '''Represents a sensor currently in an open state, 
    typically caused by an open door or window'''
    def __init__(self, sensor):
        self.sensor = sensor
    # def enter(self):
    #     print("Sensor is now open")

class ClosedState(SensorState):
    def __init__(self, sensor):
        self.sensor = sensor
    # def enter(self):
    #     print("Sensor is now closed")

class Sensor:
    def __init__(self, open_callback, timerInterval=5):
        self.open_state = OpenState(self)
        self.closed_state = ClosedState(self)
        self.current_state = self.closed_state
        self.timerInterval = timerInterval
        self.open_callback = open_callback

    def open(self, data):
        if isinstance(self.current_state, OpenState):
            return
        self.current_state = self.open_state
        self.current_state.enter()
        self.timer = threading.Timer(self.timerInterval, self.close)
        self.timer.start()
        self.open_callback(data)

    def close(self):
        if isinstance(self.current_state, ClosedState): 
            return
        self.current_state = self.closed_state
        self.current_state.enter()
        self.timer.cancel()

class SensorStateMachine:
    def __init__(self):
        self.dict = {}

    def addSensor(self, id, open_callback):
        self.dict[id] = Sensor(open_callback=open_callback)

    def open(self, id, data):
        self.dict[id].open(data)

    def close(self, id):
        self.dict[id].close()

# create a sensor and test its state transitions
# sensor = Sensor()
# sensor.close()
# sensor.open()
# sensor.open()
# time.sleep(11)
# sensor.open()


