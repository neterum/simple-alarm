import threading
import time

class SensorState:
    """
    Parent class.
    """
    def enter(self):
        pass

    def exit(self):
        pass

class OpenState(SensorState):
    """
    Represents a sensor currently in an open state, 
    typically caused by an open door or window
    """
    def __init__(self, sensor):
        self.sensor = sensor

class ClosedState(SensorState):
    """
    Represents a sensor in a closed state
    """
    def __init__(self, sensor):
        self.sensor = sensor

class Sensor:
    def __init__(self, open_callback, timerInterval=5):
        """
        A state machine.  Devices will either be in an open or closed state.
        A sensor sends off not one but several "open" messages within the
        span of a few seconds.  This class allows the application to
        "speak" the device's name only once per a user set timelength.  The
        timelength is set with the timerInteral with a time-second interval.
        Timer interval defaults to 5.  By default, the application will only
        speak the devices name at a max of once per 5 seconds, no matter how
        many received "open" messages.

        Parameters:
        open_callback (callable) : Method called that state machine will call
        when application is allowed to announce device.  

        timerInterval (int) : Interval in seconds.  Device can only be
        announced by application a max of one time during this interval.
        """
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