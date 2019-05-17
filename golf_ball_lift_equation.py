import math
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def sign_(v_,w_):
    if(v_>w_):
        return -1
    else:
        return 1



air_density = 1.168 #kg/m^3 
r=0.021335
area_cross=math.pi*r*r
ball_mass=0.04593

w=120*math.pi
lC=0.18
dC=0.21


g=9.8

w_x=0
w_y=0
w_z=0


px=[]
py=[]
pz=[]
px.append(0)
py.append(0)
pz.append(0)


v=[]
v.append(33)

v_x=[]
v_y=[]
v_z=[]



theta=20*math.pi/180
v_x.append(v[-1]*math.cos(theta))
v_y.append(v[-1]*math.sin(theta))
v_z.append(0)
if(True):
 
 with open('params.csv', 'r') as f:
    for row in reversed(list(csv.reader(f))):
        vxy= float(row[0])  #in m/s 
        theta=float(row[1])*math.pi/180  # in rad
        v_x.append(vxy*math.cos(theta))
        v_y.append(vxy*math.sin(theta))
        v_z.append(0)
        #print('v',vxy,theta)
        break

delta_t=0.0005

max_height=0

for i in range(2,1000000):

 

 a_drag=((.5*air_density*area_cross*dC)/ball_mass) * ((v[-1])**2.)
 a_lift=((.5*air_density*area_cross*lC)/ball_mass) * ((v[-1])**2.)
 

 a_x= -a_drag*math.cos(theta)+a_lift*(-math.sin(theta))
 v_x.append( v_x[-1] + a_x*delta_t)
 px.append(px[-1] + v_x[-1]*delta_t)

 
 a_y= -g +  a_drag*(-math.sin(theta)) + a_lift*math.cos(theta)
 v_y.append( v_y[-1] + a_y*delta_t)
 py.append( py[-1] + v_y[-1]*delta_t)

 #a_z= a_drag_z + a_lift_z
 a_z=0
 v_z.append( v_z[-1] + a_z*delta_t)
 pz.append( pz[-1] + v_z[-1]*delta_t)
 
 v.append( math.sqrt( v_x[-1]**2 + v_y[-1]**2 +v_z[-1]**2))

 theta = math.atan( v_y[-1] / v_x[-1] )


 if(py[-1]>max_height):
     max_height=py[-1]

 last_point = 0
 if( (py[-1]<0) and (last_point == 0)) :
  range_projectile=math.sqrt((px[-1]-px[0])**2+(py[-1]-py[0])**2)
  print('range of projectile: ',range_projectile)
  print('max height: ', max_height)
  break

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(px,py,pz)

ax.set_xlim3d(0, range_projectile+20)
ax.set_ylim3d(0,max_height+20)
ax.set_zlim3d(0,max( range_projectile,max_height))

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

with open('params.csv', "a",newline='') as f:
    writer = csv.writer(f)
    writer.writerow([px[-1],0,pz[-1]])

