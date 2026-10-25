import math
from copy import deepcopy
from functions import check_check
from game_loop import promote


### piece classes

class piece():
    def __init__(self, color, position, type, name):
        self.color = color
        self.position = position
        self.type = type
        self.name = name

    def piecePositions(self, func_board,func_piece_dict, depth=2):
        pass

    def move(self, pos, func_board,func_piece_dict, simulate=False):
        func_board[self.position[0]][self.position[1]] = "0"
        self.position = pos
        func_board[self.position[0]][self.position[1]] = self.name

    def possiblePositions(self, func_board, func_piece_dict, depth=2):
        if depth == 0:
            return []

        list = self.piecePositions(func_board,func_piece_dict, depth)

        valid_moves = []
        for index, space in enumerate(list):  # Remove spaces with same color piece
            if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                continue

            elif func_board[space[0]][space[1]] != "0" and func_piece_dict[func_board[space[0]][space[1]]].color == self.color:
                continue

            board_copy = deepcopy(func_board)
            current_position = self.position
            self.move(space, board_copy,func_piece_dict, True)
            if check_check(self.color, depth, board_copy, func_piece_dict)[0]:
                pass
            else:
                valid_moves.append(space)
            self.move(current_position, board_copy,func_piece_dict, True)

        return valid_moves



class pawn(piece):
    def __init__(self, color, position, name):
        piece.__init__(self, color, position, "p", name)
        self.hasMoved = False                                                                   # First move identifier
        self.allowEnPassant = False                                                              # Second move identifier for en passant
        self.previousPiece = "0"                                                               # For taking en passant7
        self.doneEnPassant = False
        self.dir = (self.color*2-1)*-1                                                                                 # Direction

    def piecePositions(self, func_board,func_piece_dict, depth=2):
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
                if func_piece_dict[func_board[self.position[0]+(i*2-1)][self.position[1]+self.dir]].color != self.color:   # Taking 1 up and 1 to the side, if there is an opposite color piece
                    list.append([self.position[0]+(i*2-1), self.position[1]+self.dir])

            elif func_board[self.position[0] + (i * 2 - 1)][self.position[1]] != "0":
                tempPiece =  func_piece_dict[func_board[self.position[0] + (i * 2 - 1)][self.position[1]]]
                if tempPiece.type == "p" and tempPiece.color != self.color and tempPiece.allowEnPassant:   # En Passant
                    list.append([self.position[0] + (i * 2 - 1), self.position[1]+self.dir])

        return list

    def move(self, pos, func_board, func_piece_dict, simulate=False):                                           # Move and mark moved
        if simulate and self.doneEnPassant:
            func_board[self.previousPiece.position[0]][self.previousPiece.position[1]] = self.previousPiece.name
            self.doneEnPassant = False
            self.previousPiece = "0"

        if not simulate:
            if pos[1] - self.position[1] == self.dir:
                if abs(pos[0] - self.position[0]) == 1 and func_board[pos[0]][pos[1]] == "0":
                    self.doneEnPassant = True
                    self.previousPiece = func_piece_dict[func_board[pos[0]][pos[1]-self.dir]]
                    func_board[pos[0]][pos[1]-self.dir] = "0"

            if abs(pos[1] - self.position[1]) == 2:
                self.allowEnPassant = True

        super().move(pos, func_board, func_piece_dict)


        if not simulate:
            self.hasMoved = True

            if self.position[1] in [0,7]:                                      # Promotion
                promotionChoice = promote(self.color)
                
                if promotionChoice == 0:
                    newPiece = knight(self.color, self.position, self.name)
                elif promotionChoice == 1:
                    newPiece = bishop(self.color, self.position, self.name)
                elif promotionChoice == 2:
                    newPiece = rook(self.color, self.position, self.name)
                elif promotionChoice == 3:
                    newPiece = queen(self.color, self.position, self.name)

                func_piece_dict[self.name] = newPiece

