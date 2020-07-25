from core.api_wrapper import DrivingHazardDetector
# run this to continually do stuff


api = DrivingHazardDetector()

import cv2

while True:
    
    print('kevin is initially shit')
    # call your models and obd and stuff and take action
    

    imgs = api.capture_images()
    cv2.imshow('frame1', imgs[0])
    cv2.imshow('frame2', imgs[1])

    # detect signs from road camera
    
    print(api.detect_signs(imgs[0]))


    # detect emotion from face cam

    # detect drowsiness from face cam

    # use obd data to do shit
    #speed, rpm, throttle = api.pull_OBD()

    # break
    print(' is still shit')