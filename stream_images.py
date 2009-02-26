
from opencv.cv import *
from opencv.highgui import *
from time import sleep
from getopt import getopt
from socket import *


opts, args = getopt(sys.argv[1:], 'i:p:', ['interface=', 'port=' ])

interface = ''
port = 7422

for o, a in opts:
    if o in ('-i', '--interface'):
        interface = a
    elif o in ('-p', '--port'):
        port = int(a)

sock = socket()
sock.bind((interface, port))
sock.listen(1)

capture = cvCreateCameraCapture(CV_CAP_ANY)

if not capture:
    print "No capture device!"
    exit(1)
frame_copy = False

if capture:
    while True:
        client, client_address = sock.accept()
        if not cvGrabFrame(capture):
            break
        frame = cvRetrieveFrame(capture)
        
        if not frame:
            sleep(0.1)
            continue
        
        cvSaveImage("/tmp/predabot_tmp.jpg", frame)
        tmp = open("/tmp/predabot_tmp.jpg")
        data = tmp.read()
        tmp.close()
        
        client.sendall(data)
    
    cvReleaseImage(frame_copy)
    cvReleaseCapture(capture)

cvDestroyWindow("result")

