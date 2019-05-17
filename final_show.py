import csv
import firebase_admin
from firebase_admin import credentials,firestore
import math

def get_lat_and_long(brng,d,lat1,lon1):
    brng=brng*math.pi/180 #Bearing is 90 degrees converted to radians.


    R = 6371e3

    d = d #Distance in km

    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.

    lat1 = lat1 * (math.pi / 180) #Current lat point converted to radians
    lon1 = lon1* (math.pi / 180) #Current long point converted to radians

    lat3 = math.asin( math.sin(lat1)*math.cos(d/R) +
                math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon3 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat3))

    lat3=lat3*180/math.pi
    lon3=lon3*180/math.pi
    return lat3,lon3
def calcualte_distance(lat1,lon1,lat2,lon2):
    R = 6371e3
    φ1 = lat1*math.pi/180
    φ2 = lat2*math.pi/180
    Δφ = (lat2-lat1)*math.pi/180
    Δλ = (lon2-lon1)*math.pi/180

    a = math.sin(Δφ/2) * math.sin(Δφ/2) +math.cos(φ1) * math.cos(φ2) *math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c
    return d
def get_direction_in_deg(lat1,lon1,lat2,lon2):
    alpha=math.atan((lon2-lon1)/(lat2-lat1))*180/math.pi
    return alpha

print()
print('-------------------------- Process Video ------------------------------------------------')
import golf_trail
print()
print('-------------------------- Determining speed of golf ball -------------------------------')
import golf_ball_speed_all
import golf_ball_lift_equation_
print('DONE------> Converting To Realtime coordinates')


with open('params.csv', 'r') as f:
    for row in reversed(list(csv.reader(f))):
        px=float(row[0])
        py=float(row[1])
        pz=float(row[2])
        
        break
cred = credentials.Certificate('./serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
#doc_ref = db.collection(u'users').document(u'alovelace')
#doc_ref.set({  u'first': u'Ada',   u'last': u'Lovelace',   u'born': 1815})
users_ref = db.collection(u'user_demo')
docs = users_ref.get()

if False:
  for doc in docs:
    x=doc.to_dict()

    if(doc.id=='-L_1QfTfEKYe65D9o7FH'):
     goal_hole=(x['goal_hole_location']).split()
     goal_hole=[float(e) for e in goal_hole]

     person_location=(x['person_location']).split()
     person_location=[float(e) for e in person_location]
     print('goal_hole: ',goal_hole,'person_location: ',person_location)
     direction_in_deg=get_direction_in_deg(goal_hole[0],goal_hole[1],person_location[0],person_location[1])
     print('direction in deg: ',direction_in_deg)
else:

  for doc in docs:
    x=doc.to_dict()
    
 
    if(doc.id=='-L_1QfTfEKYe65D9o7FH'):
     person_location_latitude=float((x['latitude']))

     person_location_longitude=float((x['longitude']))
     direction_in_deg=float(x['angle'])
     print('Bearing or direction in deg: ',direction_in_deg)

pz=50
range_ball=math.sqrt((px)**2+(py)**2+(pz)**2)
offset_angle=math.atan(pz/px)*180/math.pi
print('Range ',range_ball,'m ,offset Angle from direction of shot : ',offset_angle,' degree')
if(offset_angle>0):
 golf_lat,golf_lon=get_lat_and_long(direction_in_deg-offset_angle,range_ball,person_location_latitude,person_location_longitude)
else:
 golf_lat,golf_lon=get_lat_and_long(direction_in_deg+offset_angle,range_ball,person_location_latitude,person_location_longitude)
 
print('-------------------------------------------------------------')
print()
print("Position of the golf ball: Latitude:  ",golf_lat,'Longitude: ',golf_lon)
print()
print('-------------------------------------------------------------')

doc_ref = db.collection('users_demo').document('-L_1QfTfEKYe65D9o7FH')
doc_ref.set({  u'angle': direction_in_deg,   u'golf_lat': str(golf_lat) ,u'golf_lon': str(golf_lon),u'latitude':str(person_location_latitude),u'longitude':str(person_location_longitude)})
#doc_ref.set({'golf_lat':golf_lat,'golf_lon':golf_lon}, {SetOptions.merge() })