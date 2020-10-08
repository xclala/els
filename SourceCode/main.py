import random
from time import time
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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')
    while True:
        runGame()
        showTextScreen('Game Over')


def runGame():
    board = getBlankBoard()
    lastMoveDownTime = time()
    lastMoveSidewaysTime = time()
    lastFallTime = time()
    movingDown, movingLeft, movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)
    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    while True:
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time()
            if not isVaildPosition(board, fallingPiece):
                return
    checkForQuit()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if (event.key == K_p):
                DISPLAYSURF.fill(BGCOLOR)
                showTextScreen('Paused')
                lastFallTime = time()
                lastMoveDownTime = time()
                lastMoveSidewaysTime = time()
            elif (event.key == K_LEFT or event.key == K_a):
                movingLeft = False
            elif (event.key == K_RIGHT or event.key == K_d):
                movingRight = False
            elif (event.key == K_DOWN or event.key == K_s):
                movingDown = False
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and isVaildPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time()
            elif (event.key == K_RIGHT or event.key == K_d) and isVaildPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
                movingRight = True
                movingLeft = False
                lastMoveSidewaysTime = time()
            elif (event.key == K_UP or event.key == K_w):
                fallingPiece['rotation'] = (
                    fallingPiece['rotation']+1) % len(PIECES[fallingPiece['shape']])
                if not isVaildPosition(board, fallingPiece):
                    fallingPiece['rotation'] = (
                        fallingPiece['rotation']-1) % len(PIECES[fallingPiece['shape']])
            elif (event.key == K_q):
                fallingPiece['rotation'] = (
                    fallingPiece['rotation']-1) % len(PIECES[fallingPiece['shape']])
                if not isVaildPosition(board, fallingPiece):
                    fallingPiece['rotation'] = (
                        fallingPiece['rotation']+1) % len(PIECES[fallingPiece['shape']])
            elif (event.key == K_DOWN or event.key == K_s):
                movingDown = True
                if isVaildPosition(board, fallingPiece, adjY=1):
                    fallingPiece['y'] += 1
                lastMoveDownTime = time()
            elif event.key == K_SPACE:
                movingDown, movingLeft, movingRight = False
                for i in range(1, BOARDHEIGHT):
                    if not isVaildPosition(board, fallingPiece, adjY=i):
                        break
                fallingPiece['y'] += i - 1
    if (movingLeft or movingRight) and time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
        if movingLeft and isVaildPosition(board, fallingPiece, adjX=-1):
            fallingPiece['x'] -= 1
        elif movingRight and isVaildPosition(board, fallingPiece, adjX=1):
            fallingPiece['x'] += 1
        lastMoveSidewaysTime = time()
    if movingDown and time() - lastMoveDownTime > MOVEDOWNFREQ and isVaildPosition(board, fallingPiece, adjY=1):
        fallingPiece['y'] += 1
        lastMoveDownTime = time()
    if time() - lastFallTime > fallFreq:
        if not isVaildPosition(board, fallingPiece, adjY=1):
            addToBoard(board, fallingPiece)
            score += removeCompleteLines(board)
            level, fallFreq = calculateLevelAndFallFreq(score)
            fallingPiece = None
        else:
            fallingPiece['y'] += 1
            lastFallTime = time()
    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(board)
    drawStatus(score, level)
    drawNextPiece(nextPiece)
    if fallingPiece != None:
        drawPiece(fallingPiece)
    pygame.display.update()
    FPSCLOCK.tick(FPS)
