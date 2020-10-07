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
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHTBLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)
BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5
S_SHAPE_TEMPLATE = [['.....', '.....', '..OO.', '.OO..', '.....', ], [
    '.....', '..O..', '..OO.', '...O.', '.....']]
Z_SHAPE_TEMPLATE = [['.....', '.....', '.OO..', '..OO.', '.....'], [
    '.....', '..O..', '.OO..', '.O...', '.....']]
I_SHAPE_TEMPLATE = [['..O..', '..O..', '..O..', '..O..', '.....'], [
    '.....', '..O..', 'OOOO.', '.....', '.....']]
O_SHAPE_TEMPLATE = [['.....', '.....', '.OO..', '.OO..', '.....']]
J_SHAPE_TEMPLATE = [['.....', '.O...', '.OOO.', '.....', '.....'], [
    '.....', '..OO.', '..O..', '..O..', '.....'], ['.....', '.....', '.OOO.', '...O.', '.....'], ['.....', '..O..', '..O..', '.OO..', '.....']]
L_SHAPE_TEMPLATE = [['.....', '...O.', '.OOO.', '.....', '.....'], [
    '.....', '..O..', '..O..', '..OO.', '.....'], ['.....', '.....', '.OOO.', '.O...', '.....'], ['.....', '.OO..', '..O..', '..O..', '.....']]
T_SHAPE_TEMPLATE = [['.....', '..O..', '.OOO.', '.....', '.....'], ['.....', '..O..', '..OO.', '..O..', '.....'], [
    '.....', '.....', '.OOO.', '..O..', '.....'], ['.....', '..O..', '.OO..', '..O..', '.....']]
PIECES = {'S': S_SHAPE_TEMPLATE, 'Z': Z_SHAPE_TEMPLATE, 'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE, 'I': I_SHAPE_TEMPLATE, 'O': O_SHAPE_TEMPLATE, 'T': T_SHAPE_TEMPLATE}
def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf',18)
    BIGFONT = pygame.font.Font('freesansbold.ttf',100)
    pygame.display.set_captions('Tetromino')
    while True:
        runGame()
        showTextScreen('Game Over')