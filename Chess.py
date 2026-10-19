import pygame,sys,time, os, math
from copy import deepcopy

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

### piece classes

class piece():
    def __init__(self, color, position, type, name):
        self.color = color
        self.position = position
        self.type = type
        self.name = name

    def move(self, pos, func_board, simulate=False):
        func_board[self.position[0]][self.position[1]] = "0"
        self.position = pos
        func_board[self.position[0]][self.position[1]] = self.name

    def possiblePositions(self, func_board, depth=2):
        if depth == 0:
            return []

        list = self.piecePositions(func_board, depth)

        valid_moves = []
        for index, space in enumerate(list):  # Remove spaces with same color piece
            if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                continue

            elif func_board[space[0]][space[1]] != "0" and piece_dict[func_board[space[0]][space[1]]].color == self.color:
                continue

            board_copy = deepcopy(func_board)
            current_position = self.position
            self.move(space, board_copy, True)
            if check_check(self.color, depth, board_copy, piece_dict)[0]:
                pass
            else:
                valid_moves.append(space)
            self.move(current_position, board_copy, True)

        return valid_moves

class pawn(piece):
    def __init__(self, color, position, name):
        piece.__init__(self, color, position, "p", name)
        self.hasMoved = False                                                                   # First move identifier
        self.allowEnPassant = False                                                              # Second move identifier for en passant
        self.previousPiece = "0"                                                               # For taking en passant7
        self.doneEnPassant = False
        self.dir = (self.color*2-1)*-1                                                                                 # Direction

    def piecePositions(self, func_board, depth=2):
        list = []

        if func_board[self.position[0]][self.position[1]+self.dir] == "0":
            list.append([self.position[0], self.position[1]+self.dir])                                     # One space up
            if not self.hasMoved:
                if func_board[self.position[0]][self.position[1] + 2*self.dir] == "0":
                    list.append([self.position[0], self.position[1] + 2*self.dir])                               # Two spaces up for first move

        for i in range(2):
            if not (0 <= self.position[0]+(i*2-1) <= 7):
                continue
            if func_board[self.position[0]+(i*2-1)][self.position[1]+self.dir] != "0":
                if piece_dict[func_board[self.position[0]+(i*2-1)][self.position[1]+self.dir]].color != self.color:   # Taking 1 up and 1 to the side, if there is an opposite color piece
                    list.append([self.position[0]+(i*2-1), self.position[1]+self.dir])

            elif func_board[self.position[0] + (i * 2 - 1)][self.position[1]] != "0":
                tempPiece =  piece_dict[func_board[self.position[0] + (i * 2 - 1)][self.position[1]]]
                if tempPiece.type == "p" and tempPiece.color != self.color and tempPiece.allowEnPassant:   # En Passant
                    list.append([self.position[0] + (i * 2 - 1), self.position[1]+self.dir])

        return list

    def move(self, pos, func_board, simulate=False):                                                  # Move and mark moved
        if simulate and self.doneEnPassant:
            func_board[self.previousPiece.position[0]][self.previousPiece.position[1]] = self.previousPiece.name
            self.doneEnPassant = False
            self.previousPiece = "0"

        if pos[1] - self.position[1] == self.dir:
            if abs(pos[0] - self.position[0]) == 1 and func_board[pos[0]][pos[1]] == "0":
                self.doneEnPassant = True
                self.previousPiece = piece_dict[func_board[pos[0]][pos[1]-self.dir]]
                func_board[pos[0]][pos[1]-self.dir] = "0"

        if pos[1] - self.position[1] == 2:
            self.allowEnPassant = True

        super().move(pos, func_board)


        if not simulate:
            self.hasMoved = True

            if self.position[1] in [0,7]:                                      # Promotion
                for i in range(4):
                    pygame.draw.rect(screen, (0, 0, 0), (
                    (int((2*i+1) * width / 8 - width / 16), int(height / 2 - height / 16)),
                    (int(width / 8), int(height / 8))))

                    pygame.draw.rect(screen, (255, 255, 255), (
                    (int((2*i+1) * width / 8 - width / 16 + 5), int(height / 2 - height / 16 + 5)),
                    (int(width / 8 - 10), int(height / 8 - 10))))

                for i, sprite in enumerate(["kn", "b", "r", "q"]):
                    screen.blit(sprite_dict[sprite][self.color],
                                (int((2*i+1) * width / 8 - width / 32), int(height / 2 - height / 32)))
                pygame.display.update()

                run = True
                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                            mouse_pos = pygame.mouse.get_pos()
                            print(mouse_pos)
                            for i in range(4):
                                if int((2*i+1)*width/8-width/16) <= mouse_pos[0] <= int((2*i+1)*width/8+width/16) and int(height/2-height/16) <= mouse_pos[1] <= int(height/2+height/8):
                                    if i == 0:
                                        new_pieces.append(knight(self.color, self.position, self.name))
                                    elif i == 1:
                                        new_pieces.append(bishop(self.color, self.position, self.name))
                                    elif i == 2:
                                        new_pieces.append(rook(self.color, self.position, self.name))
                                    elif i == 3:
                                        new_pieces.append(queen(self.color, self.position, self.name))
                                    run = False

                piece_dict[self.name] = new_pieces[-1]

