from .custom_obd import MyOBD
import cv2
from .sign_detect.Inference.DetectorAPI import MySignDetector

# from sign_detect import something
# from openface import something
# define a class that you can instantiate in main.py that contains all calls to your components


class DrivingHazardDetector:
    def __init__(self):
        self.webcams = [cv2.VideoCapture(1), cv2.VideoCapture(2)]
        #self.OBD = MyOBD()
        self.sign_detector = MySignDetector(0.6)

    def capture_images(self):
        ret1, frame1 = self.webcams[0].read()
        ret2, frame2 = self.webcams[1].read() 
        assert ret1 and ret2, 'Camera capture failed!'

        return frame1, frame2

    def detect_signs(self, img):
        return self.sign_detector.checkForSigns(img)

    def detect_gaze(self):


        
        pass


        # return looked_left, looked_right
        # create an openface class gaze object thing
        # eq: what do you need as output? a dictionary!
        # output format: a dict where key = sign type, val = bool -> yes/no based on presence

    def pull_OBD(self):
        speed = self.OBD.query_data('speed')
        rpm = self.OBD.query_data('rpm')
        throttle = self.OBD.query_data('throttle')

        return speed, rpm, throttle

    # etc etx
