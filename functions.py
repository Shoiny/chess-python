### Functions

def get_pos_on_board(position, height, width):
    x = int(position[0]//(width/8))
    y = int(position[1]//(height/8))

    return [x,y]

def get_pos_on_screen(position, height, width):
    x = int(position[0] * (width/8))
    y = int(position[1] * (height/8))

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
                    list.extend(currentPiece.possiblePositions(func_board, func_piece_dict, depth))
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
                    if currentPiece.possiblePositions(func_board, func_piece_dict):
                       return True
    return False

def count_free_spaces(func_board):
    counter = 0
    for y in func_board:
        for x in y:
            if x == "0":
                counter += 1
    return counter