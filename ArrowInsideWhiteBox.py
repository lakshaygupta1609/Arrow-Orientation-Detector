import numpy as np
import cv2,math  
from matplotlib import pyplot as plt
import utils



cap=cv2.VideoCapture(0)

while True:
    success, img=cap.read()

    imgcont,conts,_=utils.getContours(img,cThr=[150,175],showCanny=False,filter=4,draw=False) #Selecting the White box
    
    if len(conts) != 0:
        biggest = conts[0][2]
        imgWarp = utils.warpImg(img, biggest,350,350) #warping the Image to Region of Interest
    
        imgCont2,cont2,imgThre=utils.getContours(imgWarp,cThr=[50,50],showCanny=False,filter=7,draw=False)   #Finding the Countours of Arrow
               
        
        if len(cont2) != 0:
            
            tip=tuple(cont2[0][2][0][0])
            #tip2=tuple(cont2[0][2][3][0])
            M = cv2.moments(cont2[0][2])
            cX = int(M["m10"] / M["m00"])    #Finding the centroid of the arrow
            cY = int(M["m01"] / M["m00"])
            cv2.circle(imgCont2, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(imgCont2, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.circle(imgCont2,tip, 7, (255,0,0), -1)
            cv2.circle(imgCont2,(300,cY), 7, (255,0,0), -1)
            for obj in cont2:
                cv2.polylines(imgCont2,[obj[2]],True,(0,255,0),2)
                cv2.imshow('Region of Interest',imgCont2)           #Smoothening the Contours of the arrow
            
            
            angle=int(utils.getAngle(tip,(cX,cY),(300,cY)))
            #print(angle)
           
        
            if 315<=angle<=359 or 0<=angle<45:
                print("Right")
                cv2.putText(img, "RIGHT", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)   
            elif 85<angle<95:
                print('UP')
                cv2.putText(img, "UP", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)   
            elif 135<angle<225:
                print('Left')
                cv2.putText(img, "LEFT", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)   
            else:
                print('Down')
                cv2.putText(img, "DOWN", (40,40),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
              
    cv2.imshow("Video",img)
    
    k=cv2.waitKey(1) 
    if k==27:
        break


