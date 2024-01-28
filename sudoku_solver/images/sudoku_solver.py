import pygame
import pygui
import utils
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
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_DARK_GRAY = (51, 51, 51)
FONT_COLOR_ACTIVE = (52, 52, 54)
FONT_COLOR_INACTIVE = (255, 255, 255)

# Peli tilat
STATE_PAUSED = 1
STATE_PLAYING = 2
STATE_HELP = 3

# Alusta Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5))
pygame.display.set_caption("Sudoku Solver")

# Kuvat
CELL_BACKGROUND_INACTIVE =  utils.load_image("cell-background-inactive.png", CELL_SIZE, CELL_SIZE, True)
CELL_BACKGROUND_ACTIVE =    utils.load_image("cell-background-active.png", CELL_SIZE, CELL_SIZE, True)
CELL_BACKGROUND_HOVER =     utils.load_image("cell-background-hover.png", CELL_SIZE, CELL_SIZE, True)
BOARD_BACKGROUND =          utils.load_image("board-background.jpg", WINDOW_WIDTH, WINDOW_HEIGHT, False)
MAINMENU_LOGO          =    utils.load_image("sudoku-logo.png", None, None, True)   
ESC_KEY_IMAGE =             utils.load_image("esc-key-dark.png", 55, 55, True)   
Q_KEY_IMAGE =               utils.load_image("q-key-dark.png", 55, 55, True)  

# Fontit
DEFAULT_FONT = pygame.font.Font("montserrat_alternates_semibold.ttf", 36)
HELP_FONT = pygame.font.Font("montserrat_alternates_semibold.ttf", 30)

#Päävalikon painikkeiden vakiot
BUTTON_GAP = 10
BUTTON_HEIGHT = 50
BUTOTN_TOP = 250

# Päävalikon painikkeiden tyylit
BUTTON_STYLE = pygui.Style(
    border_radius=50, 
    font=DEFAULT_FONT,
    background_color = pygui.Color(255, 0, 0)
);
BUTTON_STYLE_HOVER = pygui.Style(
    border_radius=50, 
    font=DEFAULT_FONT,
    background_color = pygui.Color(0, 0, 255),
    text_color= pygui.Color(0, 255, 0),
);