class knight(piece):
    def __init__(self,color,position,name):
        piece.__init__(self,color,position,"kn",name)

    def piecePositions(self, func_board,func_piece_dict, depth=2):
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

    def piecePositions(self,func_board,func_piece_dict,  depth=2):
        list = []

        for e in [[-1,-1], [-1, 1], [1, -1], [1,1]]:                    # All 4 diagonal directions
            for i in range(7):                                          # Go diagonally until there is a piece of the edge of the board
                space = [self.position[0] + (i+1)*e[0], self.position[1] + (i+1)*e[1]]
                if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                    break

                if func_board[space[0]][space[1]] == "0":

                    list.append(space)
                elif func_piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)
                    break
                else: break

        return list

class rook(piece):
    def __init__(self, color, position,name):
        piece.__init__(self, color, position, "r",name)
        self.hasMoved = False

    def piecePositions(self, func_board,func_piece_dict, depth=2):
        list = []

        for e in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            for i in range(7):
                space = [self.position[0] + (i+1)*e[0], self.position[1] +(i+1)*e[1]]
                if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                    break

                if func_board[space[0]][space[1]] == "0":
                    list.append(space)
                elif func_piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)
                    break
                else:
                    break

        return list

    def move(self, pos, func_board, func_piece_dict, simulate=False):
        super().move(pos, func_board, func_piece_dict)

        if not simulate:
            self.hasMoved = True

class queen(piece):
    def __init__(self, color, position, name):
        piece.__init__(self, color, position, "q", name)

    def piecePositions(self, func_board,func_piece_dict, depth=2):
        list = []

        for e in [[-1,-1], [-1, 1], [1, -1], [1,1],[-1, 0], [1, 0], [0, -1], [0, 1]]:
            for i in range(7):
                space = [self.position[0] + (i+1) * e[0], self.position[1] + (i+1) * e[1]]
                if not (0 <= space[0] <= 7 and 0 <= space[1] <= 7):
                    break

                if func_board[space[0]][space[1]] == "0":
                    list.append(space)
                elif func_piece_dict[func_board[space[0]][space[1]]].color != self.color:
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

    def find_rooks(self, func_board, func_piece_dict):
        for x in func_board:
            for y in x:
                if y != "0":
                    piec = func_piece_dict[y]
                    if piec.type == "r" and piec.color == self.color:
                        self.rooks.append(piec)

    def piecePositions(self, func_board,func_piece_dict, depth=2):
        list = []

        for e in [[-1, -1], [-1, 1], [1, -1], [1, 1], [-1, 0], [1, 0], [0, -1], [0, 1]]:
            space = [self.position[0] + 1 * e[0], self.position[1] + 1 * e[1]]
            if 0 <= space[0] <= 7 and 0 <= space[1] <= 7:

                if func_board[space[0]][space[1]] == "0":
                    list.append(space)
                elif func_piece_dict[func_board[space[0]][space[1]]].color != self.color:
                    list.append(space)

        if not self.hasMoved:                                               # King hasn't moved
            enemyList = check_check(self.color, depth, func_board, func_piece_dict)
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

                            if func_board[posX][self.position[1]] != "0":
                                if func_board[posX][self.position[1]] != rook.name or posX != rookPosX:
                                    allowCastle = False

                        if allowCastle:
                            list.append([self.position[0]+direction*2, self.position[1]])

        return list

    def move(self, pos, func_board,func_piece_dict, simulate=False):

        if not simulate:
            self.hasMoved = True
            if abs(pos[0] - self.position[0]) == 2:
                direction = int(math.copysign(1, (pos[0] - self.position[0])))
                for rook in self.rooks:
                    if (rook.position[0] - self.position[0]) * direction >0 and rook.hasMoved == False:
                        rook.move([self.position[0] + direction, self.position[1]], func_board,func_piece_dict, False)

        super().move(pos, func_board, func_piece_dict)