'''
    This creates an array of numbers for the main script to interpret as a sudoku board.
    It takes input of an 81 character long string with each character being a number and
    converts those numbers into a two dimensional array.
    It has a board_list parameter which is a .txt file containing the sudoku boards as strings.
'''

import random


def main(board_file):
    try:
        with open(board_file, 'r') as file:
            boards = file.readlines()
            file.close()
            newboards = []
            for i in boards:
                if i.endswith('\n'):
                    i = i.replace('\n', '')
                    newboards.append(i)
            boards = newboards

            randomBoard = boards[random.randint(0, len(boards) - 1)]

            randomBoardArray = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

            for i in range(len(randomBoard)):
                x = i % 9
                y = i // 9
                randomBoardArray[y][x] = int(randomBoard[i])
            return randomBoardArray
    except FileNotFoundError:
        print(f'Error loading board {board_file}')


if __name__ == '__main__':
    print(main(input()))
