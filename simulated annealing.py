import random
import numpy as np
import math
from random import choice
import statistics
import time


"""
'set_up_sudoku' function does not take parameters in input but return a list of lists 
representing the board of the puzzle
Its aim is to retrieve from a .txt file a random sudoku and format it as a list of lists 
Each list is a row of the puzzle
The use will see the number of the chosen sudoku   
"""


def set_up_sudoku() -> list:
    file = open("./datasets/sudoku.txt").readlines()
    sudoku_number = random.randint(0, 25)
    print("number chosen: ", sudoku_number)
    sudoku_text = file[sudoku_number]
    sudoku_matrix = []
    r = 0
    while r < 9:
        c = 0
        while c < 9:
            if sudoku_text[c + 9 * r].isnumeric():
                if sudoku_text[c + 9 * r] == "0":
                    sudoku_matrix.append("0")
                else:
                    sudoku_matrix.append(sudoku_text[c + 9 * r])
            c += 1
        r += 1
    return sudoku_matrix


"""
'visualize' function takes as parameter a list representing the board of the puzzle
Its aim is to visualize the board in a better way
"""


def visualize(board: list):
    r = 0
    while r < 9:
        if r % 3 == 0:
            print("-------------------------")
        c = 0
        while c < 9:
            if c == 0:
                print("|" + " ", end='')
            print(board[c + 9 * r] + " ", end='')
            if c % 3 == 2:
                print("|" + " ", end='')
            c += 1
        print("\n")
        r += 1
    print("-------------------------")


"""
'fill_board' function takes as parameter a list representing the board of the puzzle
Its aim is to randomly fill the board given that in every single 3x3 block each digit
has to appear only once
"""


def fill_board(board: list):
    r = 0
    while r < 9:
        c = 0
        while c < 9:
            if board[c + 9 * r] == "0":
                found = False
                while not found:
                    val = random.randint(1, 9)
                    if check_square(board, r, c, str(val)):
                        board[c + 9 * r] = val
                        found = True
            c += 1
        r += 1


"""
'check_square' function takes as parameters 
a list representing the board of the puzzle
two int, the first indicating the row and the second indicating the column
a string which is the value to check
This function returns True if val is not in the square of the cell whose coordinates are passed in input
False otherwise
"""


def check_square(board: list, row: int, column: int, val: str) -> bool:
    r = row - (row % 3)
    fin_r = r + 3
    while r < fin_r:
        c = column - (column % 3)
        fin_c = c + 3
        while c < fin_c:
            if val == board[c + 9 * r]:
                return False
            c += 1
        r += 1
    return True


"""
'listing_blocks' function takes as parameter a list representing the board of the puzzle
and returns a pair where
the first element is a list of lists where each list is made by pairs representing the 9 cells' positions of a block
the second element is a list of pairs indicating only the fixed cell, so those cells whose value cannot be modified
"""


def listing_blocks(board: list) -> [list[list], list[list]]:
    pos_list = []
    fixed_cells = []
    row = 0
    column = 0
    num_blocks = 0
    while num_blocks < 9:
        r = row
        fin_r = r + 3
        pos = []
        while r < fin_r:
            c = column
            fin_c = c + 3
            while c < fin_c:
                if board[c + r * 9] != "0":
                    fixed_cells.append([r, c])
                pos.append([r, c])
                c += 1
            r += 1
        pos_list.append(pos)
        column += 3
        if column == 9:
            column = 0
            row += 3
        num_blocks += 1
    return [pos_list, fixed_cells]


"""
'random_cells' function takes as input parameters
a list representing a block of the board
a list of pairs representing the coordinates of the fixed cells
The aim of this function is to choose randomly two no-fixed values of the given block
"""


def random_cells(block: list, fixed_cells: list[list]) -> list[list]:
    fixed_values = []
    i = 0
    while i < len(block):
        if block[i] in fixed_cells:
            fixed_values.append(block[i])
        i += 1
    found = False
    chosen_cells = []
    while not found:
        first = random.choice(block)
        second = choice([box for box in block if box is not first])
        if first not in fixed_values and second not in fixed_cells:
            chosen_cells.append(first)
            chosen_cells.append(second)
            found = True
    return chosen_cells


