
from opencv.cv import *
from opencv.highgui import *


capture = cvCreateCameraCapture(CV_CAP_ANY)
face_cascade = cvLoadHaarClassifierCascade("face_cascade", cvSize(20, 20))
body_cascade = None
#body_cascade = cvLoadHaarClassifierCascade("upper_body_cascade", cvSize(22, 18))

storage = cvCreateMemStorage(0)

cvNamedWindow("result", 1)

frame_copy = False

def detect_and_draw(img):
    """Detects faces in an image and draws the result"""
    
    scale = 1
    temp = cvCreateImage(cvSize(img.width / scale, img.height / scale), 8, 3)
    
    cvClearMemStorage(storage)
    
    if face_cascade:
        faces = cvHaarDetectObjects(img, face_cascade, storage, 1.1, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(80, 80))
    else:
        faces = []

    if body_cascade:
        bodies = cvHaarDetectObjects(img, body_cascade, storage, 1.1, 2, CV_HAAR_DO_CANNY_PRUNING, cvSize(40, 40))
    else:
        bodies = []
    
    for face in faces:
        pt1 = cvPoint(face.x, face.y)
        pt2 = cvPoint(face.x + face.width, face.y + face.height)
        cvRectangle(img, pt1, pt2, CV_RGB(255, 0, 0), 3, 8, 0)
    
    for body in bodies:
        pt1 = cvPoint(body.x, body.y)
        pt2 = cvPoint(body.x + body.width, body.y + body.height)
        cvRectangle(img, pt1, pt2, CV_RGB(0, 0, 244), 3, 8, 0)
    
    cvShowImage("result", img)
        

if capture:
    while True:
        if not cvGrabFrame(capture):
            break
        frame = cvRetrieveFrame(capture)
        
        if not frame:
            break
        
        if not frame_copy:
            frame_copy = cvCreateImage(cvSize(frame.width, frame.height), IPL_DEPTH_8U, frame.nChannels)
        
        if frame.origin == IPL_ORIGIN_TL:
            cvCopy(frame, frame_copy, 0)
        else:
            cvFlip(frame, frame_copy, 0)
        
        detect_and_draw(frame_copy)
        
        if cvWaitKey(10) >= 0:
            break
    
    cvReleaseImage(frame_copy)
    cvReleaseCapture(capture)

cvDestroyWindow("result")

