# Copyright (C) 2020 Hannu Viitala
#
# The source code in this file is released under the MIT license.
# Go to http://opensource.org/licenses/MIT for the full license details.
#

# *** PANDEMIC GAME ***

# 9.4.2020 Free ram 12528, Rom size 159 KB, 38 fps
# 9.4.2020 Free ram 12224, Rom size 159 KB, 38 fps
# 9.4.2020 Free ram 12224, Rom size 164 KB, 38 fps. Notes: added sprite and gameobject classes
# 9.4.2020 Free ram 9696, Rom size 165 KB, 38 fps. Notes: added hero and target gobs, and animated bitmaps
# 9.4.2020 Free ram 9536, Rom size 165 KB, 38 fps. Notes: added separate bitmaps for up and right positions
# 10.4.2020 Free ram 9168, Rom size 167 KB, 33 fps. Notes: Added plane sfx.
# 11.4.2020 Free ram 9168, Rom size 173 KB, 33 fps. Notes: Added 3 more  sound effects.
# 12.4.2020 Free ram 8448, Rom size 174 KB, 33 fps. Notes: Added dust trails

import umachine
import upygame as pygame
import gc
import data
import worldmap
import gameobject as GameObjects
import sprite
import glob
import citydata
import urandom as random

# Setup the screen buffer
pygame.display.init(False)

# PICO-8 palette
pygame.display.set_palette_16bit([0x0000, 0x194a, 0x792a, 0x0429, 0xa286, 0x5aa9, 0xbe18, 0xff7c, 0xf809, 0xfd00, 0xff44, 0x0706, 0x255f, 0x7392, 0xfbb4, 0xfe54]);

screen = pygame.display.set_mode() # full screen

# Initialize sound
sound = pygame.mixer.Sound()
endSoundAtMs = 0
loopSoundAtMs = 0
loopingSoundData = None

# Initialise the mp.
tileSize = 2
mapSizeX = 256
mapSizeY = 166
tilemap = pygame.tilemap.Tilemap(mapSizeX,mapSizeY,worldmap.WorldMap512TilemapPixels)
tilemap.set_tile(0x0, tileSize, tileSize, data.tile0);
tilemap.set_tile(0x1, tileSize, tileSize, data.tile1);
tilemap.set_tile(0x2, tileSize, tileSize, data.tile2);
tilemap.set_tile(0x3, tileSize, tileSize, data.tile3);
tilemap.set_tile(0x4, tileSize, tileSize, data.tile4);
tilemap.set_tile(0x5, tileSize, tileSize, data.tile5);
tilemap.set_tile(0x6, tileSize, tileSize, data.tile6);
tilemap.set_tile(0x7, tileSize, tileSize, data.tile7);
tilemap.set_tile(0x8, tileSize, tileSize, data.tile8);
tilemap.set_tile(0x9, tileSize, tileSize, data.tile9);
tilemap.set_tile(0xa, tileSize, tileSize, data.tile10);
tilemap.set_tile(0xb, tileSize, tileSize, data.tile11);
tilemap.set_tile(0xc, tileSize, tileSize, data.tile12);
tilemap.set_tile(0xd, tileSize, tileSize, data.tile13);
tilemap.set_tile(0xe, tileSize, tileSize, data.tile14);
tilemap.set_tile(0xf, tileSize, tileSize, data.tile15);

# Setup global variables
glob.viewPortX = 0
glob.viewPortY = 0

# setup sprite group
all_objects = sprite.Group()
all_objects_list = []

#Init game objects
heroGob = GameObjects.GameObject([data.heroUp_f1, data.heroUp_f2], [[0,0],[0,0]])
dustGob1 = GameObjects.GameObject([data.dustRight_f1, data.dustRight_f2, data.dustRight_f3], [[0,0],[0,0],[0,0]])
dustGob1.animMode = "once"

targetCityGob = GameObjects.GameObject([data.targetCity6x5_f1, data.targetCity6x5_f2], [[0,0],[0,0]])
targetCityGob.wx = 282-3 
targetCityGob.wy = 75-3
targetCityGob.active = False
all_objects.add(targetCityGob)
all_objects_list.append(targetCityGob)

infectedPeople = GameObjects.GameObject([data.infected_f1, data.infected_f2], [[0,0],[0,0]])
infectedPeople.animDur = 6
infectedPeople.wx = 55-12 
infectedPeople.wy = 88-10
infectedPeople.active = True

