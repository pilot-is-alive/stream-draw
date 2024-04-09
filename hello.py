import numpy as np
import cv2 as cv
 
drawing = False # true if mouse is pressed
ix,iy = -1,-1
win_size = (900,1600,3)
win_size_height = win_size[0]
win_size_width = win_size[1]
factor = 3
vid_size = (int(win_size_width/factor), int(win_size_height/factor))
color = (255,255,255)
video_webcam = cv.VideoCapture(0)
img_blackboard = np.zeros(win_size, np.uint8)
cv.namedWindow('image')

fourcc = cv.VideoWriter_fourcc(*'avc1')
out = cv.VideoWriter('output.mp4', fourcc,45.0, (win_size_width, win_size_height))

if not video_webcam.isOpened():
  print("Couldn't open video webcam capture")
  exit()


 
# mouse draw callback function
def draw_circle(event,x,y,flags,param):
  global ix,iy,drawing
 
  if event == cv.EVENT_LBUTTONDOWN:
    drawing = True
    ix,iy = x,y
 
  elif event == cv.EVENT_MOUSEMOVE:
    if drawing == True:
      cv.circle(img_blackboard,(x,y),2,color,-1)
 
  elif event == cv.EVENT_LBUTTONUP:
    drawing = False
    cv.circle(img_blackboard,(x,y),5,color,-1)

# Use mouse callback
cv.setMouseCallback('image',draw_circle)
 
while(1):
  ret, frame = video_webcam.read()
  if not ret:
    print("Error: Unable to read frame from video capture.")
    break

  frame = cv.resize(frame, vid_size)
  img_blackboard[0:frame.shape[0], 0:frame.shape[1]] = frame
  out.write(img_blackboard)

  cv.imshow('image',img_blackboard)
  k = cv.waitKey(1) & 0xFF
  if k == ord('q'):
    break
 
cv.destroyAllWindows()
video_webcam.release()
out.release()