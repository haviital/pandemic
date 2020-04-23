
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#CENTRAL_MERIDIAN_OFFSET = -79.0;
#CENTRAL_LATITUDE_OFFSET = -294.0;
X_OFFSET = -18.0;
Y_OFFSET = -8.0;
W = 638;
H = 480;
PI = math.pi
worldMapName = "worldmap"


def createCityList():
    
    cityList = [
        ["London",      51.509865, -0.118092],
        ["Zero",        0.0, 0.0],
        ["Paris2",      48.85341, 2.3488],
        ["Paris",       0, 0,                   240+79.0, 110+0.0],
        ["Tampere2",    61.49911, 23.787128],
        ["Tampere",     0,0,                    282+79.0, 75+0.0],
        ["Lahti",      51.509865, -0.118092,    283+79.0, 76+0.0]
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
    y = 1.25 * math.log( math.tan( 0.25 * PI + 0.4 * lat ) );
    
    x = ( W / 2 ) + ( W / (2 * PI) ) * x;
    #Northern hemisphere behaves differently from southern hemisphere
    #most likely from floating point precision errors
    #this helps compensate for the difference
    if lon > 0.0:
        y = H - (( H / 2 ) - ( H / ( 2 * 2.303412543 ) ) * y)
    else:
        y = H - (( H / 2 ) - ( H / ( 2 * 2.11896 ) ) * y)
        
    x += X_OFFSET
        
    y = H - y    
    y += Y_OFFSET
    
    return x,y
    

### MAIN

print("# citydata.py")
print("")
print("cities = (")

# city coords

#London
x,y = millerProject(51.509865, -0.118092)
print('    ("London",', int(round(x)),', ',int(round(y)),'),')

#zero
x,y = millerProject(0.0, 0.0)
print('    ("Zero",', int(round(x)),', ',int(round(y)),'),')

#paris2
x,y = millerProject(48.85341, 2.3488)
print('    ("Paris2",', int(round(x)),', ',int(round(y)),'),')

#Tampere2
x,y = millerProject(61.49911, 23.787128)
print('    ("Tampere2",', int(round(x)),', ',int(round(y)),'),')

print('    ("Tampere", 282, 75),')
print('    ("Lahti", 283,76),')
print('    ("Paris", 240, 110)')

print(")")

#x,y = millerProject(100, 100) 
#print("x=",x,"y=",y)   

cityList = createCityList()

drawToPicture(cityList)


