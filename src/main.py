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
# 26.4.2020 Free ram 7712, Rom size 178 KB, 33 fps. Notes: Added and infection counter and about 200 cities. 
# 28.4.2020 Free ram 7232, Rom size 179 KB, 31 fps. Notes: Added added guides. 
# 4.5.2020  Free ram 7200, Rom size 182 KB, 33 fps. Notes: Added the title screen as an own map 
# 4.5.2020  Free ram 5488, Rom size 188 KB, 38 (emu)fps. Notes: Added mini animations, the game end screen and the bonus screen. 

import umachine
import upygame as pygame
from upygame import TAS
import gc
import data
import worldmap
import gameobject as GameObjects
import sprite
import glob
import citydata
import urandom as random
import minianim
import ui

# Setup the screen buffer
pygame.display.init(False)

# PICO-8 palette
#pygame.display.set_palette_16bit([0x0000, 0x5aa9,  0x0706,0xff7c, 0xf809, 0xbe18, 0x194a, 0x0429, 0x792a, 0xa286, 0xff44,  0x255f, 0x7392, 0xfbb4, 0xfe54])

#pygame.display.set_palette_16bit([0x0000, 0x194a, 0x792a, 0x0429, 0xa286, 0x5aa9, 0xbe18, 0xff7c, 0xf809, 0xfd00, 0xff44, 0x0706, 0x255f, 0x7392, 0xfbb4, 0xfe54])

pygame.display.set_palette_16bit([0x0000, 0x5aa9, 0x0706, 0xff7c, 0xa286, 0x194a, 0xbe18, 0x0429, 0xf809, 0xfd00, 0xff44, 0x792a, 0x255f, 0x7392, 0xfbb4, 0xfe54])

screen = pygame.display.set_mode() # full screen

# Initialize the cookie.
myCookieDataSize = 1 + 3 # Version and high score
myCookieData = bytearray(myCookieDataSize)
myCookie = umachine.Cookie("Pandemic", myCookieData)
myCookie.load()
version=myCookieData[0]
highScore = (myCookieData[1]<<16) + (myCookieData[2]<<8) + myCookieData[3] 

# Initialize sound
sound = pygame.mixer.Sound()
endSoundAtMs = 0
loopSoundAtMs = 0
loopingSoundData = None

# Initialise the world map.
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
targetCityGob = GameObjects.GameObject([data.targetCity6x5_f1, data.targetCity6x5_f2], [[0,0],[0,0]])
targetCityGob.wx = 282-3 
targetCityGob.wy = 75-3
targetCityGob.active = False
all_objects.add(targetCityGob)
all_objects_list.append(targetCityGob)

heroGob = GameObjects.GameObject([data.heroUp_f1, data.heroUp_f2], [[0,0],[0,0]])
dustGob1 = GameObjects.GameObject([data.dustRight_f1, data.dustRight_f2, data.dustRight_f3], [[0,0],[0,0],[0,0]])
dustGob1.animMode = "once"

infectedPeople = GameObjects.GameObject([data.infected_f1, data.infected_f2], [[0,0],[0,0]])
infectedPeople.animDur = 6
infectedPeople.wx = 55-12 
infectedPeople.wy = 88-10
infectedPeople.active = True

# Guide
guideGob = GameObjects.GameObject([data.guideRight, data.guideRight, data.guideRight, data.guideRight], [[0,0], [0,0], [0,0], [0,0]])
guideGob.active = False

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
maxSearchDurationdMs = 15000
#maxSearchDurationdMs = 5000

cityCuredCount = 0
timeBonus = 0
failedCount = 0
currentCityName = ""
allwaysOnGuide = False
planeBoosterEnabled = False


