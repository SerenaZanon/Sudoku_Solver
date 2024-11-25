import time
import random


"""
'set_up_sudoku' function does not take parameters in input but return a list of lists 
representing the board of the puzzle
Its aim is to retrieve from a .txt file a random sudoku and format it as a list of lists 
Each list is a row of the puzzle
The use will see the number of the chosen sudoku   
"""


def set_up_sudoku() -> list[list]:
    file = open("./datasets/sudoku.txt").readlines()
    sudoku_number = random.randint(0, 25)
    print("number chosen: ", sudoku_number)
    sudoku_text = file[sudoku_number]
    sudoku_matrix = []
    r = 0
    while r < 9:
        c = 0
        sudoku_row = []
        while c < 9:
            if sudoku_text[c + 9 * r].isnumeric():
                sudoku_row.append(sudoku_text[c + 9 * r])
            c += 1
        sudoku_matrix.append(sudoku_row)
        r += 1
    return sudoku_matrix


"""
'visualize' function takes as parameter a list of lists representing the board of the puzzle
Its aim is to visualize the board in a better way
"""


def visualize(board: list[list]):
    r = 0
    while r < 9:
        if r % 3 == 0:
            print("-------------------------")
        c = 0
        while c < 9:
            if c == 0:
                print("|" + " ", end='')
            print(str(board[r][c]) + " ", end='')
            if c % 3 == 2:
                print("|" + " ", end='')
            c += 1
        print("\n")
        r += 1
    print("-------------------------")


"""
'next_position' function takes as parameters two int, the first representing the number of the row and the second 
the number of the column 
It calculates the position to the right (from a user point of view) of the current position
If the value of column is equal to 9 this means that we have to go to the row below 
"""


def next_position(row: int, column: int) -> (int, int):
    column = column + 1
    if column == 9:
        row = row + 1
        column = 0
    return row, column


"""
'check_row' function takes as parameters 
a list of lists representing the board of the puzzle
an int indicating the row to visit
a string which is the value to check
This function returns True if val is not in the row in input, False otherwise
"""


def check_row(board: list[list], row: int, val: str) -> bool:
    return val not in board[row]


"""
'check_column' function takes as parameters 
a list of lists representing the board of the puzzle
an int indicating the row to visit
a string which is the value to check
This function returns True if val is not in the column in input, False otherwise
"""


def check_column(board: list[list], column: int, val: str) -> bool:
    r = 0
    while r < 9:
        if val == board[r][column]:
            return False
        r += 1
    return True


"""
'check_square' function takes as parameters 
a list of lists representing the board of the puzzle
two int, the first indicating the row and the second indicating the column
a string which is the value to check
This function returns True if val is not in the square of the cell whose coordinates are passed in input
False otherwise
"""


def check_square(board: list[list], row: int, column: int, val: str) -> bool:
    r = row - (row % 3)
    fin_r = r + 3
    while r < fin_r:
        c = column - (column % 3)
        fin_c = c + 3
        while c < fin_c:
            if val == board[r][c]:
                return False
            c += 1
        r += 1
    return True


"""
'check_constraint' function takes as parameters 
a list of lists representing the board of the puzzle
two int, the first indicating the row and the second indicating the column
a string which is the value to check
This function returns True all the 'checks' function return True, False otherwise
"""


def check_constraints(board: list[list], row: int, column: int, val: str) -> bool:
    return check_row(board, row, val) and check_column(board, column, val) and check_square(board, row, column, val)


"""
'reverse_domain' function takes as a parameter a list of values and returns another list
Given the list in input, 'reverse_domain' produces a list containing the values from 1 to 9 
missing in the input list
"""


def reverse_domain(values: list) -> list:
    reverse_values = []
    for val in range(1, 10):
        if str(val) not in values:
            reverse_values.append(val)
    return reverse_values


"""
'values_row' function takes as parameters a list of lists representing the board of the sudoku 
and an int indicating the row to visit 
This function returns a list containing the values (different from 0) contained in the row
"""


