import cv2

webcam1 = cv2.VideoCapture(1)
webcam2 = cv2.VideoCapture(2)

#ret, video_frame = webcam1.read()
#cv2.imshow('frame', video_frame)

#frame_width = int(round(webcam1.get(cv2.CAP_PROP_FRAME_WIDTH)))
#frame_height = int(round(webcam2.get(cv2.CAP_PROP_FRAME_HEIGHT)))

PF_U8_RGB = 1
PF_U8_BGR = 2
PF_U8_RGBA = 3
 
# BGR U8 is the default pixel format of OpenCV images.
# We create an empty texture
#frame_texture = gh_texture.create_2d(frame_width, frame_height, PF_U8_BGR)
 
# and we update the texture pixmap with the OpenCV image.
#gh_texture.update_gpu_memory_from_numpy_img(frame_texture, video_frame)

#cv2.imwrite(filename=test_img.jpeg, img=video_frame)

while(True): 
      
    # Capture the video frame 
    # by frame 
    ret1, frame1 = webcam1.read()
    ret2, frame2 = webcam2.read() 

    # Display the resulting frame 
    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', frame2) 
    cv2.imwrite(filename='test_img.jpeg', img=frame1)
    cv2.imwrite(filename='test_img1.jpeg', img=frame2)
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 