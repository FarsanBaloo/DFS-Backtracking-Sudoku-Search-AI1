import time
import copy


def render(state):
    """ Function handels printing the board states"""

    print("============================")
    for row in state:
        print(row)
    print("============================")


def read_board():
    """Function handels the load of the Sudoku games from a file."""
    with open('Assignment 2 sudoku.txt', 'r') as f:
        lines = f.readlines()
        sudokugames = []
        sudokugame = []
        for line in lines:
            if line.strip().isdigit():
                line = [int(x) for x in line.strip()]
                sudokugame.append(line)
                if len(sudokugame) == 9:
                    sudokugames.append(sudokugame.copy())
                    sudokugame.clear()
                    continue
    return sudokugames


def iscomplete(currentsolution):
    """ Function check that all variable has a value assigned "complete" and not partial & the sum of the row is 45"""

    for row in currentsolution:
        if 0 in row or not sum(row) == 45:
            return False
    return True


def selectunassignedvariable(currentsolution):
    """ Function handels selecting next unassigned variable "static ordering"
    not effectiv" rewrite if i can manage do MRV """

    for row in range(9):
        for column in range(9):
            if currentsolution[row][column] == 0:
                return row, column


def orderdomainvalues():
    """ Function returns the order how domain values is choosen "fixed increassing" for  each variabel"
        implement this beather infuture to limit the branching factor """
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


def inference(row, column, currentsolution):
    """ Function handels interference not yet impelemented will do in future"""
    # How to apply AC-3?
    return True


def isconsistent(currentsolution, row, column, value):
    """"" Function checks the constrains to limit the search space  """

    # That no value is in same row or column
    for index in range(9):
        if currentsolution[row][index] == value or currentsolution[index][column] == value:
            return False

    # That value exist only one time in 3x3 box
    # calculate starting index for row and column for the 3*3 box
    rowstart = (row // 3) * 3
    columnstart = (column // 3) * 3

    for row in range(rowstart, rowstart + 3):
        for column in range(columnstart, columnstart + 3):
            if currentsolution[row][column] == value:
                return False

    # current guessed domain value for the variabel follows all constrins and is consistent
    return True


def backtrack(currentsolution):

    # Base case Check if the current solution is complete / the goal
    if iscomplete(currentsolution):
        return currentsolution

    # Get the first unassigned variable row and column and start solving the suduko
    row, column = selectunassignedvariable(currentsolution)

    # Guess next value from the domain (fixed increasing) not goood implemented
    for value in orderdomainvalues():
        # Is the current domain value consistent with current state regarding the constrains
        if isconsistent(currentsolution, row, column, value):
            # Then assign current guessed domain value to current variable
            currentsolution[row][column] = value
            # inference is not implemented "future function" always return true ,  AC-3,forward checking?
            if inference(row, column, currentsolution):
                # Recursively try to solve the board
                result = backtrack(currentsolution)
                if result:
                    return result

        # If current guess of domain value is not consistent "folow the constrains" remove it from current variabel
        currentsolution[row][column] = 0

    return False


def main():
    # Read the board from the file and get the initialstates
    initialstates = read_board()

    currentsolutions = copy.deepcopy(initialstates)
    finalsolutions = []

    starttime = time.time()
    # Start solv each Suduko from its initialstate and render it and its Goal state for end user
    for sudukonumber in range(len(initialstates)):

        solution = backtrack(currentsolutions[sudukonumber])

        finalsolution = copy.deepcopy(solution)
        finalsolutions.append(finalsolution)

        print('Sudoku:', sudukonumber + 1, '(Initialstate)')
        render(initialstates[sudukonumber])

        if not finalsolution:
            finalsolutions.append(["No Solution"])
            print("There is no solution for Sudoku: ,", sudukonumber + 1)
        else:
            print(f'Sudoku:', sudukonumber + 1, '(Goalstate)')
            render(finalsolutions[sudukonumber])

    stoptime = time.time()
    print(f"Time to solv:", stoptime - starttime)


if __name__ == "__main__":
    main()



