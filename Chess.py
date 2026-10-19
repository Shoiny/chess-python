import pygame,sys,time, os
from pieces import *
from functions import *
from game_loop import *


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


bk.find_rooks(board, piece_dict)
wk.find_rooks(board, piece_dict)

game_loop(board, piece_dict)