def values_row(board: list[list], row: int) -> list:
    domain_row = []
    c = 0
    while c < 9:
        if board[row][c] != "0":
            domain_row.append(board[row][c])
        c += 1
    return domain_row


"""
'values_column' function takes as parameters a list of lists representing the board of the sudoku 
and an int indicating the column to visit 
This function returns a list containing the values (different from 0) contained in the column
"""


def values_column(board: list[list], column: int) -> list:
    domain_column = []
    r = 0
    while r < 9:
        if board[r][column] != "0":
            domain_column.append(board[r][column])
        r += 1
    return domain_column


"""
'values_square' function takes as parameters a list of lists representing the board of the sudoku 
and two int, the first indicating the row and the second the column 
This function returns a list containing the values (different from 0) contained in the square of the cell whose 
coordinates are passed in input
"""


def values_square(board: list[list], row: int, column: int) -> list:
    domain_square = []
    r = row - (row % 3)
    fin_r = r + 3
    while r < fin_r:
        c = column - (column % 3)
        fin_c = c + 3
        while c < fin_c:
            if board[r][c] != "0":
                domain_square.append(board[r][c])
            c += 1
        r += 1
    return domain_square


"""
'calculate_domain' function takes as parameters a list of lists representing the board of the sudoku 
and two int, the first indicating the row and the second the column
Its aim is to find the possible values that the cell whose coordinates are passed in input can assume 
"""


def calculate_domain(board: list[list], row: int, column: int) -> list:
    domain_row = values_row(board, row)
    domain_column = values_column(board, column)
    domain_square = values_square(board, row, column)

    missing_row = reverse_domain(domain_row)
    missing_column = reverse_domain(domain_column)
    missing_square = reverse_domain(domain_square)

    dom = list(set(missing_row) & set(missing_column) & set(missing_square))
    return dom


"""
'solution' function takes as parameters a list of lists representing the board of the sudoku 
and two int, the first indicating the row and the second the column which will be (0, 0) (first cell of the board)
In this function the board is filled as follows:
If the row in input is equal to 9 then we have reached the bottom of the board, so we have finished
If the value of the cell is not 0 we skip to the next position
If the value of the cell is 0
    We calculate its domain and for each possible value we control if the constraints are respected
    In case this value is not good we set this cell again to 0
"""


def solution(board: list[list], row: int, column: int) -> bool:
    if row == 9:
        return True
    elif board[row][column] != "0":
        new_row, new_column = next_position(row, column)
        return solution(board, new_row, new_column)
    else:
        domain = calculate_domain(board, row, column)
        for val in domain:
            if check_constraints(board, row, column, val):
                board[row][column] = val
                new_row, new_column = next_position(row, column)
                if solution(board, new_row, new_column):
                    return True
            board[row][column] = "0"
        return False


"""
'main' function takes no parameters and returns nothing
It call the 'set_up_sudoku' function, the 'solution' function and the 'visualize' function
It also tells us what was the execution time 
"""


def main():
    puzzle = set_up_sudoku()
    visualize(puzzle)
    solution(puzzle, 0, 0)
    visualize(puzzle)


main()


"""
FOR EXPERIMENTS
"""


"""
'execution' function takes as parameter a list of lists representing the board of the puzzle and returns a float number 
Its aim is to calculate the execution time of the 'solution' function which is given by 
the ending time minus the starting time of the execution

def execution(board: list[list]) -> [float, bool]:
    start = time.time()
    result = solution(board, 0, 0)
    end = time.time()
    return [(end - start), result]
"""

"""
def set_up_experiments(sudoku_text: str) -> list[list]:
    sudoku_matrix = []
    r = 0
    while r < 9:
        c = 0
        sudoku_row = []
        while c < 9:
            if sudoku_text[c + 9 * r].isnumeric():
                sudoku_row.append(sudoku_text[c + 9 * r])
            c += 1
        sudoku_matrix.append(sudoku_row)
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
