
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import binascii

X_OFFSET = -81.0;
Y_OFFSET = 107.0;
W = 638;
#H = 333;
PI = math.pi
worldMapName = "WorldMap512"

IMAGE_W = 512;
IMAGE_H = 333;



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
    
    #f = open("TEST_capital_cities.txt", "r")
    f = open("capital_cities.txt", "r")
    lines = f.readlines();
    for line in lines:
        words = line.split('\t')
        #print("words",words)
        city = words[1]
        
        # Longitude
        longitude = float(words[2][:-1])
        #print("longitude",longitude)
        longitudeSign = words[2][-1:]
        if longitudeSign=="S":
            longitude = -longitude
        
        # Latitude
        latitude = float(words[3][:-2])
        latitudeSign = words[3][-2:-1]
        #print("latitudeSign",latitudeSign)
        if latitudeSign=="W":
            latitude = -latitude
            
        #print(country," ", longitude,",", latitude)
        
        cityList.append( [city, longitude, latitude])
 
    return cityList


def projectAndDrawToPicture(cityList):

    # Load map
    img = Image.open(worldMapName+".png")
    img = img.convert("RGB")
    mapImage = img.load()

    # Draw points
    newCityList = []
    for city in cityList:
        color = () 
        if len(city) == 3:
            x,y = millerProject(city[1], city[2])
            color = (255,0 ,0);
            
        if x>=0 and x<IMAGE_W and y>=0 and y<IMAGE_H:
        
            if len(city[0]) > 16:
                print("ERROR! TOO LONG CITY NAME", city[0])
            else:
                city = [city[0], city[1], city[2], x, y]
                newCityList.append(city)
                
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
    
    return newCityList

def millerProject(lat, lon):

    # degrees to radians 
    lon = lon * PI / 180;
    lat =  lat * PI / 180;
    
    x = lon;
    #y = 1.25 * math.log( math.tan( (0.25 * PI) + (0.4 * lat )) );
    y = 1.30 * math.log( math.tan( (0.25 * PI) + (0.4 * lat )) );
    scale = W/PI/2
    x *= scale;
    y *= scale;
    x += W/2;
    y += W/2*0.7331989845
    
    y = IMAGE_H-y
    
    x += X_OFFSET
    y += Y_OFFSET
         
    return x,y
    

### MAIN


cityList = createCityList3()

newCityList = projectAndDrawToPicture(cityList)

#print("cityList",cityList)

# Print CITYDATA.PY


# tile0Pixels = b'\
# \xcc\
# \xcc\
# '


print("# citydata.py")
print("")
print("FORMAT: <city name lenght><city name><x-coordinate 3 bytes><y-coordinate 3 bytes>")
print("citydataBytes= b'\\")

for city in newCityList:
    # Convert name to bytes
    
    # record lenght
    line=""
    cityNameAsBytes = str.encode(city[0])
    recordLen = 3+len(cityNameAsBytes)+3+3
    recordLenInBytes = recordLen.to_bytes(3,'big')
    for i in range(len(recordLenInBytes)): line += "\\x" + "{:02x}".format(recordLenInBytes[i])
    #line = "\\"+hex(len(cityNameAsBytes)+3+3)
    
    # name
    for i in range(len(cityNameAsBytes)): line += "\\x" + "{:02x}".format(cityNameAsBytes[i])
    
    # x-coord
    xInBytes = int(round(city[3])).to_bytes(3,'big')
    for i in range(len(xInBytes)): line += "\\x" + "{:02x}".format(xInBytes[i])

    # y coord
    yInBytes = int(round(city[4])).to_bytes(3,'big')
    for i in range(len(yInBytes)): line += "\\x" + "{:02x}".format(yInBytes[i])  
    
    print(line+"\\")
    
print("'")

    




#print("cities = (")
#
## city coords
#for city in newCityList:
#    #print("city",city)
#    print('    ("',city[0], '", ',int(round(city[3])),', ',int(round(city[4])),'),')
#
#print(")")







