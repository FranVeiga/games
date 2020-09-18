

def validate(board, value, x, y):
    for row in range(len(board[0])):
        if board[y][row] == value and x != row:
            return False

    for column in range(len(board[0])):
        if board[column][x] == value and y != column:
            return False

    blockX = x//3
    blockY = y//3
    for column in range(blockY * 3, blockY * 3 + 3):
        for row in range(blockX * 3, blockX * 3 + 3):
            if board[column][row] == value and (column, row) != (x, y):
                return False

    return True


def find(board):
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == 0:
                return (y, x)

    return None


def solve(board):
    emptyPos = find(board)
    if emptyPos:
        row, column = emptyPos
    else:
        return True

    for i in range(1, 10):
        if validate(board, i, column, row):
            board[row][column] = i

            if solve(board):
                return True

        board[row][column] = 0

    return False


def solveBoard(board):
    solve(board)
    return board
