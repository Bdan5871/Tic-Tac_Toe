import sys
import pygame
import threading
from random import randint
from pygame.locals import *

pygame.init()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

rlybad = []
rlygood = []
bad = []
good = []
circles = []
xs = []
moves = []
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
    font_obj = pygame.font.Font('freesansbold.ttf', 25)
    text_obj = font_obj.render(
        'Circles Wins: ' + str(circlesWins) + ' Xs Wins: ' + str(xsWins) + ' Draws: ' + str(draws) + ' Games: ' + str(
            gameCounter), True, black)
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
        return 2
    if 300 <= x <= 450 and 550 <= y <= 700:
        return 3
    if 450 <= x <= 600 and 250 <= y <= 400:
        return 4
    if 450 <= x <= 600 and 400 <= y <= 550:
        return 5
    if 450 <= x <= 600 and 550 <= y <= 700:
        return 6
    if 600 <= x <= 750 and 250 <= y <= 400:
        return 7
    if 600 <= x <= 750 and 400 <= y <= 550:
        return 8
    if 600 <= x <= 750 and 550 <= y <= 700:
        return 9


def getPos(pos):
    if pos == 1:
        return (325, 275)
    if pos == 2:
        return (325, 425)
    if pos == 3:
        return (325, 575)
    if pos == 4:
        return (475, 275)
    if pos == 5:
        return (475, 425)
    if pos == 6:
        return (475, 575)
    if pos == 7:
        return (625, 275)
    if pos == 8:
        return (625, 425)
    if pos == 9:
        return (625, 575)


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
        if piece % 2 == 0 and pieceexist is False:
            pygame.draw.circle(screen, black, (x + 50, y + 50), 50)
            circles.append(pos)
            moves.append(pos)
            piece += 1
            pieceexist = False
            return piece
        if piece % 2 != 0 and pieceexist is False:
            pygame.draw.line(screen, black, (x, y), (x + 100, y + 100), 4)
            pygame.draw.line(screen, black, (x + 100, y), (x, y + 100), 4)
            xs.append(pos)
            moves.append(pos)
            piece += 1
            pieceexist = False
            return piece
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


def AI(moves, piece):
    pos = 0
    index = 0
    false = 0
    for i in games:
        if i[-1] is True:
            if len(moves) == len(i) - 2:
                print(i)
                pos = check(moves, i)
                if pos != 0:
                    rlygood.append(pos)
                    pos = 0
            else:
                pos = check(moves, i)
                if pos != 0:
                    good.append(pos)
        if i[-1] is False:
            if len(moves) == len(i) - 3:
                pos = check(moves, i)
                if pos != 0:
                    rlybad.append(pos)
                    pos = 0
            else:
                pos = check(moves, i)
                if pos != 0:
                    bad.append(pos)
                    pos = 0
    if len(rlygood) != 0:
        if rlygood[0] is not None:
            piece = createpiece(rlygood[randint(0, len(rlygood) - 1)], piece)
            rlygood.clear()
            rlybad.clear()
            good.clear()
            bad.clear()
    if len(good) != 0:
        if good[0] is not None:
            for i in good:
                for j in bad:
                    if i == j and len(good) != 0:
                        if good[0] is not None:
                            if i in good:
                                good.remove(i)
    if len(good) != 0:
        if good[0] is not None:
            piece = createpiece(good[randint(0, len(good) - 1)], piece)
            rlygood.clear()
            rlybad.clear()
            good.clear()
            bad.clear()
            return piece
    if len(bad) != 0:
        if bad[0] is not None:
            for i in moves:
                for j in bad:
                    if i == pos or j == pos:
                        pos = randint(1, 9)
                        piece = createpiece(pos, piece)
                        rlygood.clear()
                        rlybad.clear()
                        good.clear()
                        bad.clear()
                        return piece
    pos = randint(1, 9)
    piece = createpiece(pos, piece)
    return piece


