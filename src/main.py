# Copyright (C) 2020 Hannu Viitala
#
# The source code in this file is released under the MIT license.
# Go to http://opensource.org/licenses/MIT for the full license details.
#

# *** PANDEMIC GAME ***

import umachine
import upygame as pygame
import gc
import data
import worldmap

# Setup the screen buffer
pygame.display.init(False)

# PICO-8 palette
pygame.display.set_palette_16bit([0x0000, 0x194a, 0x792a, 0x0429, 0xa286, 0x5aa9, 0xbe18, 0xff7c, 0xf809, 0xfd00, 0xff44, 0x0706, 0x255f, 0x7392, 0xfbb4, 0xfe54]);

screen = pygame.display.set_mode() # full screen

#


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

#tilemap.set_tile(0xb, tileSize, tileSize, data.green16);
#tilemap.set_tile(0x5, tileSize, tileSize, data.tree16);
#tilemap.set_tile(0x4, tileSize, tileSize, data.grass16);
#tilemap.set_tile(0x8, tileSize, tileSize, data.water16);

# The main loop
vx = 0;
vy = 0;
#x = -120;
#y = -100;
x = 0;
y = 0;
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

while True:

    # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:
        if eventtype.type == pygame.KEYDOWN:
            if eventtype.key == pygame.K_RIGHT: vx = -1
            if eventtype.key == pygame.K_LEFT:  vx = 1
            if eventtype.key == pygame.K_UP:    vy = 1
            if eventtype.key == pygame.K_DOWN:  vy = -1
            if eventtype.key == pygame.BUT_A: 
                seaState += 1
                if seaState > 4: seaState = 0
                if seaState == 0: tilemap.set_tile(0x0, tileSize, tileSize, data.tile0);
                if seaState == 1: tilemap.set_tile(0x0, tileSize, tileSize, data.tile1);
                if seaState == 2: tilemap.set_tile(0x0, tileSize, tileSize, data.tile9);
                if seaState == 3: tilemap.set_tile(0x0, tileSize, tileSize, data.tile10);
                if seaState == 4: tilemap.set_tile(0x0, tileSize, tileSize, data.tile8);
                
        if eventtype.type == pygame.KEYUP:
            if eventtype.key == pygame.K_RIGHT: vx = 0
            if eventtype.key == pygame.K_LEFT:  vx = 0
            if eventtype.key == pygame.K_UP:    vy = 0
            if eventtype.key == pygame.K_DOWN:  vy = 0

    # Move.
    oldX = x
    oldY = y
    x += vx
    y += vy

    # Check the map tile under the girl.
    girlCenterInMapX = (heroOnScreenX + 6) - x
    girlCerterInMapY = (heroOnScreenY + 7) - y
    tileId = tilemap.get_tile_id(girlCenterInMapX, girlCerterInMapY, tileSize)

    # If the tile is not grass, do not move.
    #if(tileId != 0xb):
    #    x = oldX
    #    y = oldY

    # Check for out of bounds.
    #if(x>0): x=0
    #if(x + mapW < screenW): x = screenW - mapW
    #if(y>0): y=0
    #if(y + mapH < screenH): y = screenH - mapH

    # Draw
    tilemap.draw(x, y)
    #pygame.draw.text(0, 0, "Tilemap TAS demo", 15);
    screen.blit(data.girl12x15, heroOnScreenX, heroOnScreenY)
    
    # Fps
    if( frameNum % 50 == 0 ):
        
        #FPS
        now = umachine.time_ms()
        fps = 50000 // (now-lastTimeFps)
        lastTimeFps = now
        
        # Get free RAM
        gc.collect()
        freeRam = gc.mem_free()
    
    # print    
    text = "FPS:"+str(fps)+" RAM:"+str(freeRam)
    pygame.draw.text(0, 0, text, 7);
    #pygame.draw.text(0, 0, str(fps), 7);
    frameNum += 1
    
    pygame.display.flip()
