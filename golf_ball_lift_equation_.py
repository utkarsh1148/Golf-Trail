import math
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def get_drag_unit_vetor(v_ball,theta,phi,wx,wy,wz):
    fdx=v_ball*math.sin(theta)*wz-v_ball*math.cos(theta)*math.cos(phi)*wy
    fdy=-1*(v_ball*math.cos(theta)*math.sin(phi)*wz-v_ball*math.cos(theta)*math.cos(phi)*wx)
    fdz=(v_ball*math.cos(theta)*math.sin(phi)*wz-v_ball*math.sin(theta)*wx)
    fdx=fdx/math.sqrt(fdx*fdx+fdy*fdy+fdz*fdz)
    fdy=fdy/math.sqrt(fdx*fdx+fdy*fdy+fdz*fdz)
    fdz=fdz/math.sqrt(fdx*fdx+fdy*fdy+fdz*fdz)


    return fdx,fdy,fdz
def sign_(v_,w_):
    if(v_>w_):
        return -1
    else:
        return 1



air_density = 1.168 #kg/m^3 
r=0.021335
area_cross=math.pi*r*r
ball_mass=0.04593

lC=0.18
dC=0.21


wx,wy,wz=0,0,0

g=9.8



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

phi=math.pi/2
if(True):
 print()
 print('------------GOLF BALL SIMULATION-------------------')
 print()
 with open('params.csv', 'r') as f:
    for row in reversed(list(csv.reader(f))):
        vxy=2.236*float(row[0])  #in m/s 
        vxy=math.sqrt((3.16*vxy-5.5)*g/math.sin(2*theta))
        theta=float(row[1])*math.pi/180  # in rad
        v_x.append(vxy*math.cos(theta))
        v_y.append(vxy*math.sin(theta))
        v_z.append(0)
        #print('v',vxy,theta)
        break

delta_t=0.0005

max_height=0
theta=math.atan(v_z[-1] / math.sqrt(v_x[-1]*v_x[-1]+v_y[-1]*v_y[-1]))
phi= math.atan(v_y[-1]/v_x[-1] )

for i in range(2,1000000):

 if(wx !=0 and wy!=0 and wz!=0):
   fdx,fdy,fdz=get_drag_unit_vetor(v[-1],theta,phi,wx,wy,wz)
 else:
     fdx=0
     fdy=0
     fdz=0

 a_drag=((.5*air_density*area_cross*dC)/ball_mass) * ((v[-1])**2.)
 a_lift=((.5*air_density*area_cross*lC)/ball_mass) * ((v[-1])**2.)
 

 a_x= -a_drag*math.cos(theta)*math.sin(phi)+a_lift*(fdx)
 v_x.append( v_x[-1] + a_x*delta_t)
 px.append(px[-1] + v_x[-1]*delta_t)

 
 a_y= -g -  a_drag*(math.sin(theta)) + a_lift*(fdy)
 v_y.append( v_y[-1] + a_y*delta_t)
 py.append( py[-1] + v_y[-1]*delta_t)

 a_z=   a_drag*math.cos(theta)*math.sin(phi) + a_lift*fdz
 v_z.append( v_z[-1] + a_z*delta_t)
 pz.append( pz[-1] + v_z[-1]*delta_t)
 
 v.append( math.sqrt( v_x[-1]**2 + v_y[-1]**2 +v_z[-1]**2))

 theta = math.atan( v_y[-1] / v_x[-1] )
 phi= math.atan( v_z[-1] / math.sqrt(v_x[-1]*v_x[-1]+v_y[-1]*v_y[-1]))

 if(py[-1]>max_height):
     max_height=py[-1]

 last_point = 0
 if( (py[-1]<0) and (last_point == 0)) :
  range_projectile=math.sqrt((px[-1]-px[0])**2+(py[-1]-py[0])**2)
  print('-----------------------------------------------')
  print()
  print('Range of projectile: ',range_projectile,' m ')
  print()
  print('max height: ', max_height)
  print()
  print('------------------------------------------------')
  break

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(px,py,pz)

#ax.set_xlim3d(0, range_projectile+20)
#ax.set_ylim3d(0,max_height+20)
#ax.set_zlim3d(0,max( range_projectile,max_height))

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

with open('params.csv', "a",newline='') as f:
    writer = csv.writer(f)
    writer.writerow([px[-1],0,pz[-1]])

