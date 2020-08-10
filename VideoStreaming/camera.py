#camera.py
# import the necessary packages
import os
import dlib
import cv2 as cv
import numpy as np
from urllib.request import urlopen
import requests
import time

global bts

class VideoCamera(object):
    def __init__(self):
        global bts
        self.inpWidth = 320       #Width of network's input image
        self.inpHeight = 240      #Height of network's input image
        predictor_path = "shape_predictor_5_face_landmarks.dat"
        face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
        self.faces_folder_path = "./faces"
         # Webcam input
        self.stream = urlopen("7688網址:8080/?action=stream")
        self.CAMERA_BUFFRER_SIZE=4096
        bts=b''

        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(predictor_path)
        self.facerec = dlib.face_recognition_model_v1(face_rec_model_path)
       
    def get_frame(self,det):

        #extracting frames
        global bts
        bts+=self.stream.read(self.CAMERA_BUFFRER_SIZE)     
        self.stream.flush()
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')

        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
            frame=cv.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv.IMREAD_UNCHANGED)      
            h,w=frame.shape[:2]
            img=cv.resize(frame,(self.inpWidth,self.inpHeight))
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
            bkImg = img

            if(det):     
                dets = self.detector(img, 1)
                print("Number of faces detected: {}".format(len(dets)))

                # Now process each face we found.
                for k, d in enumerate(dets):
                    #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    #    k, d.left(), d.top(), d.right(), d.bottom()))
                    # Get the landmarks/parts for the face in box d.
                    shape = self.sp(img, d)

                    face_descriptor = self.facerec.compute_face_descriptor(img, shape)
                    #print(face_descriptor)
            
                    img = cv.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 255), 2)
                    
                    faceImg = cv.rectangle(bkImg, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 255), 2)
                    newFileName = "Face_"+str(time.time())+".jpg"
                    cv.imwrite(os.path.join(self.faces_folder_path, newFileName), cv.cvtColor(faceImg, cv.COLOR_RGB2BGR))

                # encode OpenCV raw frame to jpg and displaying it
                ret, jpeg = cv.imencode('.jpg', cv.cvtColor(img, cv.COLOR_RGB2BGR))
                return jpeg.tobytes()
            else:
                ret, jpeg = cv.imencode('.jpg', cv.cvtColor(img, cv.COLOR_RGB2BGR))
                return jpeg.tobytes()
        return None