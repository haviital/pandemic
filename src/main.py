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
# 11.4.2020 Free ram 9168, Rom size 173 KB, 32 fps. Notes: Added 3 more  sound effects.

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

targetCityGob = GameObjects.GameObject([data.targetCity6x5_f1, data.targetCity6x5_f2], [[0,0],[0,0]])
targetCityGob.wx = 282-3 
targetCityGob.wy = 75-3
targetCityGob.active = False
all_objects.add(targetCityGob)
all_objects_list.append(targetCityGob)
gameState = "wait"


# The main loop
vx = 0;
vy = 0;
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

###########################################################    
def DrawMessagePanel():
    
    global currMessageNum
    global messageSwitchAt
    
    # Draw panel
    screen.blit(data.panelLeftEnd6x12, 1, 1)
    screen.blit(data.panelMiddle32x12, 1+6, 1)
    screen.blit(data.panelMiddle32x12, 1+6+32, 1)
    screen.blit(data.panelMiddle32x12, 1+6+32+32, 1)
    screen.blit(data.panelLeftEnd6x12, 110-1-6, 1, 0, True)
  
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
        
    pygame.draw.text(6, 3, messages[currMessageNum][0], messages[currMessageNum][1]);

###########################################################    
def RaffleTargetCity():
    
    global currMessageNum
    global messageSwitchAt
    global gameState

    # Raffle the next city
    index = random.getrandbits(8)
    index = index % len(citydata.cities)
    city = citydata.cities[index]
    
    # Set message texts
    messages[0] = ["Virus outbreak in", 7] 
    messages[1] = [ city[0]+"!", 10]
    now = umachine.time_ms()
    messageSwitchAt = now + messageDelay
    currMessageNum = 0
    
    # Set the target coordinates
    targetCityGob.wx = city[1]-3 
    targetCityGob.wy = city[2]-3
    targetCityGob.active = False
    
    # Play sound
    now = umachine.time_ms()
    sound.play_sfx(data.alertSfx, len(data.alertSfx), True)
    soundLenMs = len(data.alertSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
    #print("soundLenMs",soundLenMs)
    print("play alert sample")
    loopSoundAtMs = 0
    endSoundAtMs = now + soundLenMs
    
    gameState = "search"
   

##########################################################
# Main loop

RaffleTargetCity()

while True:

    # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:
        if eventtype.type == pygame.KEYDOWN:
            if eventtype.key == pygame.K_RIGHT: 
                vx = -1
                heroGob.hmirror = False
                heroGob.vmirror = False
                heroGob.frames = [data.heroRight_f1, data.heroRight_f2]
            if eventtype.key == pygame.K_LEFT:  
                vx = 1
                heroGob.hmirror = True
                heroGob.vmirror = False
                heroGob.frames = [data.heroRight_f1, data.heroRight_f2]
            if eventtype.key == pygame.K_UP:    
                vy = 1
                heroGob.hmirror = False
                heroGob.vmirror = False
                heroGob.frames = [data.heroUp_f1, data.heroUp_f2]
            if eventtype.key == pygame.K_DOWN:  
                vy = -1
                heroGob.hmirror = False
                heroGob.vmirror = True
                heroGob.frames = [data.heroUp_f1, data.heroUp_f2]
            if eventtype.key == pygame.BUT_A: 
                # Raffle a new city
                RaffleTargetCity()
                
        if eventtype.type == pygame.KEYUP:
            if eventtype.key == pygame.K_RIGHT: vx = 0
            if eventtype.key == pygame.K_LEFT:  vx = 0
            if eventtype.key == pygame.K_UP:    vy = 0
            if eventtype.key == pygame.K_DOWN:  vy = 0

    if gameState == "search":
        
        # Check the distance to the target city
        if(abs(targetCityGob.wx + (glob.viewPortX-55)) < 3 and abs(targetCityGob.wy + (glob.viewPortY-44)) < 3):
            
            # City found! 
    
            messages[0] = ["Medicine delivered", 7] 
            messages[1] = [ "People survived!", 7]
            now = umachine.time_ms()
            messageSwitchAt = now + messageDelay
            currMessageNum = 0
            
            # Play sound
            now = umachine.time_ms()
            sound.play_sfx(data.succeededSfx, len(data.succeededSfx), True)
            soundLenMs = len(data.succeededSfx)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
            #print("soundLenMs",soundLenMs)
            print("play succeededSfx")
            loopSoundAtMs = 0
            endSoundAtMs = now + soundLenMs
            
            gameState = "wait"
    
        elif(abs(targetCityGob.wx + (glob.viewPortX-55)) < 20 and abs(targetCityGob.wy + (glob.viewPortY-44)) < 20):
            targetCityGob.active = True

    # Handle loping sound start and end
    if vx==0 and vy==0:
        # Hero is not moving, do not loop the sfx any more.
        loopSoundAtMs=0 # end looping
    elif loopSoundAtMs==0 and endSoundAtMs==0: # Play only if a single shot sfx is noi playing
        # The plane is moving, start playing the motor sfx
        loopingSoundData = data.motorSfx
        soundLenMs = len(loopingSoundData)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        loopSoundAtMs = now + soundLenMs
        print("start play looping sample")
        
    # Play sound effects
    
    # Non-looping sfx has higher priority
    if endSoundAtMs!=0 and now>endSoundAtMs: endSoundAtMs = 0 #ended
    
    # Looping sfx
    now = umachine.time_ms()
    if endSoundAtMs==0 and loopSoundAtMs!=0 and now>loopSoundAtMs:
        sound.play_sfx(loopingSoundData, len(loopingSoundData), True)
        soundLenMs = len(loopingSoundData)*2//8  # len at 8 kHz, 4-bit data i.e. 2 samples per byte
        print("play looping sample")
        loopSoundAtMs = now + soundLenMs

    # Move.
    oldX = glob.viewPortX
    oldY = glob.viewPortY
    glob.viewPortX += vx
    glob.viewPortY += vy

    # Update
    heroGob.update()
    all_objects.update()

    # Draw
    tilemap.draw(glob.viewPortX, glob.viewPortY)
    
    # Draw enemies
    all_objects.draw(screen)

    # Draw hero in the center of the screen.
    screen.blit(heroGob.image, 49, 38, 0, heroGob.hmirror, heroGob.vmirror)
    
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
        
        print("gameState",gameState)
    
    # print    
    text = str(fps)+" "+str(freeRam)
    pygame.draw.text(0, 88-6, text, 6);
    #pygame.draw.text(0, 0, str(fps), 7);
    frameNum += 1
    
    pygame.display.flip()
    
    