"""
'switch' function takes in input
a list representing the board of the puzzle
and two coordinates which are swapped 
and returns the modified board 
"""


def switch(board: list, first_pos: list, second_pos: list) -> list:
    tmp_board = np.copy(board)
    temp = tmp_board[first_pos[1] + first_pos[0] * 9]
    tmp_board[first_pos[1] + first_pos[0] * 9] = tmp_board[second_pos[1] + second_pos[0] * 9]
    tmp_board[second_pos[1] + second_pos[0] * 9] = temp
    return tmp_board


"""
'row_cost' function takes as parameter a list representing the board of the puzzle and returns an int value
The returned result is equal to the number of digits that are not unique in each row
"""


def row_cost(board: list) -> int:
    full_cost = 0
    r = 0
    while r < 9:
        occurrences = np.zeros(shape=9)
        c = 0
        while c < 9:
            index = board[c + r * 9].astype(int) - 1
            occurrences[index] += 1
            c += 1
        cost = 0
        for val in occurrences:
            if val != 1:
                cost += 1
        full_cost += cost
        r += 1
    return full_cost


"""
'column_cost' function takes as parameter a list representing the board of the puzzle and returns an int value
The returned result is equal to the number of digits that are not unique in each column
"""


def column_cost(board: list) -> int:
    full_cost = 0
    c = 0
    while c < 9:
        occurrences = np.zeros(shape=9)
        r = 0
        while r < 9:
            index = board[c + r * 9].astype(int) - 1
            occurrences[index] += 1
            r += 1
        cost = 0
        for val in occurrences:
            if val != 1:
                cost += 1
        full_cost += cost
        c += 1
    return full_cost


"""
'cost_function' function takes as parameter a list representing the board of the puzzle and returns an int value
The returned result is equal to the sum of 'cost_row' and 'cost_column'
"""


def cost_function(board: list) -> int:
    return row_cost(board) + column_cost(board)


"""
'calculating_temperature' function takes as parameters
a list representing the board of the puzzle 
a list of lists representing the cells' positions in each block
a list of pairs representing the position of fixed cells
This function returns a float equal to the initial temperature of the algorithm
"""


def calculating_temperature(board: list, blocks: list[list], fixed_cells: list[list]) -> float:
    list_of_costs = []
    tmp_board = board
    for i in range(0, 9):
        tmp_board = new_version_sudoku(tmp_board, blocks, fixed_cells)
        list_of_costs.append(cost_function(tmp_board))
    return statistics.pstdev(list_of_costs)


"""
'new_version_sudoku' function takes as parameters
a list representing the board of the puzzle 
a list of lists representing the cells' positions in each block
a list of pairs representing the position of fixed cells
Its aim is to choose a random block, two random cells in it and swap them giving a new version of the board
"""


def new_version_sudoku(board: list, blocks: list[list], fixed_cells: list[list]) -> list:
    block = random.randint(0, 8)
    chosen_cells = random_cells(blocks[block], fixed_cells)
    new_version = switch(board, chosen_cells[0], chosen_cells[1])
    return new_version


"""
'choose_new_version_sudoku' function takes as parameters
a list representing the board of the puzzle 
a list of lists representing the cells' positions in each block
a list of pairs representing the position of fixed cells
a float which is the initial temperature
Its aim is to compute the delta between the given board and a new version of it
This function returns the new board board and the cost difference if the probability of accepting it is high
otherwise it return the current board and 
"""


def choose_new_version_sudoku(board: list, blocks: list[list], fixed_cells: list[list], temperature: float) \
        -> [list, int]:
    new_version = new_version_sudoku(board, blocks, fixed_cells)
    new_board = new_version
    current_cost = cost_function(board)
    new_cost = cost_function(new_board)
    delta = new_cost - current_cost
    div = math.exp(-delta/temperature)
    if np.random.uniform(1, 0, 1) < div:
        return new_board, delta
    else:
        return board, 0


"""
'solution' function takes as input parameter a list representing the board of the puzzle 
Some variable are stated and until the solution is not found it continue to iterate
It gives back a pair where the first value is the board and the second ids a boolean
If the boolean is equal to True then the board represents the final solution
"""