# Päävalikon painikkeet, loin customin gui kirjaston, renderöi tällä hetkellä vain nappeja
play_button =    pygui.Button("Play", pygui.Pos("50%", BUTOTN_TOP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER)
help_button =    pygui.Button("Help", pygui.Pos("50%", play_button.position.y + play_button.size.y + BUTTON_GAP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER)
restart_button = pygui.Button("Restart", pygui.Pos("50%", help_button.position.y + help_button.size.y + BUTTON_GAP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER)
quit_button =    pygui.Button("Quit", pygui.Pos("50%", restart_button.position.y + restart_button.size.y + BUTTON_GAP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER)

# Loin luokan pelin tilalle jotta voin jakaa ja asettaa sen funktioiden välillä
class GameState:
   state = None
   def __init__(self, state:int):
       self.state = state
   def get(self):
       return self.state
   def set(self, state:int):
      self.state = state

# Generoi 9x9 aloitus sudoku lauta, ei generoi sääntöjen mukaista lautaa, pitäisi tehdä uudelleen: https://youtu.be/ok-kB9ZCm60?si=IhiKOtbCCdxTP3M7
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

# Funktio tarkistaa voiko numeron asettaa annettuun paikkaan.
def is_valid(active_board, row, column, num):
    return (
        num not in active_board[row] and
        num not in [active_board[i][column] for i in range(CELLS_IN_GRID)] and
        num not in [active_board[i][j] for i in range(row // 3 * 3, (row // 3 + 1) * 3) for j in range(column // 3 * 3, (column // 3 + 1) * 3)]
    )

# Funktio ratkaisee sudokulaudan(Ei toimi)
def solve_sudoku(active_board):
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            if active_board[row][column] == 0:
                for num in range(1, 10):
                    if is_valid(active_board, row, column, num):
                        active_board[row][column] = num
                        if solve_sudoku(active_board):
                            return True  
                        active_board[row][column] = 0  # Onko kelvollinen vastaus?
                return False
    return True

# Funtktio täyttää sudokulaudan 
def copy_board(starting_board):
    active_board = [[0] * CELLS_IN_GRID for _ in range(CELLS_IN_GRID)]
    for i in range(CELLS_IN_GRID):
        for j in range(CELLS_IN_GRID):
            active_board[i][j] = starting_board[i][j]
    return active_board

# Funktio hakee rivin ja sarakkeen hiiren sijainnin perusteella
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    row = y // CELL_SIZE
    column = x // CELL_SIZE
    return row, column

# Funktio piirtää sudoku ruudukon
def draw_grid(screen):
    for i in range(1, CELLS_IN_GRID):
        if i % 3 == 0:
            pygame.draw.line(screen, COLOR_WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_HEIGHT), GRID_PADDING)
            pygame.draw.line(screen, COLOR_WHITE, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), GRID_PADDING)

# Piirtää pelilaudan taustan
def draw_grid_background(screen, starting_board, hovered_cell = None):
    screen.blit(BOARD_BACKGROUND, (0, 0))
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            x = column * CELL_SIZE
            y = row * CELL_SIZE
            cell_value = starting_board[row][column]

            if cell_value > 0:
                screen.blit(CELL_BACKGROUND_INACTIVE, (x, y))
                
            elif hovered_cell is not None and hovered_cell == (row, column):
                    screen.blit(CELL_BACKGROUND_HOVER, (x, y))
            else:
                screen.blit(CELL_BACKGROUND_ACTIVE, (x, y))
   
# Funktio piirtää numerot laudalle
def draw_numbers(screen, active_board, starting_board):
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            if active_board[row][column] != 0:
                x = column * CELL_SIZE + CELL_SIZE // 2 
                y = row * CELL_SIZE + CELL_SIZE // 2
                text = str(active_board[row][column])

                if not starting_board[row][column]:
                    draw_text(screen, text, DEFAULT_FONT, FONT_COLOR_ACTIVE, x, y)
                else:
                    draw_text(screen, text, DEFAULT_FONT, FONT_COLOR_INACTIVE, x, y)

# Funktio piirtää tektiä
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Funktio piirtää päävalikon
def draw_main_menu():
    screen.fill(COLOR_WHITE)
    screen.blit(MAINMENU_LOGO, ((WINDOW_WIDTH - MAINMENU_LOGO.get_width()) // 2, 75))
    play_button.draw(screen)
    help_button.draw(screen)
    restart_button.draw(screen)
    quit_button.draw(screen)

# Funktio piirtää apu valikon
def draw_help_menu():
    render_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    render_surface.fill(COLOR_WHITE)

    # Piirrä apu valikon 'Controls' teksti
    y_offset = 50 
    text_surface = DEFAULT_FONT.render("Game controls:", True, COLOR_DARK_GRAY)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
    render_surface.blit(text_surface, text_rect)

    # Piirrä apu valikon controllien kuvaukset ja kuvakkeet
    control_descriptions = {"ESC": ("Pauses the game",ESC_KEY_IMAGE), "Q": ("Quits the game", Q_KEY_IMAGE)}
    y_offset, x_offset = 100, 100
    gap_y, gap_x = 50, 10

    for key, (description, image) in control_descriptions.items():
        render_surface.blit(image, (x_offset, y_offset))
        description_surface = HELP_FONT.render(description, True, COLOR_DARK_GRAY)
        description_rect = description_surface.get_rect(topleft=(x_offset + image.get_width() + gap_x, y_offset + (image.get_height() - description_surface.get_height()) // 2))
        render_surface.blit(description_surface, description_rect)
        y_offset += gap_y

    screen.blit(render_surface, (0, 0))

# Funktio tarkistaa, voiko käyttäjä muokata hiiren päällä olevaa solua.
def is_hoverable(hovered_cell: list, starting_board:list):
    return hovered_cell is not None and not starting_board[hovered_cell[0]][hovered_cell[1]]

# Funktio sammuttaa pelin
def exit_game():
    pygame.quit();
    sys.exit()

# Funktio avaa pelin
def run_game():
    starting_board = generate_random_sudoku()
    active_board =   copy_board(starting_board)
    hovered_cell =   None
    state =          GameState(STATE_PAUSED)
    clock =          pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state.get() == STATE_PAUSED:
                        state.set(STATE_PLAYING)
                    elif state.get() == STATE_PLAYING:
                        state.set(STATE_PAUSED);
                        play_button.set_text("Continue")
                    elif state.get() == STATE_HELP:
                        state.set(STATE_PAUSED)

                if event.unicode.isdigit():
                    if is_hoverable(hovered_cell, starting_board):
                        active_board[hovered_cell[0]][hovered_cell[1]]  = int(event.unicode)

            elif event.type == pygame.MOUSEWHEEL and state.get() is not STATE_PAUSED:
                if is_hoverable(hovered_cell, starting_board):
                    num = active_board[hovered_cell[0]][hovered_cell[1]] + int(event.y)
                    if(num < 0):
                        num = 9
                    if(num > 9):
                        num = 0
                    active_board[hovered_cell[0]][hovered_cell[1]] = num

            elif event.type == pygame.MOUSEBUTTONDOWN and state.get() is not STATE_PAUSED:
                if event.button == 1:  
                    row, column = get_mouse_pos()
                    if not starting_board[row][column]:
                        num = active_board[row][column]
                        num = (num + 1) % 10  
                        active_board[row][column] = num

            elif state.get() is STATE_PAUSED:
                if play_button.is_pressed():
                    state.set(STATE_PLAYING)
                if restart_button.is_pressed():
                    starting_board = generate_random_sudoku()
                    active_board = copy_board(starting_board)
                    hovered_cell = None
                    state.set(STATE_PLAYING)
                if help_button.is_pressed():
                    state.set(STATE_HELP)
                if quit_button.is_pressed():
                    exit_game()
                    

            elif event.type == pygame.MOUSEMOTION and state.get() is not STATE_PAUSED:
                hovered_cell = get_mouse_pos()

      
        if state.get() == STATE_PLAYING:
            draw_grid_background(screen, starting_board, hovered_cell)
            draw_grid(screen)
            draw_numbers(screen, active_board, starting_board)

        elif state.get() == STATE_PAUSED:
            draw_main_menu()
            
        elif state.get() == STATE_HELP:
            draw_help_menu()
            
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)

def main():
    run_game();

main()