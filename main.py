from core.api_wrapper import DrivingHazardDetector
import time
import cv2
from timeit import default_timer as timer

api = DrivingHazardDetector()

start = -1
looked_left, looked_right = False, False
min_speed = 1e18
time_start_speed = -1 # we kinda dumb
start_speed = 0

acceleration = 0 # kyles dumb

def main():
    
    while True:
        imgs = api.capture_images()
        cv2.imshow('frame1', imgs[0])
        cv2.imshow('frame2', imgs[1]) # rip this proj

        # detect signs from road camera
        
        stop_bool = api.detect_signs(imgs[0])
        if stop_bool == True:
            start = timer()

        print(stop_bool)

        # warn about stop sign


        # detect LR-gaze

        left, right = api.detect_gaze()
        looked_left, looked_right = left or lookedLeft, right or lookedRight

        # pull OBD data
        speed, rpm, throttle = api.pull_OBD()
        speed = speed.value.to("mph")

        print(speed)
        min_speed = min(min_speed, speed)

        # check for stop sign failure

        fail_stop_sign = [False, False, False]
        if timer() - start > 5:
            fail_stop_sign[0] = not looked_left
            fail_stop_sign[1] = not looked_right
            fail_stop_sign[2] = min_speed > 0.5

            start = -1
            looked_left, looked_right = False, False

        # report error if applicable
        
        if True in fail_stop_sign: #maybe while stop_bool or less than 5 sec? or when your speed starts to increase and you dont see it
            stop_rules = ['look left', 'look right', 'fully stop']
            message = ''
            for count, i in enumerate(fail_stop_sign):
                if i == False:
                    message += 'you did not ' + stop_rules[count] + ', '
                if count == len(fail_stop_sign) - 1:
                    message = message[:-2] + '.' #if the message is a '.' then nothing plays it's just a pause
            api.play_audio(message)

        #detect if their driving is too jerky

        speed_diff = speed - start_speed
        time_diff = timer() - time_start_speed
        acceleration = speed_diff / time_diff
        
        if acceleration > #TOO FAST:
            #sound warning about too fast xd
            api.play_audio('you are accelerating too fast weeeeee woooooo weeeeeee woooooo xdxdxdxdxdxd omegalul')
        elif: acceleration < -0.00229907
            #sound warning braking too fast
            api.play_audio('you are gonna damage your brake pads')

        #reset timer and speeds 

        time_start_speed = timer() # where's eddie's model @ tho :(
        start_speed = speed
        #braking too fast
        
        #accelerating too fast

        # detect emotion from face cam

        # detect drowsiness from face cam

        # sound alarm if they're drowsy

        #sound alarm if they're angr 


        # break


if __name__ == "__main__":
    main()

    # 👁💧👄💧👁