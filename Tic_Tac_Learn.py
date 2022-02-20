import sys
import pygame
from random import randint
from pygame.locals import *
import numpy as np
import policy_network
import value_network
import engine

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

circles = []
xs = []
moves = [".",".",".",".",".",".",".",".","."]
games = []
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
screen.fill((255, 255, 255))
white = (255, 255, 255)
black = (0, 0, 0)
x, y = 0, 0
thing = 0
i = 0
piece = 0
circlesWins = 0
xsWins = 0
draws = 0
gameCounter = 0
running = True
win = False

pygame.display.set_caption('Tic Tac Toe')
font_obj = pygame.font.Font('freesansbold.ttf', 25)
circleWinDisplay = font_obj.render('Circle Wins! Press any key to play again.', True, black)
xWinDisplay = font_obj.render('X Wins! Press any key to play again.', True, black)


def createBoard():
    text_obj = font_obj.render('Circles Wins: ' + str(circlesWins) + ' Xs Wins: ' + str(xsWins) + ' Draws: ' + str(draws) + ' Games: '  + str(gameCounter), True, black)
    screen.blit(text_obj, (10, 10))
    pygame.draw.line(screen, black, (450, 250), (450, 700), 4)
    pygame.draw.line(screen, black, (600, 250), (600, 700), 4)
    pygame.draw.line(screen, black, (300, 400), (750, 400), 4)
    pygame.draw.line(screen, black, (300, 550), (750, 550), 4)
    pygame.draw.line(screen, black, (300, 250), (750, 250), 4)
    pygame.draw.line(screen, black, (300, 700), (750, 700), 4)
    pygame.draw.line(screen, black, (300, 250), (300, 700), 4)
    pygame.draw.line(screen, black, (750, 250), (750, 700), 4)
    pygame.display.update()


def checkcursor(x, y):
    if 300 <= x <= 450 and 250 <= y <= 400:
        return 1
    if 300 <= x <= 450 and 400 <= y <= 550:
        return 4
    if 300 <= x <= 450 and 550 <= y <= 700:
        return 7
    if 450 <= x <= 600 and 250 <= y <= 400:
        return 2
    if 450 <= x <= 600 and 400 <= y <= 550:
        return 5
    if 450 <= x <= 600 and 550 <= y <= 700:
        return 8
    if 600 <= x <= 750 and 250 <= y <= 400:
        return 3
    if 600 <= x <= 750 and 400 <= y <= 550:
        return 6
    if 600 <= x <= 750 and 550 <= y <= 700:
        return 9


def getPos(pos):
    if pos == 1:
        return 325, 275
    if pos == 4:
        return 325, 425
    if pos == 7:
        return 325, 575
    if pos == 2:
        return 475, 275
    if pos == 5:
        return 475, 425
    if pos == 8:
        return 475, 575
    if pos == 3:
        return 625, 275
    if pos == 6:
        return 625, 425
    if pos == 9:
        return 625, 575


def createpiece(pos, piece):
    if pos is not None:
        x, y = getPos(pos)
        pieceexist = False
        for e in circles:
            if e == pos:
                pieceexist = True
        for a in xs:
            if a == pos:
                pieceexist = True
        if pieceexist:
            return piece
        if piece % 2 == 0:
            pygame.draw.line(screen, black, (x, y), (x + 100, y + 100), 4)
            pygame.draw.line(screen, black, (x + 100, y), (x, y + 100), 4)
            xs.append(pos)
            moves[pos - 1] = "X"
            piece += 1
            return piece
        else:
            pygame.draw.circle(screen, black, (x + 50, y + 50), 50)
            circles.append(pos)
            moves[pos - 1] = "O"
            piece += 1
            return piece


def testwin(pieceList):
    if 1 in pieceList and 2 in pieceList and 3 in pieceList:
        return True

    if 4 in pieceList and 5 in pieceList and 6 in pieceList:
        return True

    if 7 in pieceList and 8 in pieceList and 9 in pieceList:
        return True

    if 1 in pieceList and 4 in pieceList and 7 in pieceList:
        return True

    if 2 in pieceList and 5 in pieceList and 8 in pieceList:
        return True

    if 3 in pieceList and 6 in pieceList and 9 in pieceList:
        return True

    if 1 in pieceList and 5 in pieceList and 9 in pieceList:
        return True

    if 3 in pieceList and 5 in pieceList and 7 in pieceList:
        return True

    return False

createBoard()
policy_net = policy_network.PolicyNetwork([18, 10, 9])
value_net = value_network.ValueNetwork([18, 10, 1])
e = engine.Engine(policy_net, value_net)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            pos = checkcursor(x, y)
            piece = createpiece(pos, piece)
    if len(circles) >= 3:
        if testwin(circles):
            screen.blit(circleWinDisplay, (500, 500))
            circlesWins += 1
            gameCounter += 1
            screen.fill(white)
            moves = [".",".",".",".",".",".",".",".","."]
            circles.clear()
            xs.clear()
            createBoard()
    if len(xs) >= 3:
        if testwin(xs):
            screen.blit(xWinDisplay, (500, 500))
            xsWins += 1
            gameCounter += 1
            circles.clear()
            xs.clear()
            moves = [".",".",".",".",".",".",".",".","."]
            createBoard()
    if len(xs) == 5 or len(circles) == 5:
        draws += 1
        gameCounter += 1
        screen.fill(white)
        circles.clear()
        xs.clear()
        moves = [".",".",".",".",".",".",".",".","."]
        createBoard()
    if piece is not None and piece % 2 == 1:
        piece = createpiece(e.get_optimal_move(1000, np.asarray(np.reshape(moves, (3, 3))))[0] + 1, piece)

    pygame.display.update()