class knight(piece):
    def __init__(self,color,position,name):
        piece.__init__(self,color,position,"kn",name)

    def piecePositions(self, func_board, depth=2):
        list = []                                                   # All possible spaces
        list.append([self.position[0] + 2,self.position[1] + 1])
        list.append([self.position[0] + 2, self.position[1] - 1])
        list.append([self.position[0] + 1, self.position[1] + 2])
        list.append([self.position[0] + 1, self.position[1] - 2])
        list.append([self.position[0] - 1, self.position[1] + 2])
        list.append([self.position[0] - 1, self.position[1] - 2])
        list.append([self.position[0] - 2, self.position[1] + 1])
        list.append([self.position[0] - 2, self.position[1] - 1])

        return list

class bishop(piece):
    def __init__(self,color,position,name):
        piece.__init__(self,color,position,"b",name)

    def piecePositions(self,func_board,  depth=2):
        list = []

        for e in [[-1,-1], [-1, 1], [1, -1], [1,1]]:                    # All 4 diagonal directions
            for i in range(7):                                          # Go diagonally until there is a piece of the edge of the board
                space = [self.position[0] + (i+1)*e[0], self.position[1] + (i+1)*e[1]]
                if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                    break

                if func_board[space[0]][space[1]] == "0":

                    list.append(space)
                elif piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)
                    break
                else: break

        return list

class rook(piece):
    def __init__(self, color, position,name):
        piece.__init__(self, color, position, "r",name)
        self.hasMoved = False

    def piecePositions(self, func_board, depth=2):
        list = []

        for e in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            for i in range(7):
                space = [self.position[0] + (i+1)*e[0], self.position[1] +(i+1)*e[1]]
                if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                    break

                if func_board[space[0]][space[1]] == "0":
                    list.append(space)
                elif piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)
                    break
                else:
                    break

        return list

    def move(self, pos, func_board, simulate=False):
        super().move(pos, func_board)

        if not simulate:
            self.hasMoved = True

class queen(piece):
    def __init__(self, color, position, name):
        piece.__init__(self, color, position, "q", name)

    def piecePositions(self, func_board, depth=2):
        list = []

        for e in [[-1,-1], [-1, 1], [1, -1], [1,1],[-1, 0], [1, 0], [0, -1], [0, 1]]:
            for i in range(7):
                space = [self.position[0] + (i+1) * e[0], self.position[1] + (i+1) * e[1]]
                if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                    break

                if func_board[space[0]][space[1]] == "0":
                    list.append(space)
                elif piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)
                    break
                else:
                    break

        return list

