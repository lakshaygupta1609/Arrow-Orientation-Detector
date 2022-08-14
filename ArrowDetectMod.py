import numpy as np
import cv2,math  
from matplotlib import pyplot as plt
import utils
import random as rng
import imutils

def find_marker(image):
    	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)

KNOWN_DISTANCE = 24.0
# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 20.0
image = cv2.imread("arrow_qt1.jpeg")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

cap=cv2.VideoCapture(0)

while True:
    success, img=cap.read()

    imgcont,conts,_=utils.getContours(img,cThr=[150,175],showCanny=False,minArea=1000,filter=7,draw=False) #Selecting the White box
    #print (conts)
    if len(conts) != 0:
        for obj in conts:
            cv2.polylines(imgcont,[obj[2]],True,(0,255,0),2)
        #cv2.imshow('Region of Interest',imgcont) 
        x,y,w,h = cv2.boundingRect(conts[0][2])
        
        cv2.rectangle(img,(x-20,y-20),(x+w+20,y+h+20),(0,255,0),2)
        crop_img = img[y-20:y+h+20, x-20:x+w+20]
        #cv2.imshow("Warp",crop_img)
        tip=tuple(conts[0][2][0][0])
            
        M = cv2.moments(conts[0][2])
        cX = int(M["m10"] / M["m00"])    #Finding the centroid of the arrow
        cY = int(M["m01"] / M["m00"])
        
        cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(img, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #cv2.circle(img,tip, 7, (255,0,0), -1)
        #cv2.circle(img,(100,cY), 7, (255,0,0), -1)
        
        angle=int(utils.getAngle(tip,(cX,cY),(30,cY)))
        #print(angle)
        # convert the image to grayscale, blur it, and detect edges
          
        inches = (KNOWN_WIDTH * focalLength) / w            
        
        if 315<=angle<=359 or 0<=angle<45:
            print("Left %.2fft" % (inches / 12))
            cv2.putText(img, "Left %.2fft" % (inches / 12), (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)   
        elif 260<angle<279:
            print('UP %.2fft' % (inches / 12))
            cv2.putText(img, "UP %.2fft" % (inches / 12), (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)   
        elif 135<angle<225:
            print('Right %.2fft' % (inches / 12))
            cv2.putText(img, "RIGHT %.2fft" % (inches / 12), (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)   
        else:
            print('Down %.2fft' % (inches / 12))
            cv2.putText(img, "DOWN %.2fft" % (inches / 12), (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
    
    cv2.imshow("Video",img)
    
    k=cv2.waitKey(1) 
    if k==27:
        break