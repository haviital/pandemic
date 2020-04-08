# Copyright (C) 2020 Hannu Viitala
#
# The source code in this file is released under the MIT license.
# Go to http://opensource.org/licenses/MIT for the full license details.
#

import upygame


tile0Pixels = b'\
\xcc\
\xcc\
'
tile0 = upygame.surface.Surface(2, 2, tile0Pixels)
tile1Pixels = b'\
\xcc\
\xcb\
'
tile1 = upygame.surface.Surface(2, 2, tile1Pixels)
tile2Pixels = b'\
\xcc\
\xbc\
'
tile2 = upygame.surface.Surface(2, 2, tile2Pixels)
tile3Pixels = b'\
\xcc\
\xbb\
'
tile3 = upygame.surface.Surface(2, 2, tile3Pixels)
tile4Pixels = b'\
\xcb\
\xcc\
'
tile4 = upygame.surface.Surface(2, 2, tile4Pixels)
tile5Pixels = b'\
\xcb\
\xbb\
'
tile5= upygame.surface.Surface(2, 2, tile5Pixels)
tile6Pixels = b'\
\xbb\
\xbc\
'
tile6 = upygame.surface.Surface(2, 2, tile6Pixels)
tile7Pixels = b'\
\xbc\
\xbc\
'
tile7 = upygame.surface.Surface(2, 2, tile7Pixels)
tile8Pixels = b'\
\xbb\
\xbb\
'
tile8 = upygame.surface.Surface(2, 2, tile8Pixels)
tile9Pixels = b'\
\xbc\
\xcb\
'
tile9 = upygame.surface.Surface(2, 2, tile9Pixels)
tile10Pixels = b'\
\xbb\
\xcb\
'
tile10 = upygame.surface.Surface(2, 2, tile10Pixels)
tile11Pixels = b'\
\xbb\
\xcc\
'
tile11 = upygame.surface.Surface(2, 2, tile11Pixels)
tile12Pixels = b'\
\xbc\
\xcc\
'
tile12 = upygame.surface.Surface(2, 2, tile12Pixels)
tile13Pixels = b'\
\xcb\
\xcb\
'
tile13 = upygame.surface.Surface(2, 2, tile13Pixels)
tile14Pixels = b'\
\xbc\
\xbb\
'
tile14 = upygame.surface.Surface(2, 2, tile14Pixels)
tile15Pixels = b'\
\xcb\
\xbc\
'
tile15 = upygame.surface.Surface(2, 2, tile15Pixels)


girl12x15Pixels = b'\
\x00\x0a\xaa\xaa\xa0\x00\
\x00\xaa\x00\x00\xaa\x00\
\x0a\xa0\x00\x00\x0a\xa0\
\xaa\x00\x0a\xa0\x00\xaa\
\xa0\x00\xa0\x0a\x00\x0a\
\xa0\x0a\x00\x00\xa0\x0a\
\xa0\x0a\x00\x00\xa0\x0a\
\xa0\x00\xa0\x0a\x00\x0a\
\xaa\x00\x0a\xa0\x00\xaa\
\x0a\xa0\x00\x00\x0a\xa0\
\x00\xaa\x00\x00\xaa\x00\
\x00\x0a\xaa\xaa\xa0\x00\
\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\
'
girl12x15 = upygame.surface.Surface(12, 15, girl12x15Pixels)