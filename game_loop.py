import pygame,sys,time, os
from functions import *

### loading sprites
path = os.getcwd()
path = path + "\\sprites"
king_black = pygame.image.load(path + "\\king_black.png")
king_white = pygame.image.load(path + "\\king_white.png")
queen_black = pygame.image.load(path + "\\queen_black.png")
queen_white = pygame.image.load(path + "\\queen_white.png")
rook_black = pygame.image.load(path + "\\rook_black.png")
rook_white = pygame.image.load(path + "\\rook_white.png")
bishop_black = pygame.image.load(path + "\\bishop_black.png")
bishop_white = pygame.image.load(path + "\\bishop_white.png")
knight_black = pygame.image.load(path + "\\knight_black.png")
knight_white = pygame.image.load(path + "\\knight_white.png")
pawn_black = pygame.image.load(path + "\\pawn_black.png")
pawn_white = pygame.image.load(path + "\\pawn_white.png")

sprite_dict = {
    "k":  [king_black, king_white],
    "q":  [queen_black, queen_white],
    "r":  [rook_black, rook_white],
    "b":  [bishop_black, bishop_white],
    "kn": [knight_black, knight_white],
    "p":  [pawn_black, pawn_white]
}


### Initialize Pygame Screen
pygame.init()
font = pygame.font.SysFont("Calibri", 35)
width = 800
height = 800
screen = pygame.display.set_mode([width,height])
darkcolor=(100,100,100)
whitecolor=(255,255,255)
color_dict = {0: "Black", 1: "White"}


### Promotion GUI

def promote(color):
    for i in range(4):
        pygame.draw.rect(screen, (0, 0, 0), (
            (int((2 * i + 1) * width / 8 - width / 16), int(height / 2 - height / 16)),
            (int(width / 8), int(height / 8))))

        pygame.draw.rect(screen, (255, 255, 255), (
            (int((2 * i + 1) * width / 8 - width / 16 + 5), int(height / 2 - height / 16 + 5)),
            (int(width / 8 - 10), int(height / 8 - 10))))

    for i, sprite in enumerate(["kn", "b", "r", "q"]):
        screen.blit(sprite_dict[sprite][color],
                    (int((2 * i + 1) * width / 8 - width / 32), int(height / 2 - height / 32)))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                for i in range(4):
                    if int((2 * i + 1) * width / 8 - width / 16) <= mouse_pos[0] <= int((2 * i + 1) * width / 8 + width / 16) and int(height / 2 - height / 16) <= mouse_pos[1] <= int(height / 2 + height / 8):
                        return i

### PYGAME LOOP ###

def game_loop(func_board, func_piece_dict):
    updateScreen = True
    piece_selected = False
    turn = 1
    runGame = True
    pawncounter = 0
    freeSpaces = count_free_spaces(func_board)


    while runGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        ### Input handling ###
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:                      # Left click
                updateScreen = True
                mouse_pos = pygame.mouse.get_pos()
                selectedSquare = get_pos_on_board(mouse_pos, height, width)

        ### Piece selection and moving ###
                if piece_selected:
                    if selectedSquare in possibleMoves:

                        for x in func_board:
                            for y in x:
                                if y != "0":
                                    pawn = func_piece_dict[y]
                                    if pawn.type == "p":
                                        pawn.allowEnPassant = False

                        selectedPiece.move(selectedSquare, func_board, func_piece_dict)
                        tempFreeSpaces = count_free_spaces(func_board)

                        if selectedPiece.type != "p" and tempFreeSpaces == freeSpaces:
                            pawncounter += 1
                        else:
                            pawncounter = 0

                        freeSpaces = tempFreeSpaces
                        turn = 1 - turn

                    piece_selected = False

                    ### End conditions ###
                    if pawncounter == 100:
                        print("draw")
                        runGame = False

                    if check_check(turn, 2, func_board, func_piece_dict)[0] and not can_move(turn, func_board, func_piece_dict):
                        print(f"{color_dict[1 - turn]} wins!!")
                        runGame = False
                    elif not can_move(turn, func_board, func_piece_dict):
                        print("draw")
                        runGame = False

                elif func_board[selectedSquare[0]][selectedSquare[1]] != "0":
                    selectedPiece = func_piece_dict[func_board[selectedSquare[0]][selectedSquare[1]]]
                    if selectedPiece.color == turn:
                        piece_selected = True
                        possibleMoves = selectedPiece.possiblePositions(func_board, func_piece_dict)

        ### Draw Screen ###
        for indexX, x in enumerate(func_board):
            for indexY, y in enumerate(x):
                if((indexY + indexX)%2 == 0):
                    pygame.draw.rect(screen, whitecolor, (indexX*(width/8), indexY*(height/8), (indexX+1)*(width/8), (indexY+1)*(height/8)))
                else:
                    pygame.draw.rect(screen, darkcolor, (indexX * (width / 8), indexY * (height / 8), (indexX + 1) * (width / 8), (indexY + 1) * (height / 8)))

                if y != "0":
                    screen.blit(sprite_dict[func_piece_dict[y].type][func_piece_dict[y].color], ((indexX*(width/8) + width/32, indexY*(height/8) + height/32)))

        if piece_selected:
            for move in possibleMoves:
                circlePos = get_pos_on_screen(move, height, width)
                pygame.draw.circle(screen, (0,255,0), (int(circlePos[0]+width/16), int(circlePos[1]+height/16)), 15)

        if updateScreen:
            pygame.display.update()
            updateScreen = False