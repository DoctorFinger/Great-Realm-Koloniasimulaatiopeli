import pygame
import sys
import random

# Vakiot
FRAMES_PER_SECOND = 30
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_PADDING = 4
CELLS_IN_GRID = 9
CELL_SIZE = WINDOW_WIDTH // CELLS_IN_GRID 

# Värit
COLOR_WHITE = (200, 200, 200)
COLOR_BLACK = (0, 0, 0)
FONT_COLOR_ACTIVE = (52, 52, 54)
FONT_COLOR_INACTIVE = (255, 255, 255)

# Alusta Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5))
pygame.display.set_caption("Sudoku Solver")
clock = pygame.time.Clock()

# Kuvat
CELL_BACKGROUND_INACTIVE =  pygame.image.load("cell-background-inactive.png").convert_alpha();
CELL_BACKGROUND_INACTIVE =  pygame.transform.scale(CELL_BACKGROUND_INACTIVE, (CELL_SIZE, CELL_SIZE))
CELL_BACKGROUND_ACTIVE =    pygame.image.load("cell-background-active.png").convert_alpha();
CELL_BACKGROUND_ACTIVE =    pygame.transform.scale(CELL_BACKGROUND_ACTIVE, (CELL_SIZE, CELL_SIZE))
CELL_BACKGROUND_HOVER =    pygame.image.load("cell-background-hover.png").convert_alpha();
CELL_BACKGROUND_HOVER =    pygame.transform.scale(CELL_BACKGROUND_HOVER, (CELL_SIZE, CELL_SIZE))
BOARD_BACKGROUND =          pygame.image.load("board-background.jpg").convert();
BOARD_BACKGROUND =          pygame.transform.scale(BOARD_BACKGROUND, (WINDOW_WIDTH, WINDOW_HEIGHT));
MAINMENU_LOGO =                pygame.image.load("sudoku-logo.png").convert_alpha();   

# Fontit
DEFAULT_FONT = pygame.font.Font("montserrat_alternates_semibold.ttf", 36)

# Funktio generoi 9x9 sudokun
def generate_random_sudoku():
    sudoku_board = [[0] * 9 for i in range(9)]
    for grid_row in range(3):
        for grid_column in range(3):
            base_numbers = list(range(1, 10))
            random.shuffle(base_numbers)

            indices_to_zero = random.sample(range(len(base_numbers)), random.randint(3, 8))
            for index in indices_to_zero:
                base_numbers[index] = 0

            for row in range(3):
                for column in range(3):
                    sudoku_board[row + 3 * grid_row][column + 3 * grid_column] = base_numbers[row * 3 + column]

    return sudoku_board


# Funktio piirtää pelilaudan ruudukon
def draw_grid(screen):
    for i in range(1, CELLS_IN_GRID):
        if i % 3 == 0:
            pygame.draw.line(screen, COLOR_WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_HEIGHT), GRID_PADDING)
            pygame.draw.line(screen, COLOR_WHITE, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), GRID_PADDING)


# Funktio piirtää pelilaudan taustan
def draw_grid_background(screen, initial_board, hover_cell = None):
    screen.blit(BOARD_BACKGROUND, (0, 0))
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            x = column * CELL_SIZE
            y = row * CELL_SIZE
            cell_value = initial_board[row][column]

            if cell_value > 0:
                screen.blit(CELL_BACKGROUND_INACTIVE, (x, y))
                
            elif hover_cell is not None and hover_cell == (row, column):
                screen.blit(CELL_BACKGROUND_HOVER, (x, y))
            else:
                screen.blit(CELL_BACKGROUND_ACTIVE, (x, y))


   
