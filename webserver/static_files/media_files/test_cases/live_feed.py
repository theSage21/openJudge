import cv,cv2

def get_live_feed():
    cam=cv.CaptureFromCAM(0)
    window=cv.NamedWindow('live',0)
    window=cv.NamedWindow('live_subtracted',0)
    #calibrate the camera
    #required to adjust for lighting
    for i in range(10):
        img=cv.QueryFrame(cam)
    #capture and show the feed
    while True:
        img=cv.QueryFrame(cam)
        if img!=0:
            cv.ShowImage('live',img)
        c=cv.WaitKey(10)
        if c==27:break
    cv.DestroyWindow('live')

if __name__=='__main__':
    get_live_feed()