###########################################################    
def TitleScreen():
    
    # Initialise the title map.
    titleMapSizeX = 56 # Must be even
    titleMapSizeY = 100
    titleTilemap = pygame.tilemap.Tilemap(titleMapSizeX,titleMapSizeY,worldmap.titleMapPixels)
    titleTilemap.set_tile(0x0, tileSize, tileSize, data.tile0);
    titleTilemap.set_tile(0x1, tileSize, tileSize, data.tile1);
    titleTilemap.set_tile(0x2, tileSize, tileSize, data.tile2);
    titleTilemap.set_tile(0x3, tileSize, tileSize, data.tile3);
    titleTilemap.set_tile(0x4, tileSize, tileSize, data.tile4);
    titleTilemap.set_tile(0x5, tileSize, tileSize, data.tile5);
    titleTilemap.set_tile(0x6, tileSize, tileSize, data.tile6);
    titleTilemap.set_tile(0x7, tileSize, tileSize, data.tile7);
    titleTilemap.set_tile(0x8, tileSize, tileSize, data.tile8);
    titleTilemap.set_tile(0x9, tileSize, tileSize, data.tile9);
    titleTilemap.set_tile(0xa, tileSize, tileSize, data.tile10);
    titleTilemap.set_tile(0xb, tileSize, tileSize, data.tile11);
    titleTilemap.set_tile(0xc, tileSize, tileSize, data.tile12);
    titleTilemap.set_tile(0xd, tileSize, tileSize, data.tile13);
    titleTilemap.set_tile(0xe, tileSize, tileSize, data.tile14);
    titleTilemap.set_tile(0xf, tileSize, tileSize, data.tile15);

    # Palette
    worldPalette =      [0x0000, 0x5aa9, 0x0706, 0xff7c, 0xa286, 0x194a, 0xbe18, 0x0429, 0xf809, 0xfd00, 0xff44, 0x792a, 0x255f, 0x7392, 0xfbb4, 0xfe54]
    titlePalette =      [0x0000, 0x5aa9, 0x0706, 0xff7c, 0xa286, 0x5aa9, 0xbe18, 0x0000, 0xf809, 0xfd00, 0xff44, 0x0706, 0xffff, 0x7392, 0xfbb4, 0xfe54]
    titleFadedPalette = [0x0000, 0x194a, 0x792a, 0xa286, 0x0000, 0x5aa9, 0xbe18, 0xff7c, 0xf809, 0xfd00, 0xff44, 0x0706, 0x194a, 0x7392, 0xfbb4, 0xfe54]
    pygame.display.set_palette_16bit(titlePalette)
    
    
    
    instructionsPageList = [
        [
        # Page
        #123456789012345678
        "A deadly pandemic ",
        "has spread over ",
        "the world. The ",
        "cities,big and ",
        "small,have closed",
        "borders and try to",
        "survive on their ",
        "own. The strict",
        "isolation makes ",
        "the situation a ",
        "bit better but ",
        "still the pandemic",
        ],
        [
        # Page
        #123456789012345678
        "regularly raises ",
        "its ugly head in",
        "different parts of",
        "the world. Luckily",
        "there is now a",
        "cure for the",
        "disease.",
        "Unfortunately, the",
        "potion is very,",
        "very expensive,",
        "and out of the",
        "reach of all but",
        ],
        [
        # Page
        #123456789012345678
        "the wealthiest",
        "people.You are a ",
        "member of an ",
        "underground,", 
        "anarchistic ",
        "organisation ",
        'called "Bro ',
        'Hodion". It ',
        "makes strikes to",
        "the medicine ",
        "factories and ",
        "steals the potion",
        ],
        [
        # Page
        #123456789012345678
        "Your job is to ",
        "take your air ",
        "vehicle and bring",
        "the potion to the",
        "cities where the",
        "pandemic has ",
        "surfaced.Do not ",
        "get lost as that",
        "would mean that ",
        "the pandemic has ",
        "spread too wide to",
        "save the city!",  
        ],
    ]
    
    creaditsPageList = [
        [
        # Page
        #123456789012345678
        "version 0.5, 2020",
        "",
        "Coding and gfx by", 
        "Hannu Viitala.",
        "Tools and help by",
        "the mighty",
        "Pokitto community!",
        "www.pokitto.com",
        ],
    ]
    
    x = 0
    startScrollY = -((titleMapSizeY*2) - 88 - 1)
    y = startScrollY
    y -= 30  # still image time 
    #y = -20 #!!HV TEST
    y2 = y
    scrollingUp = False
    scrollingDown = True
    #scrollingDown = False
    frameNum = 0
    mini = None
    selectedMode = 3 # just title screen
    nextSelectedMode = 3
    while True:
    
        # 
        now = umachine.time_ms()
        
        # Update here so that the keys are read again in flip() before this comes effective.
        selectedMode = nextSelectedMode
        
        
        # Read keys
        if selectedMode == 3: # show just titlescreen
            eventtype = pygame.event.poll()
            if eventtype != pygame.NOEVENT:
                if eventtype.type == pygame.KEYDOWN:
                    if eventtype.key == pygame.BUT_A:
                        nextSelectedMode = None
    
        # Scroll down screen
        if scrollingDown:
            y += 2
            if y > 0: 
                # Start scrolling up
                y = 0 
                scrollingUp = True
                scrollingDown = False
            y2 = y
            if y<startScrollY: y2 = startScrollY
            
        elif scrollingUp:
            y -= 100 # increase as fixed point number
            y2 = (y // 1000) | 1 # convert fixed point to integer
            #y2 = y2 | 1 # Use only odd coordinates to prevent flicker in dithered areas
            if y2>0: y2 = 0
            if y2 < -20: 
                # stop scroilling
                y2 = -20
                scrollingUp = False
                
        # RAffle a mini anim when stopped moving.
        if (not scrollingUp) and (not scrollingDown):
            # Raffle if not active mini anim exists
            #print("mini==None",mini==None)
            #if mini!=None : print("mini.gob.active",mini.gob.active)
            if mini==None or (not mini.gob.active): 
                mini = minianim.RaffleMiniAnim(screen)
        
        # Draw
        titleTilemap.draw(x, y2)
        
        # Draw minianim
        if mini != None: mini.UpdateAndDraw()
        
        # Draw the dialog according the current mode
        if selectedMode == None: 
            #print("open menu")
            nextSelectedMode = ui.UpdateAndDrawMenu(["Start","Instructions","Credits"])
        elif selectedMode==0:
            # Start game
            #print("Start game")
            pygame.display.set_palette_16bit(worldPalette)
            return
        elif selectedMode==1:
            # Instructions
            if not ui.UpdateAndDrawTextPages(instructionsPageList):
                # Close the dialog
                nextSelectedMode = None   
        elif selectedMode==2:
            # Instructions
            if not ui.UpdateAndDrawTextPages(creaditsPageList):
                # Close the dialog
                nextSelectedMode = None   

        # Periodic processing.
        frameNum += 1
        if( frameNum % 10 == 0 ):
            # Read random numbers so that the seuquence is not the same each time the city is raffled.
            # It depends on how fast the user presses A and goes to the "search" mode.
            random.getrandbits(8)

        pygame.display.flip()
    

###########################################################    
def GameEndScreen():
    
    global cityCuredCount
    global timeBonus
    global highScore

    # Palette
    worldPalette =      [0x0000, 0x5aa9,  0x0706,0xff7c, 0xf809, 0xbe18, 0x194a, 0x0429, 0x792a, 0xa286, 0xff44,  0x255f, 0x7392, 0xfbb4, 0xfe54]
    fadedWorldPalette = [0x0000, 0x5aa9,  0x0706,0xff7c, 0x0000, 0x5aa9, 0xbe18, 0xff7c, 0xf809, 0xfd00, 0xff44, 0x0706, 0x194a, 0x7392, 0xfbb4, 0xfe54]
    pygame.display.set_palette_16bit(fadedWorldPalette)
    
    # If this is the new high score, save it to eeprom
    currentScore = cityCuredCount*10+timeBonus
    if highScore < currentScore:
        highScore = currentScore
        myCookieData[0] = 1 #version
        myCookieData[1] = (highScore >> 16) & 0xff
        myCookieData[2] = (highScore >> 8) & 0xff
        myCookieData[3] = highScore & 0xff
        myCookie.save()
    
    while True:
    
        # Read keys
        eventtype = pygame.event.poll()
        if eventtype != pygame.NOEVENT:
            if eventtype.type == pygame.KEYDOWN:
                if eventtype.key == pygame.BUT_A:
                    # Reset game
                    pygame.display.set_palette_16bit(worldPalette)
                    cityCuredCount = 0
                    points = 0
                    timeBonus = 0
                    failedCount = 0
                    allwaysOnGuide = False
                    planeBoosterEnabled = False
                    
                    return

        # 
        now = umachine.time_ms()
        
        # Draw
        tilemap.draw(-200, 0)
        
        # Draw texts
        textY = 2
        textStepY = 8
        pygame.draw.text(10, textY, "Game over!", 8); textY += textStepY*2
        pygame.draw.text(10, textY, "You found "+str(cityCuredCount)+" cities.", 10); textY += textStepY
        pygame.draw.text(10, textY, "Time bonus: "+str(timeBonus), 10); textY += textStepY
        pygame.draw.text(10, textY, "Total score: "+str(currentScore), 10); textY += textStepY*2
        pygame.draw.text(10, textY, "High score: "+str(highScore), 7); textY += textStepY
        
        # Draw text
        pygame.draw.text(10, 88-10, "A: Start", 9);

        pygame.display.flip()
    


###########################################################    
# Gets a fixed size string from a byte array 
def getStringFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return str(data, "utf-8"), pos+length

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
def RaffleAndShowNewTargetCity():
    
    global currMessageNum
    global messageSwitchAt
    global searchTimeEndAt
    global gameState
    global currentCityName

    # Raffle the next city
    cityNum = random.getrandbits(8)
    #index = index % len(citydata.cities)
    cityNum = cityNum % citydata.numOfCities
    
    currentCityName, cityX, cityY = unpackCityData(cityNum)
    #city = citydata.cities[index]
    
    # Set message texts
    messages[0] = [ currentCityName+"!", 10]
    messages[1] = ["Virus outbreak in", 7] 
    now = umachine.time_ms()
    messageSwitchAt = now + messageDelay
    currMessageNum = 0
    
    # Set the target coordinates
    targetCityGob.wx = cityX-3 
    targetCityGob.wy = cityY-3
    #targetCityGob.active = True
    #targetCityGob.update() # call to calc screen coordinates
    targetCityGob.active = False
    #print("targetCityGob.Active 3",targetCityGob.active)
    
    # Play sound
    now = umachine.time_ms()
    sound.play_sfx(data.alertSfx, len(data.alertSfx), True)
    soundLenMs = len(data.alertSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
    #print("soundLenMs",soundLenMs)
    print("play alert sample")
    loopSoundAtMs = 0
    endSoundAtMs = now + soundLenMs
    
    # Set search end time
    searchTimeEndAt = now+maxSearchDurationdMs
    
    # Show the "virus found"-dialog
    ui.ShowModalDialog(["Virus found.Fly", "the potion to", currentCityName+"."], tilemap, glob.viewPortX, glob.viewPortY)
    gameState = "search"    
   
###########################################################    
def HandleSearchState():
    
    global messageSwitchAt
    global currMessageNum
    global loopSoundAtMs
    global endSoundAtMs
    global cityCuredCount
    global timeBonus
    global failedCount
    global allwaysOnGuide
    global planeBoosterEnabled
  
    # Check timeout
    now = umachine.time_ms()
    if searchTimeEndAt < now:
        
        # City lost! 

        messageSwitchAt = now + messageDelay
        currMessageNum = 0
        
        # Play sound
        sound.play_sfx(data.failedSfx, len(data.failedSfx), True)
        soundLenMs = len(data.failedSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        #print("soundLenMs",soundLenMs)
        loopSoundAtMs = 0
        endSoundAtMs = now + soundLenMs
        print("city lost")

        #        
        ui.ShowModalDialog(["Too many", "infections!", "Mission failed"], tilemap, glob.viewPortX, glob.viewPortY)
        
        # Reset bonuses
        allwaysOnGuide = False
        planeBoosterEnabled = False
        
        # Failed too many times?
        failedCount += 1
        if failedCount>2:
            GameEndScreen() # End the game
        
        RaffleAndShowNewTargetCity()
            
    # Check the distance to the target city
    elif(abs((targetCityGob.wx+2) + (glob.viewPortX-55)) < 5 and abs((targetCityGob.wy+2) + (glob.viewPortY-44)) < 5):
        
        # City found! 

        now = umachine.time_ms()

        # Play sound
        sound.play_sfx(data.succeededSfx, len(data.succeededSfx), True)
        soundLenMs = len(data.succeededSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        #print("soundLenMs",soundLenMs)
        loopSoundAtMs = 0
        endSoundAtMs = now + soundLenMs
        print("target found")
        
        # Stop animating the city
        targetCityGob.currentAnimFrameNum = 0
        targetCityGob.ResetAnimation()
        targetCityGob.animDurCounter = 1000  # big enough for keeping the image still
        targetCityGob.active = False
        #print("targetCityGob.Active 1",targetCityGob.Active)
        
        cityCuredCount += 1
        timePassed = (now + maxSearchDurationdMs) - searchTimeEndAt
        timeBonus += 10 - (10 * timePassed//maxSearchDurationdMs)
        
        # Reset bonuses
        allwaysOnGuide = False
        planeBoosterEnabled = False
        
        #        
        ui.ShowModalDialog(["You made it in", "time! The city", "is now healed."], tilemap, glob.viewPortX, glob.viewPortY)
        
        # Raffle a bonus
        bonus = random.getrandbits(5) # 0-31
        bonus = 2
        if bonus<2:
            # Always on compass
            allwaysOnGuide = True
            ui.ShowModalDialog(["People of ", currentCityName, "grant to you:", "A compass!"], tilemap, glob.viewPortX, glob.viewPortY)
        elif bonus<4:
            # Plane boost
            planeBoosterEnabled = True
            ui.ShowModalDialog(["People of ", currentCityName, "grant to you:", "A turbo boost!"], tilemap, glob.viewPortX, glob.viewPortY)
            
        RaffleAndShowNewTargetCity()

    # Check if the target is near 
    elif(abs((targetCityGob.wx+2) + (glob.viewPortX-55)) < 25 and abs((targetCityGob.wy+2) + (glob.viewPortY-44)) < 25):
        targetCityGob.active = True
        #print("targetCityGob.Active 2",targetCityGob.active)
        targetCityGob.animDurCounter = 3
        targetCityGob.ResetAnimation()
        #print("target near")
        
    
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

        # Reset animation
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

###########################################################    
def DrawUI():
    
    global currMessageNum
    global messageSwitchAt
    
    # draw gauge
    now = umachine.time_ms()
    if gameState == "search":
        screen.blit(infectedPeople.image, 4, 88-12 )
        currenDur = maxSearchDurationdMs - (searchTimeEndAt - now)
        TAS.drawGauge(2, 17, 13, currenDur, maxSearchDurationdMs)

    # Draw guide
    if guideGob.active:
        guideGob.Animate()
        #print("guideGob.currentAnimFrameNum", guideGob.currentAnimFrameNum)
        
        guideGob.rect.x += guideGob.frameOffsets[guideGob.currentAnimFrameNum][0]
        guideGob.rect.y += guideGob.frameOffsets[guideGob.currentAnimFrameNum][1]
        screen.blit(guideGob.image, guideGob.rect.x, guideGob.rect.y, 0, guideGob.hmirror, guideGob.vmirror)

###########################################################    
def UpdateGuide():
    
    # Show the guide only during the last 7 seconds.
    now = umachine.time_ms()
    if searchTimeEndAt > (now + 7000) and not allwaysOnGuide:
        guideGob.active = False
        return
    
    # Use "fixed point" numbers in the calculation by multiplaying by 1000
    heroOnScreenX = 55
    heroOnScreenY = 44
    hx_fp = 1000* heroOnScreenX # Hero world pos x
    hy_fp = 1000* heroOnScreenY # Hero world pos y
    cityOnScreenX = (targetCityGob.wx + glob.viewPortX)
    cityOnScreenY = (targetCityGob.wy + glob.viewPortY)
    deltaOnScreenX = (cityOnScreenX-heroOnScreenX)
    deltaOnScreenY = (cityOnScreenY-heroOnScreenY)
    
    # factor
    k_fp = 1000*1000
    if deltaOnScreenX != 0:
        k_fp = (1000*deltaOnScreenY) // deltaOnScreenX

    # If the target city is not on screen, show the guide.  
    guideGob.active = False
    if deltaOnScreenX > 55 or deltaOnScreenX<-55 or deltaOnScreenY>44 or deltaOnScreenY<-44:
        
        # Store old direction
        oldHMirror = guideGob.hmirror
        oldVMirror = guideGob.vmirror

        if deltaOnScreenX>0:
            # Calc where the line crosses the right edge
            y_fp = k_fp * (110-heroOnScreenX)
            y = (y_fp//1000) + heroOnScreenY
            if y > 0-4 and y < 88+4:
                # draw guide
                guideGob.hmirror = False
                guideGob.vmirror = False
                guideGob.rect.x = 110-8
                guideGob.rect.y = y-4
                guideGob.frames = [data.guideRight, data.guideRight, data.guideRight, data.guideRight]
                guideGob.frameOffsets = [[0,0], [0,0], [0,0], [0,0]]
                guideGob.active = True
        else:
            # Calc where the line crosses the left edge
            y_fp = k_fp * (0-heroOnScreenX)
            y = (y_fp//1000) + heroOnScreenY
            if y > 0-4 and y < 88+4:
                # draw guide
                guideGob.hmirror = True
                guideGob.vmirror = False
                guideGob.rect.x = 0
                guideGob.rect.y = y-4
                guideGob.frames = [data.guideRight, data.guideRight, data.guideRight, data.guideRight]
                guideGob.frameOffsets = [[0,0], [0,0], [0,0], [0,0]]
                guideGob.active = True    
                
        #print("guideGob.active",guideGob.active)
        if guideGob.active == False:
            # inversed factor
            kInverse_fp = (1000*deltaOnScreenX) // deltaOnScreenY
            #print("test1")
            
            if deltaOnScreenY>0:
                # Calc where the line crosses the bottom edge
                x_fp = kInverse_fp * (88-heroOnScreenY)
                x = (x_fp//1000) + heroOnScreenX
                if x > 0-4 and x < 110+4:
                    # draw guide
                    guideGob.hmirror = False
                    guideGob.vmirror = False
                    guideGob.rect.x = x-5
                    guideGob.rect.y = 88-6
                    guideGob.frames = [data.guideBottom, data.guideBottom, data.guideBottom, data.guideBottom]
                    guideGob.frameOffsets = [[0,0], [0,0], [0,0], [0,0]]
                    guideGob.active = True    
                    #print("test2")
            else:
                # Calc where the line crosses the top edge
                x_fp = kInverse_fp * (0-heroOnScreenY)
                x = (x_fp//1000) + heroOnScreenX
                if x > 0-4 and x < 110+4:
                    # draw guide
                    guideGob.hmirror = False
                    guideGob.vmirror = True
                    guideGob.rect.x = x-5
                    guideGob.rect.y = 0
                    guideGob.frames = [data.guideBottom, data.guideBottom, data.guideBottom, data.guideBottom]
                    guideGob.frameOffsets = [[0,0], [0,0], [0,0], [0,0]]
                    guideGob.active = True    
                    #print("test3")
  
        # Reset animation only if direction has been changed
        if guideGob.active == True and (oldHMirror != guideGob.hmirror or oldVMirror != guideGob.hmirror):
            guideGob.ResetAnimation()




##########################################################
# Main loop

#
pygame.draw.set_transparent_color(0)
pygame.draw.set_background_color(0)

#
TitleScreen()

#
RaffleAndShowNewTargetCity()

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
    if planeBoosterEnabled:
        glob.viewPortX += viewPortVelX*2
        glob.viewPortY += viewPortVelY*2
    else:
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
    
    # Draw messages the counter and the guide
    DrawUI()
    
    # Fps
    if( frameNum % 50 == 0 ):
        
        #FPS
        now = umachine.time_ms()
        fps = 50000 // (now-lastTimeFps)
        lastTimeFps = now
        
        # Get free RAM
        gc.collect()
        freeRam = gc.mem_free()
        
    # Periodic processing.
    if( frameNum % 10 == 0 ):
        if gameState == "search":
            UpdateGuide()
        else:
            # Read random numbers so that the seuquence is not the same each time the city is raffled.
            # It depends on how fast the user presses A and goes to the "search" mode.
            random.getrandbits(8)

        #print("gameState",gameState)
    
    # print    
    text = str(fps) +" "+str(freeRam)
    #pygame.draw.text(0, 0, text, 6);
    frameNum += 1
    
    pygame.display.flip()
    
    