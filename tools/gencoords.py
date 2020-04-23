
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

cityList = createCityList()

drawToPicture(cityList)


