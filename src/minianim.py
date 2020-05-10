# minianim.py

import upygame as pygame
import umachine
import gameobject as GameObjects
import data
import urandom as random

screen = None
lastRaffleTime = 0
raffleTimeout = 2000

def RaffleMiniAnim(screen_):
    
    global screen
    global lastRaffleTime
    screen = screen_
    minianim = None
    
    now = umachine.time_ms()
    #print("lastRaffleTime",lastRaffleTime,"lastRaffleTime + raffleTimeout", lastRaffleTime + raffleTimeout,"now",now)
    if now > (lastRaffleTime + raffleTimeout):
        
        lastRaffleTime = now
        minaminCount = len(data.minianimList)
        r = random.getrandbits(8)  # between 0 and 255
        probabilityFactor = 10 # One in 10 wins
        animNum = (minaminCount*probabilityFactor) * r // 256  # between 0 and (minaminCount*probabilityFactor)
        #animNum = 2
        print("raffled animNum",animNum)
        
        if animNum<minaminCount:
            # (x,y,w,h, duration,(fram1, frame2,...),(frame1Pos, frame2Pos,...)),
            animData = data.minianimList[animNum]
            #print("animData",animData)
            frameW = animData[2]
            frameH = animData[3]
            frameSurfaces = []
            frameOffsets = []
            animPixelDataList = animData[6]
            #print("animPixelDataList",animPixelDataList)
            animFrameOffsetList = animData[7]
            #print("animFrameOffsetList",animFrameOffsetList)
            for i in range(len(animPixelDataList)):
                frameSurfaces.append( pygame.surface.Surface(frameW, frameH, animPixelDataList[i]) )
                frameOffsets.append(animFrameOffsetList[i])
                
            #print("frameOffsets",frameOffsets)
            minianim = MiniAnim( frameSurfaces, frameOffsets, animData[0], animData[1], animData[4], animData[5])

    return minianim

# The class.
class MiniAnim(object):
    def __init__(self, surfaces, frameOffsets, x, y, totalDuration, frameDuration):
        self.gob = GameObjects.GameObject(surfaces, frameOffsets)
        self.x = x 
        self.y = y
        self.hmirror = False
        self.vmirror = False
        self.totalDuration = totalDuration
        self.gob.animDur = frameDuration
        self.startTime = umachine.time_ms()

    def Update(self):
        
        if umachine.time_ms() > self.startTime + self.totalDuration:
            self.gob.active = False
        
        self.gob.update()
        
    def Draw(self):
        if self.gob.active:
            x = self.x + self.gob.frameOffsets[ self.gob.currentAnimFrameNum][0]
            y = self.y +  self.gob.frameOffsets[ self.gob.currentAnimFrameNum][1]
            screen.blit(self.gob.image, x, y, self.hmirror, self.vmirror)

    def UpdateAndDraw(self):
        self.Update()
        self.Draw()
