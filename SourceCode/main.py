import random
import time
import pygame
import sys
from pygame.locals import *
FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'
MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1
XMARGIN = int((WINDOWWIDTH-BOARDWIDTH*BOXSIZE)/2)
TOPMARGIN = WINDOWHEIGHT-(BOARDHEIGHT*BOXSIZE)-5
