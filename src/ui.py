# ui.py
# UI related functions

import upygame as pygame
from upygame import TAS

currentMenuPos = 0
currentPagePos = 0

###########################################################    
def UpdateAndDrawMenu(itemList):
    
    global currentMenuPos
    
    # TAS UI coordinates are in tiles. A tile is 6x6 pixels.
    uiTileSize = 6
    w = 16
    itemCount = len(itemList)
    h = itemCount + 2
    print("h",h)
    x = 1
    y = (88 - h*6) // (2*uiTileSize)
    
   # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:
        if eventtype.type == pygame.KEYDOWN:
            if eventtype.key == pygame.BUT_A:
                selectedMenuPos = currentMenuPos
                
                # Reset state
                currentMenuPos = 0 # reset
                TAS.clear() # remove everything in TAS UI
                
                return selectedMenuPos

            if eventtype.key == pygame.BUT_B:
                return None
            
            if eventtype.key == pygame.K_UP:
                     currentMenuPos -= 1
                     if currentMenuPos < 0:
                         currentMenuPos = 0
            if eventtype.key == pygame.K_DOWN:
                     currentMenuPos += 1
                     if currentMenuPos >= itemCount:
                         currentMenuPos = itemCount-1

    # Draw menu items
    TAS.drawBox(x, y, x+w-1, y+h-1)
    print("drawBox x",x,"y",y,"w",w,"h",h)

    for i in range(itemCount):
        cursorY = y+1+i
        TAS.setCursor(3, cursorY)
        TAS.printString(itemList[i])
        if currentMenuPos == i:
            TAS.setTile(2, cursorY, TAS.LEFT_ARROW_TILE)
            TAS.setTile(15, cursorY, TAS.RIGHT_ARROW_TILE)
   
    return None

###########################################################    
def UpdateAndDrawTextPages(pageList):
    
    global currentPagePos
    
    # TAS UI coordinates are in tiles. A tile is 6x6 pixels.
    uiTileSize = 6
    w = 17
    pageCount = len(pageList)
    h = 12
    x = 0
    y = 0
    
   # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:
        if eventtype.type == pygame.KEYDOWN:
            if eventtype.key == pygame.BUT_A: # Next page
                currentPagePos += 1
                if currentPagePos>=pageCount:
                    currentPagePos = 0
            if eventtype.key == pygame.BUT_B:  # Close
            
                # Reset state
                currentPagePos = 0 # reset
                TAS.clear() # remove everything in TAS UI
                
                return False
            

    # Draw page text
    TAS.fillRectTiles(0, 0, 18, 11, TAS.SPACE_TILE)
    boxTopTile = 25
    TAS.fillRectTiles(0, 12, 18, 12, boxTopTile)
    TAS.fillRectTiles(0, 13, 18, 14, TAS.SPACE_TILE)
    #TAS.drawBox(x, y, x+w, y+h)
    page = pageList[currentPagePos]
    for i in range(len(page)):
        TAS.setCursor(0, i)
        TAS.printString(page[i])
        
    # Draw button help
    TAS.setCursor(0, 13)
    if pageCount > 1:
        TAS.printString("A:Next B:Close")
    else:
        TAS.printString("B:Close")
     
    # Draw page counter
    if pageCount > 1:
        TAS.setCursor(15, 13)
        TAS.printInteger(currentPagePos+1)
        TAS.setCursor(16, 13)
        TAS.printString("/")
        TAS.setCursor(17, 13)
        TAS.printInteger(pageCount)
   
    return True

###########################################################    
def UpdateAndDrawDialog(textLineList):
    
    # TAS UI coordinates are in tiles. A tile is 6x6 pixels.
    uiTileSize = 6
    w = 16
    rowCount = len(textLineList)
    h = rowCount + 2
    x = 1
    y = (88 - h*6) // (2*uiTileSize)
    
   # Read keys
    eventtype = pygame.event.poll()
    if eventtype != pygame.NOEVENT:
        if eventtype.type == pygame.KEYDOWN:
            # Close. Reset state
            TAS.clear() # remove everything in TAS UI
            return False
            
    # Draw page text
    TAS.drawBox(x, y, x+w-1, y+h-1)
    for i in range(len(textLineList)):
        TAS.setCursor(2, y+i+1)
        text = textLineList[i]
        print("text",text,"text[0]",text[0],"text[:5]",text[0:5])
        if len(text)>14: 
            text = text[:14]
        TAS.printString(text)
        
    return True


###########################################################    
def ShowModalDialog(textLineList, tilemap, tilemapX, tilemapY):
    
    showDialog = True
    TAS.clear() # remove everything in TAS UI
    while showDialog:
    

        # Draw
        tilemap.draw(tilemapX, tilemapY)
        
        #
        showDialog = UpdateAndDrawDialog(textLineList)
        
        pygame.display.flip()

    TAS.clear() # remove everything in TAS UI

