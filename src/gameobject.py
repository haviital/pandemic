# gameobject.py

# Copyright (C) 2019 Hannu Viitala
#
# The source code in this file is released under the MIT license.
# Go to http://opensource.org/licenses/MIT for the full license details.

import upygame as pygame
#import globals as glob
import sprite
#import urandom as random
#import data
#import utils
import glob

# The game object class.
class GameObject(sprite.Sprite):
    def __init__(self, surfaces, frameOffsets):
        sprite.Sprite.__init__(self)
        self.frames = surfaces
        self.frameOffsets = frameOffsets
        self.currentAnimFrameNum = 0
        self.image = self.frames[self.currentAnimFrameNum]  # current image
        self.animDur = 3
        self.animDurCounter = self.animDur
        self.animDir = 1
        self.animMode = "";

        # velocity and position in the world
        self.vx = 0
        self.vy = 0
        self.wx = 0 # world x
        self.wy = 0 # world y
        # Note. the rect member data is in viewport domain (e.g. screen)
        self.moveDelay = 0
        self.moveDelayCounter = 0

        # Position in the viewport
        self.rect = self.frames[self.currentAnimFrameNum].get_rect()

    def ResetAnimation(self):

         # The animation duration
        self.animDurCounter = self.animDur

        # Set current image
        self.image = self.frames[self.currentAnimFrameNum]
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        self.wx += self.frameOffsets[self.currentAnimFrameNum][0]
        self.wy += self.frameOffsets[self.currentAnimFrameNum][1]
                
    def Animate(self):
        
        if(not self.active): return

        # Delay
        self.moveDelayCounter -= 1
        if(self.moveDelayCounter<=0):
            self.moveDelayCounter = self.moveDelay
        else:
            return

        # Advance frame if animation is set
        if self.animDur > 0:

          #
          self.animDurCounter -= 1

          # if animation duration has elapsed, advance frame
          if self.animDurCounter == 0:
                self.currentAnimFrameNum += self.animDir
                if (self.currentAnimFrameNum >= len(self.frames)):
                    if self.animMode == "once":
                        self.currentAnimFrameNum = len(self.frames) - 1
                    else:  # loop
                        self.currentAnimFrameNum = 0

                self.ResetAnimation()

    def update(self):

        if(not self.active): return

        # Animate
        self.Animate()

        #print("juice: wx", self.wx,"wy",self.wy)
        # Advance position in the world
        prevX = self.wx
        prevY = self.wy
        self.wx += self.vx
        self.wy += self.vy

       # Set the position in the viewport
        self.rect.x = self.wx + glob.viewPortX
        self.rect.y = self.wy + glob.viewPortY

        # Start again from the top
        #if(self.wy>glob.SCREEN_H):
        #    self.wy = -self.rect.height

    # Check all collisions
    def CheckCollisions(self):
        heroWasHit = None
        enemyWasHit = None
        enemyIsOverWall = None
        herocollide = glob.heroGob.rect.colliderect
        heroGobX = glob.heroGob.x
        heroGobY = glob.heroGob.y
        heroGobW = glob.heroGob.rect.width
        heroGobH = glob.heroGob.rect.height
        srect = pygame.Rect(0,0,0,0)

        s = self
        srect.width = s.rect.width
        srect.height = s.rect.height
        srectx = s.wx
        srecty = s.wy
        srect.x = srectx
        srect.y = srecty

        # Check the collision to the wall in the tilemap
        #tileIdList = glob.tilemap.get_tile_ids(srectx, srecty, srectx+srect.width, srecty+srect.height, 8)
        #tl = glob.tileAttributeArray[tileIdList[0]] & glob.TILE_FLAG_BLOCKING
        #tr = glob.tileAttributeArray[tileIdList[1]] & glob.TILE_FLAG_BLOCKING
        #bl = glob.tileAttributeArray[tileIdList[2]] & glob.TILE_FLAG_BLOCKING
        #br = glob.tileAttributeArray[tileIdList[3]] & glob.TILE_FLAG_BLOCKING
        #if( tl + tr + bl + br > 0):
        #    enemyIsOverWall = True

        # Check if the enemy is out-of-screen
        if (srectx<0 or srecty<0 ):
            return heroWasHit, enemyWasHit, enemyIsOverWall

        # Check for the hero hit is by the enemy
        if (abs(heroGobX-srectx<heroGobW) and abs(heroGobY-srecty<heroGobH)):
            if herocollide(s.rect):
                heroWasHit = s

        return heroWasHit, enemyIsOverWall

