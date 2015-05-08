import numpy as np
import cv2

cap = cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG()
while(True):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv2.imshow('frame',fgmask)
    cv2.imshow('frame_raw',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