targetCityGob = GameObjects.GameObject([data.targetCity6x5_f1, data.targetCity6x5_f2], [[0,0],[0,0]])
targetCityGob.wx = 282-3 
targetCityGob.wy = 75-3
targetCityGob.active = False
all_objects.add(targetCityGob)
all_objects_list.append(targetCityGob)


gameState = "wait"
redrawDustAt1 = 0

# The main loop
viewPortVelX = 0;
viewPortVelY = 0;
#x = -120;
#y = -100;
#x = 0;
#y = 0;
mapW = mapSizeX*tileSize # 24 tiles of 16 pixels
mapH = mapSizeY*tileSize # 24 tiles of 16 pixels
screenW = screen.get_rect().width
screenH = screen.get_rect().height
heroOnScreenX = screenW // 2
heroOnScreenY = screenH // 2

frameNum = 1
fps = 0
lastTimeFps = umachine.time_ms()
freeRam = 0
seaState = 0
messages = [
    ["Virus outbreak in", 7],
    ["xxx!", 10]
]
messageDelay = 2000
messageSwitchAt = umachine.time_ms() + messageDelay
currMessageNum = 0
searchTimeEndAt = 0

###########################################################    
def DrawMessagePanel():
    
    global currMessageNum
    global messageSwitchAt
    
    # Draw panel
    screen.blit(data.panelLeftEnd, 1, 1)
    screen.blit(data.panelMiddle, 1+6, 1)
    screen.blit(data.panelMiddle, 1+6+32, 1)
    screen.blit(data.panelMiddle, 1+6+32+32, 1)
    screen.blit(data.panelLeftEnd, 110-1-6, 1, 0, True)
  
    # Draw message
    now = umachine.time_ms()
    if messageSwitchAt != 0 and messageSwitchAt < now:
        # time to switch message
        if currMessageNum==0 and len(messages[1][0]) > 0:
            currMessageNum = 1
        else: 
            if currMessageNum==1 and len(messages[0][0]) > 0: 
                currMessageNum = 0
        messageSwitchAt = now + messageDelay
        
    pygame.draw.text(6, 2, messages[currMessageNum][0], messages[currMessageNum][1]);
    
    if gameState == "search":
        # Draw panel
        x = infectedPeople.wx
        y = infectedPeople.wy
        screen.blit(data.panelLeftEnd, x-5, y-1)
        screen.blit(data.panelMiddle,  x-5+6, y-1)
        screen.blit(data.panelLeftEnd, x-5+6+32, y-1, 0, True)
        screen.blit(infectedPeople.image, x, y )
        
        timePassed = ((now + 10000) - searchTimeEndAt) // 100
        pygame.draw.text(x+infectedPeople.image.get_rect().width+2, y, str(timePassed));
        
###########################################################    
# Gets a fixed size string from a byte array 
def getStringFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return str(data, "utf-8"), pos+length

###########################################################    
# Gets an integer from a byte array 
def getIntFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return int.from_bytes(data, 'big'), pos+length
        
###########################################################    
def unpackCityData(cityNum):
    
    currIndex=0
    currentCityNum = 0
    recordLen = 0
    while(True):
        #dataLen = int(citydata.citydataBytes[0])
        #recordLen, newPos = getIntFromByteArray( citydata.citydataBytes, currIndex, 3)
        newPos = currIndex
        recordLen = citydata.citydataBytes[newPos]
        newPos += 1
        if cityNum == currentCityNum:
            
            print("cityNum",cityNum,"currentCityNum",currentCityNum)
            
            #Uncompress city record
            print("recordLen=", recordLen)
            nameLen = recordLen - 1 - 2 - 2
            print("recordLen=", recordLen,"nameLen",nameLen)
            name, newPos = getStringFromByteArray( citydata.citydataBytes, newPos, nameLen)
            #x, newPos = getIntFromByteArray( citydata.citydataBytes, newPos, 3)
            x = 256*citydata.citydataBytes[newPos] + citydata.citydataBytes[newPos+1]
            y = 256*citydata.citydataBytes[newPos+2] + citydata.citydataBytes[newPos+3]
            #y, newPos = getIntFromByteArray( citydata.citydataBytes, newPos, 3)
            
            print("name=", name, "x=", x, "y=", y)
            
            break
        else:
            currIndex += recordLen
            currentCityNum += 1
    
    return name, x, y
    
