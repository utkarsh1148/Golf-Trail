
import csv
import math
import cv2
from scipy.spatial import distance as dist
import math
fps=0
import scipy
noise_bound=2
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt



def f(x, A, B): 
    return A*x + B
def get_perp_dist(m_,c_,x1,y1):
    d=abs(m_*x1-y1+c_)
    d=d/math.sqrt(m_*m_+1)
    return d
def least_perpendicular(px,py):
    N=len(px)
    px=np.asarray(px)
    py=np.asarray(py)

    B=(np.sum(py*py)-(N*np.mean(py)**2))-(np.sum(px*px)-(N*np.mean(px)**2))
    D=(N*np.mean(px)*np.mean(py)-np.sum(px*py))
    
    if(D==0):
     D=0.0001
    B=0.5*B/D
    m1=-B+math.sqrt(B*B+1)
    m2=-B-math.sqrt(B*B+1)

    c1=np.mean(py)-m1*np.mean(px)
    c2=np.mean(py)-m2*np.mean(px)

    s1=0
    for i in range(0,len(px)):
        s1=s1+get_perp_dist(m1,c1,px[i],py[i])
    s2=0
    for i in range(0,len(px)):
        s2=s2+get_perp_dist(m2,c2,px[i],py[i])
    if(s1<s2):
        return m1,c1
    else:
        return m2,c2
def calc_vel (pt1,pt2,fps,frame_diff):
    distance=dist.euclidean(pt1,pt2)
    velocity =(distance*fps)/frame_diff
    return velocity

video = cv2.VideoCapture('side_view_shot_6.mp4')
     
# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print( "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
video.release()
px=[]
py=[]
area=[]
frame_number=[]

with open('motion.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_line=True
    csv_reader=list(csv_reader)
    for row in csv_reader:
        if first_line is True :
            first_line=False
            area_i=float(row[3])
            px_i=float(row[0])
            py_i=float(row[1])
          
            radius_i=int(4.4*math.sqrt(area_i/3.14))
            r=math.sqrt(area_i/3.14)
           
           
            continue

        distance=dist.euclidean((px_i,py_i),(float(row[0]),float(row[1])))
        if(distance>radius_i):
         px.append(float(row[0]))
         py.append(float(row[1]))
         area.append(float(row[3]))
         frame_number.append(int(row[2]))

plt.plot(px,py,'ro-')

#m,c=least_perpendicular(px,py)
m,c=curve_fit(f,px,py)[0]
theta=math.atan(m)*(180/math.pi)
px_=px
py_=[]


for i in range(0,len(px)):
    py_.append(m*px[i]+c)
plt.plot(px,py_,'bo-')

hy=[]
for i in range(0,len(px)):
    hy.append(0*px[i]+py_[0])
plt.plot(px,hy,'g')


#plt.axis([px[0], px[-1], min(py_[0],py[0]),max(py[-1],py_[-1])])
plt.axis([min(px[0]-r,py_[0]-r),max(py_[-1],px[-1]) ,min(px[0]-r,py_[0]-r),max(px[-1],py_[-1])])
plt.show()
 
vel=calc_vel((px[0],py_[0]),(px[-1],py_[-1]),fps,frame_number[-1]-frame_number[0])  
print('velocity : ',vel,' pixels/sec')
#theta=math.atan(abs(py_[-1]-py_[0])/abs(px[-1]-px[0]))


#r=math.sqrt(area_i/3.14)
print('radius of golf ball: ',r,'pixels')
k=0.04267/(2*r)


vel_act=vel*k
print(vel_act*(960*18)/(fps*5))

print('------------------------------------------------------------------------')
print()
print('velocity : ',vel_act*960/fps,'m/s , theta: ',theta,'deg')
print()
print('------------------------------------------------------------------------')

with open('params.csv', "w",newline='') as f:
    writer = csv.writer(f)
    #writer.writerow([vel_act*960/fps,theta])
    writer.writerow([vel_act*960/fps,theta])
    