class king(piece):
    def __init__(self, color, position, name):
        piece.__init__(self, color, position, "k", name)
        self.hasMoved = False
        self.rooks = []

    def find_rooks(self, func_board):
        for x in func_board:
            for y in x:
                if y != "0":
                    piec = piece_dict[y]
                    if piec.type == "r" and piec.color == self.color:
                        self.rooks.append(piec)

    def piecePositions(self, func_board, depth=2):
        list = []

        for e in [[-1, -1], [-1, 1], [1, -1], [1, 1], [-1, 0], [1, 0], [0, -1], [0, 1]]:
            space = [self.position[0] + 1 * e[0], self.position[1] + 1 * e[1]]
            if 0 <= space[0] <= 7 and 0 <= space[1] <= 7:

                if func_board[space[0]][space[1]] == "0":
                    list.append(space)
                elif piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)

        if not self.hasMoved:                                               # King hasn't moved
            enemyList = check_check(self.color, depth, func_board, piece_dict)
            if not enemyList[0]:                                            # King is not in check
                for rook in self.rooks:
                    if not rook.hasMoved:                                   # Rook hasn't moved
                        allowCastle = True
                        rookPosX = rook.position[0]
                        direction = int(math.copysign(1, (rookPosX - self.position[0])))
                        for x in range(1, abs(rookPosX - self.position[0])+1):
                            posX = self.position[0] + direction*x

                            if [posX, self.position[1]] in enemyList[1]:
                                allowCastle = False

                            if board[posX][self.position[1]] != "0":
                                if board[posX][self.position[1]] != rook.name or posX != rookPosX:
                                    allowCastle = False

                        if allowCastle:
                            list.append([self.position[0]+direction*2, self.position[1]])

        return list

    def move(self, pos, func_board, simulate=False):

        if not simulate:
            self.hasMoved = True
            if abs(pos[0] - self.position[0]) == 2:
                direction = int(math.copysign(1, (pos[0] - self.position[0])))
                for rook in self.rooks:
                    if (rook.position[0] - self.position[0]) * direction >0:
                        rook.move([self.position[0] + direction, self.position[1]], func_board, False)

        super().move(pos, func_board)




### Functions

