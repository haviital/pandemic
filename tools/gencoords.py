
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

X_OFFSET = -16.0;
Y_OFFSET = -8.0;
W = 638;
H = 480;
PI = math.pi
worldMapName = "worldmap"


def createCityList():
    
    cityList = [
        ["London",      51.509865, -0.118092],
        ["Zero",        0.0, 0.0],
        ["Paris",      48.85341, 2.3488],
        ["Tampere",    61.49911, 23.787128],
        ["Rome",        41.902782, 12.496366],
        ["Helsinki",    60.192059, 24.945831],
        ["Cape Town",   -33.918861, 18.423300],
        ["Los Angeles", 34.052235, -118.243683],
        ["Buenos Aires",-34.603722, -58.381592],
        ["Melbourne",   -37.840935, 144.946457],
        ["Athens",      37.983810, 23.727539]
    ]
 
    return cityList

# Format:
# Aberdeen, Scotland	57	9 N	2	9 W	5:00 p.m.
def createCityList2():
    
    cityList = []
    
    f = open("biggest_cities.txt", "r")
    lines = f.readlines();
    for line in lines:
        words = line.split('\t')
        print("words",words)
        city = words[0]
        
        # Longitude
        longitudeInt = words[1]
        longitudeDec = words[2].split(' ')[0]
        longitudeSign = "N"
        if len(words[2].split(' '))==2:
            longitudeSign = words[2].split(' ')[1]
        longitude = float(longitudeInt+'.'+longitudeDec)
        if longitudeSign=="S":
            longitude = -longitude
        
        # Latitude
        latitudeInt = words[3]
        latitudeDec = words[4].split(' ')[0]
        latitudeSign = "W"
        if len(words[4].split(' '))==2:
            latitudeSign = words[4].split(' ')[1]
        latitude = float(latitudeInt+'.'+latitudeDec)
        if latitudeSign=="W":
            latitude = -latitude
            
        #print(country," ", longitude,",", latitude)
        
        cityList.append( [city.split(',')[0], longitude, latitude])
 
    return cityList

# Format:
# Brazil	Brasilia	15.47S	47.55W
def createCityList3():
    
    cityList = []
    
    f = open("capital_cities.txt", "r")
    lines = f.readlines();
    for line in lines:
        words = line.split('\t')
        print("words",words)
        city = words[1]
        
        # Longitude
        longitude = float(words[2][:-1])
        print("longitude",longitude)
        longitudeSign = words[2][-1:]
        if longitudeSign=="S":
            longitude = -longitude
        
        # Latitude
        latitude = float(words[3][:-2])
        latitudeSign = words[3][-2:-1]
        print("latitudeSign",latitudeSign)
        if latitudeSign=="W":
            latitude = -latitude
            
        #print(country," ", longitude,",", latitude)
        
        cityList.append( [city, longitude, latitude])
 
    return cityList


def drawToPicture(cityList):

    # Load map
    img = Image.open(worldMapName+".bmp")
    img = img.convert("RGB")
    mapImage = img.load()

    # Draw points
    for city in cityList:
        color = () 
        if len(city) == 3:
            x,y = millerProject(city[1], city[2])
            color = (255,0 ,0);
        else:
            x,y = (city[3], city[4])
            color = (0, 255 ,0);
            
        mapImage[x,y] = color;
        mapImage[x+1,y] = color;
        mapImage[x-1,y] = color;
        mapImage[x,y+1] = color;
        mapImage[x,y-1] = color;
        font = ImageFont.truetype("arial.ttf", 10, encoding="unic")
        draw = ImageDraw.Draw(img)
        draw.text((x+3,y-5), city[0], color, font)

            
    # Save map
    img.save( worldMapName+"_test.png", "PNG" )

def millerProject(lat, lon):

    # degrees to radians 
    lon = lon * PI / 180;
    lat =  lat * PI / 180;
    
    x = lon;
    #y = 1.25 * math.log( math.tan( (0.25 * PI) + (0.4 * lat )) );
    y = 1.35 * math.log( math.tan( (0.25 * PI) + (0.4 * lat )) );
    scale = W/PI/2
    x *= scale;
    y *= scale;
    x += W/2;
    y += W/2*0.7331989845
    
    y = H-y
    
    x += X_OFFSET
    y += Y_OFFSET
         
    return x,y
    

### MAIN

# print("# citydata.py")
# print("")
# print("cities = (")

# # city coords

# #London
# x,y = millerProject(51.509865, -0.118092)
# print('    ("London",', int(round(x)),', ',int(round(y)),'),')

# #zero
# x,y = millerProject(0.0, 0.0)
# print('    ("Zero",', int(round(x)),', ',int(round(y)),'),')

# #paris2
# x,y = millerProject(48.85341, 2.3488)
# print('    ("Paris2",', int(round(x)),', ',int(round(y)),'),')

# #Tampere2
# x,y = millerProject(61.49911, 23.787128)
# print('    ("Tampere2",', int(round(x)),', ',int(round(y)),'),')

# print('    ("Tampere", 282, 75),')
# print('    ("Lahti", 283,76),')
# print('    ("Paris", 240, 110)')

# print(")")

# #x,y = millerProject(100, 100) 
# #print("x=",x,"y=",y)   

cityList = createCityList3()

drawToPicture(cityList)

print("cityList",cityList)