###########################################################    
def RaffleTargetCity():
    
    global currMessageNum
    global messageSwitchAt
    global searchTimeEndAt
    global gameState

    # Raffle the next city
    cityNum = random.getrandbits(8)
    #index = index % len(citydata.cities)
    cityNum = cityNum % 200
    
    #cityName, cityX, cityY = uncompressCityData(cityNum)
    cityName, cityX, cityY = unpackCityData(0)
    #city = citydata.cities[index]
    
    # Set message texts
    messages[0] = ["Virus outbreak in", 7] 
    messages[1] = [ cityName+"!", 10]
    now = umachine.time_ms()
    messageSwitchAt = now + messageDelay
    currMessageNum = 0
    
    # Set the target coordinates
    targetCityGob.wx = cityX-3 
    targetCityGob.wy = cityY-3
    targetCityGob.active = False
    
    # Play sound
    now = umachine.time_ms()
    sound.play_sfx(data.alertSfx, len(data.alertSfx), True)
    soundLenMs = len(data.alertSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
    #print("soundLenMs",soundLenMs)
    print("play alert sample")
    loopSoundAtMs = 0
    endSoundAtMs = now + soundLenMs
    
    # Set search end time
    searchTimeEndAt = now+10000
    
    gameState = "search"
   
###########################################################    
def HandleSearchState():
    
    global messageSwitchAt
    global currMessageNum
    global loopSoundAtMs
    global endSoundAtMs
    global gameState
  
    # Check timeout
    now = umachine.time_ms()
    if searchTimeEndAt < now:
        
        # City lost! 

        messages[0] = ["Not enough medicine", 7] 
        messages[1] = [ "City lost!", 7]
        
        messageSwitchAt = now + messageDelay
        currMessageNum = 0
        
        # Play sound
        sound.play_sfx(data.failedSfx, len(data.failedSfx), True)
        soundLenMs = len(data.failedSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        #print("soundLenMs",soundLenMs)
        loopSoundAtMs = 0
        endSoundAtMs = now + soundLenMs
        print("city lost")
        
        gameState = "wait"
    
    # Check the distance to the target city
    elif(abs(targetCityGob.wx + (glob.viewPortX-55)) < 10 and abs(targetCityGob.wy + (glob.viewPortY-44)) < 10):
        
        # City found! 

        messages[0] = ["Medicine delivered", 7] 
        messages[1] = [ "People survived!", 7]
        now = umachine.time_ms()
        messageSwitchAt = now + messageDelay
        currMessageNum = 0
        
        # Play sound
        sound.play_sfx(data.succeededSfx, len(data.succeededSfx), True)
        soundLenMs = len(data.succeededSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        #print("soundLenMs",soundLenMs)
        loopSoundAtMs = 0
        endSoundAtMs = now + soundLenMs
        print("target found")
        
        gameState = "wait"

    elif(abs(targetCityGob.wx + (glob.viewPortX-55)) < 20 and abs(targetCityGob.wy + (glob.viewPortY-44)) < 20):
        targetCityGob.active = True
        print("target near")
        
    
###########################################################    
def DrawHero():
    
    global redrawDustAt1

    # Draw dust
    now = umachine.time_ms()
    if viewPortVelX!=0 or viewPortVelY!=0: 
        if redrawDustAt1==0:
            # Start drawing dust
            redrawDustAt1 = 1 
            if viewPortVelX != 0 :
                dustGob1.frames = [data.dustRight_f1, data.dustRight_f2, data.dustRight_f3]
            if viewPortVelY != 0 :  # plane down
                dustGob1.frames = [data.dustUp_f1, data.dustUp_f2, data.dustUp_f3]

    else: redrawDustAt1 = 0 # Stop drawing dust

    # Dust1 : If the times has elapsed, set the new coordinates
    if redrawDustAt1 != 0 and redrawDustAt1 < now:
        if viewPortVelX < 0:  # plane right
            dustGob1.wx = -glob.viewPortX + 49 - dustGob1.image.get_rect().width + 1
            dustGob1.wy = -glob.viewPortY + 41
        if viewPortVelX > 0:  # plane left
            dustGob1.wx = -glob.viewPortX + 49 + heroGob.image.get_rect().width - 1
            dustGob1.wy = -glob.viewPortY + 41
        if viewPortVelY < 0:  # plane down
            dustGob1.wx = -glob.viewPortX + 53
            dustGob1.wy = -glob.viewPortY + 38 - dustGob1.image.get_rect().height + 1
        if viewPortVelY > 0:  # plane up
            dustGob1.wx = -glob.viewPortX + 53
            dustGob1.wy = -glob.viewPortY + 38 + heroGob.image.get_rect().height - 1

        # Reset animationy
        dustGob1.currentAnimFrameNum = 0
        dustGob1.ResetAnimation()
        
        dustGob1.update();    
        
        redrawDustAt1 = now + 200
        #redrawDustAt2 = now + 150
     
    # if moving, draw the dust
    if redrawDustAt1 > 0:   
        screen.blit(dustGob1.image, dustGob1.rect.x,  dustGob1.rect.y, 0, heroGob.hmirror, heroGob.vmirror)

    # Draw Hero
    screen.blit(heroGob.image, 49, 38, 0, heroGob.hmirror, heroGob.vmirror)

##########################################################
# Main loop

RaffleTargetCity()

while True:

    # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:
        if eventtype.type == pygame.KEYDOWN:
            if eventtype.key == pygame.K_RIGHT: 
                viewPortVelX = -1
                viewPortVelY = 0
                heroGob.hmirror = False
                heroGob.vmirror = False
                heroGob.frames = [data.heroRight_f1, data.heroRight_f2]
            if eventtype.key == pygame.K_LEFT:  
                viewPortVelX = 1
                viewPortVelY = 0
                heroGob.hmirror = True
                heroGob.vmirror = False
                heroGob.frames = [data.heroRight_f1, data.heroRight_f2]
            if eventtype.key == pygame.K_UP:    
                viewPortVelY = 1
                viewPortVelX = 0
                heroGob.hmirror = False
                heroGob.vmirror = False
                heroGob.frames = [data.heroUp_f1, data.heroUp_f2]
            if eventtype.key == pygame.K_DOWN:  
                viewPortVelY = -1
                viewPortVelX = 0
                heroGob.hmirror = False
                heroGob.vmirror = True
                heroGob.frames = [data.heroUp_f1, data.heroUp_f2]
            if eventtype.key == pygame.BUT_A: 
                # Raffle a new city
                RaffleTargetCity()
                
        if eventtype.type == pygame.KEYUP:
            if eventtype.key == pygame.K_RIGHT: viewPortVelX = 0
            if eventtype.key == pygame.K_LEFT:  viewPortVelX = 0
            if eventtype.key == pygame.K_UP:    viewPortVelY = 0
            if eventtype.key == pygame.K_DOWN:  viewPortVelY = 0

    #
    if gameState == "search":
        HandleSearchState()
        

    # Handle loping sound start and end
    if viewPortVelX==0 and viewPortVelY==0:
        # Hero is not moving, do not loop the sfx any more.
        loopSoundAtMs=0 # end looping
    elif loopSoundAtMs==0 and endSoundAtMs==0: # Play only if a single shot sfx is noi playing
        # The plane is moving, start playing the motor sfx
        loopingSoundData = data.motorSfx
        soundLenMs = len(loopingSoundData)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        loopSoundAtMs = now + soundLenMs
        #print("start play looping sample")
        
    # Play sound effects
    
    # Non-looping sfx has higher priority
    if endSoundAtMs!=0 and now>endSoundAtMs: endSoundAtMs = 0 #ended
    
    # Looping sfx
    now = umachine.time_ms()
    if endSoundAtMs==0 and loopSoundAtMs!=0 and now>loopSoundAtMs:
        sound.play_sfx(loopingSoundData, len(loopingSoundData), True)
        soundLenMs = len(loopingSoundData)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        #print("play looping sample")
        loopSoundAtMs = now + soundLenMs

    # Move.
    oldX = glob.viewPortX
    oldY = glob.viewPortY
    glob.viewPortX += viewPortVelX
    glob.viewPortY += viewPortVelY

    # Update
    heroGob.update()
    dustGob1.update()
    all_objects.update()
    infectedPeople.update()
    
    # Draw
    tilemap.draw(glob.viewPortX, glob.viewPortY)
    
    # Draw enemies
    all_objects.draw(screen)

    # Draw hero in the center of the screen.
    DrawHero()
    
    # Draw messages
    DrawMessagePanel()

    # Fps
    if( frameNum % 50 == 0 ):
        
        #FPS
        now = umachine.time_ms()
        fps = 50000 // (now-lastTimeFps)
        lastTimeFps = now
        
        # Get free RAM
        gc.collect()
        freeRam = gc.mem_free()
        
        #print("gameState",gameState)
    
    # print    
    text = str(fps)+" "+str(freeRam)
    pygame.draw.text(0, 88-6, text, 6);
    #pygame.draw.text(0, 0, str(fps), 7);
    frameNum += 1
    
    pygame.display.flip()
    
    