# Funktio piirtää pelilaudan numerot
def draw_numbers(screen, board, initial_board):
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            if board[row][column] != 0:
                x = (column * CELL_SIZE) + (CELL_SIZE // 2) 
                y = (row * CELL_SIZE) + (CELL_SIZE // 2)
                text = str(board[row][column])

                if not initial_board[row][column]:
                    draw_text(text, DEFAULT_FONT, FONT_COLOR_ACTIVE, x, y)
                else:
                    draw_text(text, DEFAULT_FONT, FONT_COLOR_INACTIVE, x, y)

      

# Funktio tarkistaa voiko numeron asettaa annettuun paikkaan.
def is_valid(board, row, column, num):
    return (
        num not in board[row] and
        num not in [board[i][column] for i in range(CELLS_IN_GRID)] and
        num not in [board[i][j] for i in range(row // 3 * 3, (row // 3 + 1) * 3) for j in range(column // 3 * 3, (column // 3 + 1) * 3)]
    )

# Funktio ratkaisee sudokun(Ei toimi)
def solve_sudoku(board):
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            if board[row][column] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, column, num):
                        board[row][column] = num

                        if solve_sudoku(board):
                            return True  
                        board[row][column] = 0  # Onko kelvollinen vastaus?
                return False
    return True

# Funtktio täyttää sudokulaudan 
def fill_board(board, initial_board):
    for i in range(CELLS_IN_GRID):
        for j in range(CELLS_IN_GRID):
            board[i][j] = initial_board[i][j]

# Funktio hakee rivin ja sarakkeen hiiren sijainnin perusteella
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    row = y // CELL_SIZE
    column = x // CELL_SIZE
    return row, column

# Funktio piirtää tekstin
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Funktio piirtää päävalikon
def draw_main_menu(menu:dict):
    pygame.draw.rect(screen, dict.color, (dict.start.x, dict.start.y, dict.start.width, dict.start.height));
    return 

# Funktio piirtää päävalikon
def draw_main_menu():
    screen.fill(COLOR_WHITE)
    screen.blit(MAINMENU_LOGO, ((WINDOW_WIDTH - MAINMENU_LOGO.get_width()) // 2, 75))
    draw_text("Press Space to Play", DEFAULT_FONT, COLOR_BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    draw_text("Press Q to Quit", DEFAULT_FONT, COLOR_BLACK, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)

# Funktio sammuttaa pelin
def exit_game():
    pygame.quit(); 
    sys.exit()

# Funktio avaa pelin
def run_game():
    board = [[0] * CELLS_IN_GRID for i in range(CELLS_IN_GRID)]
    initial_board = generate_random_sudoku()
    fill_board(board, initial_board)
    paused = True
    hover_cell = None

    while True:

        # Käsitellään Pygame-tapahtumat.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Käsitellään näppäimistötapahtumat.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_q:
                    exit_game();

                elif event.unicode.isdigit():
                    if hover_cell is not None and not initial_board[hover_cell[0]][hover_cell[1]]:
                        board[hover_cell[0]][hover_cell[1]]  = int(event.unicode)

            # Käsitellään hiiren vieritystapahtumat, vaihtaa numeroa hiiren vierityksellä
            elif not paused and event.type == pygame.MOUSEWHEEL:
                if hover_cell is not None and not initial_board[hover_cell[0]][hover_cell[1]]:
                    num = board[hover_cell[0]][hover_cell[1]] + int(event.y)
                    if(num < 0):
                        num = 9
                    if(num > 9):
                        num = 0
                    board[hover_cell[0]][hover_cell[1]]  =  num
 
            # Käsitellään hiiren painallustapahtumat, vaihtaa solun numeroa klikkauksesta
            elif not paused and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    row, column = get_mouse_pos()
                    if not initial_board[row][column]:
                        num = board[row][column]
                        num = (num + 1) % 10  
                        board[row][column] = num

            # Hankkii hiiren tämänhetkeisen paikan verrattuna soluun
            elif not paused and event.type == pygame.MOUSEMOTION:
                hover_cell = get_mouse_pos()

        # Piirtää pelin
        if not paused:
            draw_grid_background(screen, initial_board, hover_cell)
            draw_grid(screen)
            draw_numbers(screen, board, initial_board)

        # Piirtää pelivalikon
        else:
            draw_main_menu()

        
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

def main():
    run_game();

main()