def AI2(circles, xs, moves, piece):
    possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pos = checkWinLose(circles)
    for i in moves:
        if pos == i:
            pos = 0
    if pos == 0:
        pos = checkWinLose(xs)
        for i in moves:
            if pos == i:
                pos = 0
    if pos == 0:
        if len(circles) == 0:
            if len(xs) ==1:
                if xs[0] != 5:
                    pos = 5
                else:
                    pos = 1
    if pos == 0:
        if len(circles) == 0 and len(xs) == 0:
            pos = 5
        if len(circles) == 1:
            if circles[0] == 5:
                pos = 1
                if (1 in xs or 9 in xs) and 4 in xs:
                    pos = 7
                elif 1 in xs or 9 in xs:
                    pos = 4
            elif circles[0] == 1:
                pos = 3
                for i in xs:
                    if i == 2 or i == 3:
                        pos = 7
    if pos == 0:
        pos = randint(1,9)
    piece = createpiece(pos, piece)
    return piece


def checkWinLose(pieceList):
    if (2 in pieceList and 3 in pieceList) or (5 in pieceList and 9 in pieceList) or (4 in pieceList and 7 in pieceList):
        return 1
    if (1 in pieceList and 3 in pieceList) or (5 in pieceList and 8 in pieceList):
        return 2
    if (1 in pieceList and 2 in pieceList) or (6 in pieceList and 9 in pieceList) or (5 in pieceList and 7 in pieceList):
        return 3
    if (1 in pieceList and 7 in pieceList) or (6 in pieceList and 5 in pieceList):
        return 4
    if (2 in pieceList and 8 in pieceList) or (7 in pieceList and 3 in pieceList) or (6 in pieceList and 4 in pieceList) or (1 in pieceList and 9 in pieceList):
        return 5
    if (3 in pieceList and 9 in pieceList) or (5 in pieceList and 4 in pieceList):
        return 6
    if (1 in pieceList and 4 in pieceList) or (5 in pieceList and 3 in pieceList) or (8 in pieceList and 9 in pieceList):
        return 7
    if (2 in pieceList and 5 in pieceList) or (7 in pieceList and 9 in pieceList):
        return 8
    if (1 in pieceList and 5 in pieceList) or (3 in pieceList and 6 in pieceList) or (7 in pieceList and 8 in pieceList):
        return 9
    return 0


def check(moves, i):
    pos = 0
    move = 0
    if len(moves) > len(i):
        for j in range(len(i)):
            if i[j] != moves[j]:
                return pos
            move = i[j + 1]
    if len(moves) < len(i):
        for j in range(len(moves)):
            if i[j] != moves[j]:
                return 0
            move = i[j + 1]
        return move


def checkExists(games, moves):
    for i in games:
        if i == moves:
            return False
    return True


createBoard()
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
        win = testwin(circles)
        if win is True:
            screen.blit(circleWinDisplay, (500, 500))
            circlesWins += 1
            gameCounter += 1
            screen.fill(white)
            moves.append(False)
            if checkExists:
                games.append(moves[:])
            win = False
            moves.clear()
            circles.clear()
            xs.clear()
            createBoard()
    if len(xs) >= 3:
        win = testwin(xs)
        if win is True:
            screen.blit(xWinDisplay, (500, 500))
            xsWins += 1
            gameCounter += 1
            screen.fill(white)
            moves.append(True)
            if checkExists:
                games.append(moves[:])
            win = False
            circles.clear()
            xs.clear()
            moves.clear()
            createBoard()
    if len(xs) == 5 or len(circles) == 5:
        draws += 1
        gameCounter += 1
        screen.fill(white)
        win = False
        moves.append(True)
        if checkExists:
            games.append(moves[:])
        circles.clear()
        xs.clear()
        moves.clear()
        createBoard()
    if piece % 2 == 1:
         piece = AI(moves, piece)
    if piece % 2 == 0:
        piece = AI2(circles, xs, moves, piece)
    pygame.display.update()
