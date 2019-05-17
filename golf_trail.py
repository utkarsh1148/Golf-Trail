import numpy as np
import cv2
from matplotlib import pyplot as plt
import argparse
from scipy.spatial import distance as dist
from scipy.optimize import curve_fit
import math
import csv
video_name='side_view_shot_16.mp4'
font = cv2.FONT_HERSHEY_SIMPLEX
def calc_vel (pt1,pt2,fps,frame_diff):
    distance=dist.euclidean(pt1,pt2)
    velocity =(distance*fps)/frame_diff
    return velocity
def apply_rectangular_mask(img,x1,y1,x2,y2):
    img_=img.copy()
    mask = np.zeros(img_.shape, dtype = "uint8")
    cv2.rectangle(mask,(x1,y1),(x2,y2),(255,255,255),-1)
    return cv2.bitwise_and(img_, mask)
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
 
		# draw a rectangle around the region of interest
		cv2.circle(img, refPt[0],radius, (0, 255, 0), 2)
def save_first_frame_of_video():
    cap = cv2.VideoCapture(video_name)
    while(cap.isOpened()):
      ret, frame = cap.read()
      if(ret):
        cv2.imwrite('frame1.png',frame)
        break
def apply_circular_mask(img,px_,py_,r,shiftX,shiftY):
    img_=img.copy()
    mask = np.zeros(img_.shape, dtype = "uint8")
    cv2.circle(mask,(px_+shiftX,py_-shiftY),r,(255,255,255),-1)
    
    return cv2.bitwise_and(img_, mask)


radius=65
refPt = []

y_th=2
x_th=2



save_first_frame_of_video()
img = cv2.imread('frame1.png',1)
frame_h,frame_w,frame_c=img.shape
#print('frame h',frame_h,'frame_w',frame_w)

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
while True:
	cv2.imshow("image", img)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
        #cv2.destroyAllWindows()
		break


gimg=img[:,:,0]
cv2.imshow('gimg',gimg)
cball=apply_circular_mask(gimg,refPt[0][0],refPt[0][1],radius,0,0)
_,thresh=cv2.threshold(cball,160,255,cv2.THRESH_BINARY)

#thresh=cv2.erode(thresh,kernel,iterations = 1)
#thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
thresh=cv2.morphologyEx(thresh, cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))

thresh=cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
thresh = cv2.GaussianBlur(thresh,(5,5),0)

conts,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

max_i=-1
max_area=0
for i in range(0,len(conts)):
    (cX,cY),r= cv2.minEnclosingCircle(conts[i])
    this_area=3.14*r*r
    if(this_area>max_area):
        max_area=this_area
        max_i=i
if(max_i!=-1):
    cX=550
    cY=410
    r=20
    (cX,cY),r= cv2.minEnclosingCircle(conts[max_i])

    
    
  
       
    prev_cont=conts[max_i]
    px_i=int(cX)
    py_i=int(cY)
    area_i=max_area
    x,y,w,h = cv2.boundingRect(conts[max_i])
    cv2.circle(img,(int(cX),int(cY)),int(r),(0,0,0),2)


cv2.drawContours(img,conts,-1,(0,255,0),1)

cv2.imshow('image',img)
cv2.imshow('thresh',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()


px_center=[]
py_center=[]

px_top=[]
py_top=[]

px_left=[]
py_left=[]


area=[]
frame_no=[]





area.append(area_i)
frame_no.append(0)

frame_count=1








cap = cv2.VideoCapture(video_name)
# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0,255,(100,3))
# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame,cv2.COLOR_BGR2GRAY)
#p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

#p0= np.array([300, 300]).reshape(1, 1,2)
p0=np.array([[[px_i,py_i]],[[px_i, py_i-r+14]],[[px_i-r+14, py_i]]], dtype=np.float32)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
while(1):
  ret,frame = cap.read()
  if(ret):
    frame_gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]
    # draw the tracks
    len_=0
    for i,(n,o) in enumerate(zip(good_new,good_old)):
        len_=len_+1

    if(len_==3):
      for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        if(i==0):
            px_center.append(a) 
            py_center.append(b)
            
        elif(i==1):
            px_top.append(a) 
            py_top.append(b)
        else:
            px_left.append(a) 
            py_left.append(b)

     
        frame_no.append(frame_count)
        area.append(area_i)
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        


        
        if(len(px_center)%7==0 and frame_count>20 and False):
          r=math.sqrt(area_i/3.14)
          vel=calc_vel((px_center[-1],py_center[-1]),(px_center[-5],py_center[-5]),25,frame_no[-1]-frame_no[-5])  
          k=0.04267/(2*r)
          vel_act=vel*k
          
          cv2.putText(mask,2*str(vel_act),(int(px_center[-1]),int(py_center[-1])), font, 0.3,(255,255,255),1,cv2.LINE_AA)
        frame = cv2.circle(frame,(a,b),3,color[i].tolist(),-1)
            
        #print(len(px_center),len(px_top),len(px_left))
        img = cv2.add(frame,mask)
        cv2.imshow('frame',img)
        frame_count=frame_count+1
        k = cv2.waitKey(30) & 0xff
        if k == 27:
         break
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)
    else:
        print('ended')
        break
  else:
        print('video end')
        break





cv2.waitKey(0)
cv2.destroyAllWindows()
#for i in range(0,len(px_center)-1):
#    cv2.line(frame,(px_center[i],py_center[i]),(px_center[i+1],py_center[i+1]),(255,0,0),2)
#    if(i%5==0):
#           cv2.putText(frame,'('+str(px_center[i])+','+str(py_center[i])+')',(int(px_center[i]),int(py_center[i])), font, 0.3,(255,0,0),1,cv2.LINE_AA)

py_center[:]=[frame_h-y for y in py_center]

rows = zip(px_center,py_center,frame_no,area)

with open('motion.csv', "w",newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