def solution(board: list) -> list:
    victory = False
    stuck = 0
    reducing_factor = 0.99
    max_iter = 100

    positions_blocks, fixed = listing_blocks(board)
    iterations = len(fixed)
    tmp_board = np.copy(board)
    fill_board(tmp_board)
    temperature = calculating_temperature(tmp_board, positions_blocks, fixed)
    errors = cost_function(tmp_board)

    if errors <= 0:
        victory = True

    while not victory:
        old_errors = errors
        for i in range(0, iterations):
            new_version = choose_new_version_sudoku(tmp_board, positions_blocks, fixed, temperature)
            tmp_board = new_version[0]
            error_diff = new_version[1]
            errors += error_diff
            if errors <= 0:
                victory = True

        temperature = temperature * reducing_factor

        if errors <= 0:
            victory = True
        if errors >= old_errors:
            stuck += 1
        else:
            stuck = 0
        if stuck > max_iter:
            temperature += 2
    return tmp_board


"""
'main' function takes no parameters and returns nothing
It call the 'set_up_sudoku' function, the 'solution' function
It also tells us what was the execution time 
"""


def main():
    puzzle = set_up_sudoku()
    visualize(puzzle)
    result = solution(puzzle)
    visualize(result)


main()

"""
FOR EXPERIMENTS
"""

"""
def solution(board: list) -> [list, bool]:
    victory = False
    stuck = 0
    reducing_factor = 0.99
    MAX_ITER = 100
    n_iter = 0

    positions_blocks, fixed = listing_blocks(board)
    iterations = len(fixed)
    tmp_board = np.copy(board)
    fill_board(tmp_board)
    temperature = calculating_temperature(tmp_board, positions_blocks, fixed)
    errors = cost_function(tmp_board)

    if errors <= 0:
        victory = True

    while not victory and n_iter < MAX_ITER:
        old_errors = errors
        for i in range(0, iterations):
            new_version = choose_new_version_sudoku(tmp_board, positions_blocks, fixed, temperature)
            tmp_board = new_version[0]
            error_diff = new_version[1]
            errors += error_diff
            if errors <= 0:
                victory = True

        temperature = temperature * reducing_factor

        if errors <= 0:
            victory = True
        if errors >= old_errors:
            stuck += 1
        else:
            stuck = 0
        if stuck > MAX_ITER:
            temperature += 2
            n_iter += 1
    return [tmp_board, victory]
"""

"""
'execution' function takes as parameter a list of lists representing the board of the puzzle and returns a float number 
Its aim is to calculate the execution time of the 'solution' function which is given by 
the ending time minus the starting time of the execution

def execution(board: list) -> [float, bool]:
    start = time.time()
    result = solution(board)
    end = time.time()
    return [(end - start), result[1]]
"""

"""
def set_up_experiments(sudoku_text: str) -> list:
    sudoku_matrix = []
    r = 0
    while r < 9:
        c = 0
        while c < 9:
            if sudoku_text[c + 9 * r].isnumeric():
                if sudoku_text[c + 9 * r] == "0":
                    sudoku_matrix.append("0")
                else:
                    sudoku_matrix.append(sudoku_text[c + 9 * r])
            c += 1
        r += 1
    return sudoku_matrix
"""

"""
def experiments(tests: list) -> list:
    costs = []
    for sudoku in tests:
        cost = execution(sudoku)
        costs.append(cost)
    return costs
"""

"""
def visualize_costs(costs, headers):
    print("--------------------------------------------------")
    for i in range(0, 8):
        print("| " + headers[i] + " | " + str(costs[i][0]) + " | " + str(costs[i][1]) + " |")
        print("--------------------------------------------------")
"""

"""
def main():
    tests = []
    file = open("./datasets/experiments.txt").readlines()
    for i in range(0, 8):
        sudoku_text = file[i]
        new_sudoku = set_up_experiments(sudoku_text)
        tests.append(new_sudoku)
    sudoku_costs = experiments(tests)
    headers_table = ["Sudoku 1 easy  ", "Sudoku 2 easy  ", "Sudoku 1 normal", "Sudoku 2 normal", "Sudoku 1 medium",
                     "Sudoku 2 medium", "Sudoku 1 hard  ", "Sudoku 2 hard  "]
    visualize_costs(sudoku_costs, headers_table)


main()
"""