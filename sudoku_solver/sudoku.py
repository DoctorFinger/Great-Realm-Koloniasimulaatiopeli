import random
import copy 



def find_invalid_cells(board):
    invalid_numbers = set()  # Use a set to avoid duplicates

    # Get invalid numbers in rows
    for row_index, row in enumerate(board):
        for num in range(1, 10):
            if num not in row:
                invalid_numbers.add((row_index, row.index(num) if num in row else None))

    # Get invalid numbers in columns
    for col_index in range(9):
        column = [board[row_index][col_index] for row_index in range(9)]
        for num in range(1, 10):
            if num not in column:
                invalid_numbers.add((column.index(num) if num in column else None, col_index))

    # Get invalid numbers in 3x3 squares
    for i in range(3):
        for j in range(3):
            square = [board[3*i + x][3*j + y] for x in range(3) for y in range(3)]
            for num in range(1, 10):
                if square.count(num) != 1:
                    for x in range(3):
                        for y in range(3):
                            if board[3*i + x][3*j + y] == num:
                                invalid_numbers.add((3*i + x, 3*j + y))
    return list(invalid_numbers)  # Convert set back to list for consistent output format

def is_valid_move(grid, row, col, number):
    for x in range( 9 ):
        if grid[row][x] == number:
            return False;

    for x in range( 9 ):
        if grid[x][col] == number:
            return False;

    corner_row = row - row % 3
    corner_col = col - col % 3
    
    for x in range( 3 ):
        for y in range( 3 ):
            if grid[corner_row + x][corner_col + y] == number:
                return False;

    return True;


# rekursiivinen funktio sudokun ratkaisuun
def solve_sudoku( grid, row, col ):
    if col == 9:
        if row == 8:
            return True; # Jos sarake on 9 and rivi 8, sudoku on ratkaistu
    
        row += 1;
        col = 0;
    
    if grid[row][col] > 0:
        return solve_sudoku( grid, row, col + 1 )

    for num in range( 1, 10 ):
        if is_valid_move( grid, row, col, num ):
            grid[row][col] = num;
        
            if solve_sudoku( grid, row, col + 1):
                return True;
    
        grid[row][col] = 0

    return False


def create_solved_board():
    empty_board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(empty_board, 0, 0)
    return empty_board


def create_starting_board(difficulty:float=0.5)->list:
    solved_board = create_solved_board();
    if difficulty < 0 or difficulty > 1:
        raise ValueError("Difficulty must be between 0 and 1")

    new_board = copy.deepcopy(solved_board)
    for i in range(9):
        for j in range(9):
            if random.random() > difficulty:
                new_board[i][j] = 0

    return new_board

def is_valid_sudoku(board):
    # Set containing valid elements for sudoku
    valid_elements = set(range(1, 10))
    
    # Check rows
    for row in board:
        if set(row) != valid_elements: 
            return False

    # Check columns
    for col in zip(*board):
        if set(col) != valid_elements: 
            return False

    # Check sub-grids
    for i in range(3, 10, 3):
        for j in range(3, 10, 3):
            subgrid_elements = {(board[q][w]) for w in range(j-3, j) for q in range(i-3, i)}
            if valid_elements != subgrid_elements:
                return False
            
    return True


