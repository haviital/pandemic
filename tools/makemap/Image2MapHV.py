# Filename  : Image2MapHV.py
# Authors   : Georg Muntingh and Bjorn Lindeijer. Modifies by Hannu Viitala
# Version   : 1.0
# Date      : April 6, 2010
# Copyright : Public Domain

from PIL import Image
import os, sys, networkx
from functools import cmp_to_key   # required for cmp_to_key

class TileMap:
    """ This class represents a map of tiles.
    """

    def __init__(self, file, tileX, tileY):
        # For initialization, map image with filename file should be specified, together with the
        # tile size (tile X, tileY). First we set the tile sizes.
        self.TileX, self.TileY = tileX, tileY

        # Open the map and find its attributes.
        print ("Opening the map image file: " + file)
        self.MapImage = Image.open(file)
        self.MapImageWidth, self.MapImageHeight = self.MapImage.size
        self.Width, self.Height = self.MapImageWidth // self.TileX, self.MapImageHeight // self.TileY

        # Store the unique tiles in a list and a hash, and the map in a list.
        #self.MapList, self.TileList, self.TileDict = self.parseMap()

        # Create an image file from our map of unique tiles.
        #self.TileImage = self.getTileImage()

    def parseMap(self):
        """ This function takes the map image, and obtains
            * a list TList of unique tiles.
            * a hash TDict of unique tiles.
            * a double list self.MapList of where an entry equals i if
                self.TileList[i] is the corresponding picture on the map image.
        """

        progress = -1
        TilesDict = {}
        print("Parsing the Map: ")

        # Jump through the map image in n x n-tile steps. In each step:
        #  * If the string of the tile is in the dictionary, place its value in map list MList[y][x].
        #  * Otherwise, add this tile to the list, and add its string to the dictionary with value "the
        #    number of elements in the list". Also place this value in MList[y][x].
        for y in range(self.Height):
            for x in range(self.Width):
                box = self.TileX * x, self.TileY * y, self.TileX * (x+1), self.TileY * (y+1)
                tile = self.MapImage.crop(box)
                s = tile.tobytes()
                
                if TilesDict[s]

                if s in TilesDict:
                    MList[y][x] = TDict[s]
                else:
                    TilesDict[s] = len(TList)

                # Calculate the progress, and print it to the screen.
                p = ((x + y * self.Width) * 100) / (self.Width * self.Height)
                if progress != p:
                    progress = p
                    self.printProgress(progress)

        self.printProgress(100)
        print ("Done!")

        return MList, TList, TDict


if sys.argv[1] == "--help":
    print ("Usage  : python Image2MapHV.py tileX tileY file")
    print ("Example: python Image2MapHV.py 8 8 Caves.png")
elif len(sys.argv) != 4:
    print ("Error  : You specified too few arguments!\n")
    print ("Usage  : python Image2MapHV.py tileX tileY file")
    print ("Example: python Image2MapHV.py 8 8 Caves.png")
else:
    tileX, tileY = int(sys.argv[1]), int(sys.argv[2])
    file = sys.argv[3]
    
    map = TileMap(file, tileX, tileY)

    tilefile = os.path.splitext(file)[0] + "-TilesetHV" + ".png"
    print ("Saving the tileset image into the file: " + tilefile)
    map.TileImage.save( tilefile, "PNG" )