def get_pos_on_board(position, height, width):
    x = int(position[0]//(width/8))
    y = int(position[1]//(height/8))

    return [x,y]

def get_pos_on_screen(position, height, width):
    x = int(position[0] * (width/8))
    y = int(position[1] * (width/8))

    return (x,y)

def check_check(color, depth, func_board, func_piece_dict):
    depth = depth-1
    list = []
    check = False

    for indexX, column in enumerate(func_board):
        for indexY, square in enumerate(column):
            if square != "0":
                currentPiece = func_piece_dict[func_board[indexX][indexY]]
                if currentPiece.color != color:
                    list.extend(currentPiece.possiblePositions(func_board, depth))
                elif currentPiece.type == "k":
                    own_king = currentPiece

    if own_king.position in list:
        check = True
    return check, list

def can_move(color, func_board, func_piece_dict):
    for indexX, column in enumerate(func_board):
        for indexY, square in enumerate(column):
            if square != "0":
                currentPiece = func_piece_dict[func_board[indexX][indexY]]
                if currentPiece.color == color:
                    if currentPiece.possiblePositions(func_board):
                       return True
    return False

def count_free_spaces(func_board):
    counter = 0
    for y in func_board:
        for x in y:
            if x == "0":
                counter += 1
    return counter



### initialize board

# 8x8 2-dimensional list for game board
board = []
for i in range(8):
    board.append([])
    for e in range(8):
        board[i].append("0")


### Initialising all pieces
bp1 = pawn(0, [0, 1], "bp1")
bp2 = pawn(0, [1, 1], "bp2")
bp3 = pawn(0, [2, 1], "bp3")
bp4 = pawn(0, [3, 1], "bp4")
bp5 = pawn(0, [4, 1], "bp5")
bp6 = pawn(0, [5, 1], "bp6")
bp7 = pawn(0, [6, 1], "bp7")
bp8 = pawn(0, [7, 1], "bp8")

br1 = rook(0, [0, 0], "br1")
bkn1 = knight(0, [1, 0], "bkn1")
bb1 = bishop(0, [2, 0], "bb1")
bq = queen(0, [3, 0], "bq")
bk = king(0, [4, 0], "bk")
bb2 = bishop(0, [5, 0], "bb2")
bkn2 = knight(0, [6, 0], "bkn2")
br2 = rook(0, [7, 0], "br2")

wp1 = pawn(1, [0, 6], "wp1")
wp2 = pawn(1, [1, 6], "wp2")
wp3 = pawn(1, [2, 6], "wp3")
wp4 = pawn(1, [3, 6], "wp4")
wp5 = pawn(1, [4, 6], "wp5")
wp6 = pawn(1, [5, 6], "wp6")
wp7 = pawn(1, [6, 6], "wp7")
wp8 = pawn(1, [7, 6], "wp8")

wr1 = rook(1, [0, 7], "wr1")
wkn1 = knight(1, [1, 7], "wkn1")
wb1 = bishop(1, [2, 7], "wb1")
wq = queen(1, [3, 7], "wq")
wk = king(1, [4, 7], "wk")
wb2 = bishop(1, [5, 7], "wb2")
wkn2 = knight(1, [6, 7], "wkn2")
wr2 = rook(1, [7, 7], "wr2")

for currentPiece in [
    wp1, wp2, wp3, wp4, wp5, wp6, wp7, wp8,
    wr1, wkn1, wb1, wq, wk, wb2, wkn2, wr2,
    bp1, bp2, bp3, bp4, bp5, bp6, bp7, bp8,
    br1, bkn1, bb1, bq, bk, bb2, bkn2, br2
]:
    board[currentPiece.position[0]][currentPiece.position[1]] = currentPiece.name

### Identify piece by name ###
piece_dict = {
    "wp1": wp1, "wp2": wp2, "wp3": wp3, "wp4": wp4,
    "wp5": wp5, "wp6": wp6, "wp7": wp7, "wp8": wp8,

    "wr1": wr1, "wkn1": wkn1, "wb1": wb1, "wq": wq,
    "wk": wk, "wb2": wb2, "wkn2": wkn2, "wr2": wr2,

    "bp1": bp1, "bp2": bp2, "bp3": bp3, "bp4": bp4,
    "bp5": bp5, "bp6": bp6, "bp7": bp7, "bp8": bp8,

    "br1": br1, "bkn1": bkn1, "bb1": bb1, "bq": bq,
    "bk": bk, "bb2": bb2, "bkn2": bkn2, "br2": br2
}

color_dict = {0: "Black", 1: "White"}
bk.find_rooks(board)
wk.find_rooks(board)

new_pieces = []

### PYGAME LOOP ###
updateScreen = True
piece_selected = False
turn = 1
runGame = True
pawncounter = 0
freeSpaces = count_free_spaces(board)

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

                    for x in board:
                        for y in x:
                            if y != "0":
                                pawn = piece_dict[y]
                                if pawn.type == "p":
                                    pawn.allowEnPassant = False

                    selectedPiece.move(selectedSquare, board)
                    tempFreeSpaces = count_free_spaces(board)

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

                if check_check(turn, 2, board, piece_dict)[0] and not can_move(turn, board, piece_dict):
                    print(f"{color_dict[1 - turn]} wins!!")
                    runGame = False
                elif not can_move(turn, board, piece_dict):
                    print("draw")
                    runGame = False

            elif board[selectedSquare[0]][selectedSquare[1]] != "0":
                selectedPiece = piece_dict[board[selectedSquare[0]][selectedSquare[1]]]
                if selectedPiece.color == turn:
                    piece_selected = True
                    possibleMoves = selectedPiece.possiblePositions(board)

    ### Draw Screen ###
    for indexX, x in enumerate(board):
        for indexY, y in enumerate(x):
            if((indexY + indexX)%2 == 0):
                pygame.draw.rect(screen, whitecolor, (indexX*(width/8), indexY*(height/8), (indexX+1)*(width/8), (indexY+1)*(height/8)))
            else:
                pygame.draw.rect(screen, darkcolor, (indexX * (width / 8), indexY * (height / 8), (indexX + 1) * (width / 8), (indexY + 1) * (height / 8)))

            if y != "0":
                screen.blit(sprite_dict[piece_dict[y].type][piece_dict[y].color], ((indexX*(width/8) + width/32, indexY*(height/8) + height/32)))

    if piece_selected:
        for move in possibleMoves:
            circlePos = get_pos_on_screen(move, height, width)
            pygame.draw.circle(screen, (0,255,0), (int(circlePos[0]+width/16), int(circlePos[1]+height/16)), 15)

    if updateScreen:
        pygame.display.update()
        updateScreen = False
