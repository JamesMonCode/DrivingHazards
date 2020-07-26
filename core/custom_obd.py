import obd
import time
import pyttsx3

obd.logger.setLevel(obd.logging.DEBUG)

class MyOBD:
    def __init__(self):
        self.connection = obd.OBD(portstr="\\.\\COM3", timeout=30)

        if not self.obd_working():
            raise Exception('OBD sucks ass; timeout not long enough/failed connection')
        
    def obd_working(self, test_query=obd.commands.SPEED):
        if len(self.connection.supported_commands) <= 7:
            return False
        
        res = self.connection.query(test_query)
        return res is not None
    
    def query_data(ver):
        assert ver in ['speed', 'rpm', 'throttle']

        ver_to_cmd = {
            'speed': obd.commands.SPEED,
            'rpm': obd.commands.RPM,
            'throttle': obd.commands.THROTTLE_POS,
        }

        return self.connection.query(ver_to_cmd[ver], force=True)

    def play_audio(self, alert):
        engine = pyttsx3.init()
        if alert == :
            engine.say('you are dumb') 
        elif alern == :
            engine.say('option2')

        engine.runAndWait()
        # and more