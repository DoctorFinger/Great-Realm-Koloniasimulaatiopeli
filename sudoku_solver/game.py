import pygame
import pygui
import utils
import sys
import random
import sudoku

# Vakiot
FRAMES_PER_SECOND = 60
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
COLOR_LIGHT_GRAY = (160, 165, 170)
COLOR_DARK_GRAY = (51, 51, 51)
FONT_COLOR_ACTIVE = (52, 52, 54)
FONT_COLOR_INACTIVE = (255, 255, 255)

# Peli tilat
STATE_PAUSED = 1
STATE_PLAYING = 2
STATE_COMPLETED = 3
STATE_HELP = 4

# Alusta Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5))
pygame.display.set_caption("Sudoku Solver")

# Kuvat
CELL_BACKGROUND_INACTIVE =  utils.load_image("images/cell-background-inactive.png", CELL_SIZE, CELL_SIZE, True)
CELL_BACKGROUND_ACTIVE =    utils.load_image("images/cell-background-active.png", CELL_SIZE, CELL_SIZE, True)
CELL_BACKGROUND_HOVER =     utils.load_image("images/cell-background-hover.png", CELL_SIZE, CELL_SIZE, True)
BOARD_BACKGROUND =          utils.load_image("images/board-background.jpg", WINDOW_WIDTH, WINDOW_HEIGHT, False)
MAINMENU_LOGO =             utils.load_image("images/sudoku-logo.png", None, None, True)   
KEY_IMAGE_ESC =             utils.load_image("images/esc-key-dark.png", 55, 55, True)   
KEY_IMAGE_Q =               utils.load_image("images/q-key-dark.png", 55, 55, True)  

# Äänet
BUTTON_CLICK_SOUND = utils.load_sound("sounds/button_click.wav")

# Fontit
DEFAULT_FONT = pygame.font.Font("montserrat_alternates_semibold.ttf", 36)
COMPLETION_FONT_TITLE = pygame.font.Font("montserrat_alternates_semibold.ttf", 42)
COMPLETION_FONT_PARAGRAPH = pygame.font.Font("montserrat_alternates_semibold.ttf", 30)
CHOOSE_DIFFICULTY_FONT = pygame.font.Font("montserrat_alternates_extrabold.ttf", 36)
HELP_FONT = pygame.font.Font("montserrat_alternates_semibold.ttf", 30)

#Päävalikon painikkeiden vakiot
BUTTON_GAP = 10
BUTTON_HEIGHT = 50
BUTOTN_TOP = 250

# Päävalikon painikkeiden tyylit
BUTTON_STYLE = pygui.Style(
    border_radius=50, 
    font=DEFAULT_FONT,
    background_color = pygui.Color(255, 0, 0, 255),
);
BUTTON_STYLE_HOVER = pygui.Style(
    border_radius=50, 
    font=DEFAULT_FONT,
    background_color = pygui.Color(62, 40, 185, 255),
    text_color= pygui.Color(255, 255, 255, 255)
);
PARAGRAPH_STYLE = pygui.Style(
    font=DEFAULT_FONT,
    background_color = pygui.Color(255, 0, 0, 255),
    text_color= pygui.Color(255, 255, 255, 255),
    border_radius=15
);

# Päävalikon painikkeet, loin customin gui kirjaston, renderöi tällä hetkellä vain nappeja
play_button =           pygui.Button("Play", pygui.Pos("50%", BUTOTN_TOP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
help_button =           pygui.Button("Help", pygui.Pos("50%", play_button.position.y + play_button.size.y + BUTTON_GAP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
restart_button =        pygui.Button("Restart", pygui.Pos("50%", help_button.position.y + help_button.size.y + BUTTON_GAP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
quit_button =           pygui.Button("Quit", pygui.Pos("50%", restart_button.position.y + restart_button.size.y + BUTTON_GAP), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
completion_button =     pygui.Button("Main Menu", pygui.Pos("50%", "50%"), pygui.Size(300, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
easy_button =           pygui.Button("Easy", pygui.Pos("50%", (60 * 2 + BUTTON_GAP) + 100), pygui.Size(400, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
medium_button =         pygui.Button("Medium", pygui.Pos("50%", (60 * 3 + BUTTON_GAP)+ 100), pygui.Size(400, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
hard_button =           pygui.Button("Hard", pygui.Pos("50%", (60 * 4 + BUTTON_GAP) + 100), pygui.Size(400, BUTTON_HEIGHT), BUTTON_STYLE, BUTTON_STYLE_HOVER, BUTTON_CLICK_SOUND)
difficulty_text =       pygui.Paragraph("Select difficulty", pygui.Pos("50%", 98), pygui.Size(400, 120), PARAGRAPH_STYLE)


# Loin luokan pelin tilalle jotta voin jakaa ja asettaa sen funktioiden välillä
class GameState:
   state = None
   def __init__(self, state:int):
       self.state = state
   def get(self):
       return self.state
   def set(self, state:int):
      self.state = state

# Funtktio kopio sudokulaudan 
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
def draw_grid_background(screen, starting_board, hovered_cell=None):
    screen.blit(BOARD_BACKGROUND, (0, 0))
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            x = column * CELL_SIZE
            y = row * CELL_SIZE
            cell_value = starting_board[row][column]

            if cell_value > 0:
                screen.blit(CELL_BACKGROUND_INACTIVE, (x, y))
            elif hovered_cell is not None and (row == hovered_cell[0] or column == hovered_cell[1]):
                screen.blit(CELL_BACKGROUND_HOVER, (x, y))
            else:
                screen.blit(CELL_BACKGROUND_ACTIVE, (x, y))


# Funktio piirtää numerot laudalle
def draw_numbers(screen, active_board, starting_board, invalid_cells):
    for row in range(CELLS_IN_GRID):
        for column in range(CELLS_IN_GRID):
            if active_board[row][column] != 0:
                x = column * CELL_SIZE + CELL_SIZE // 2 
                y = row * CELL_SIZE + CELL_SIZE // 2
                text = str(active_board[row][column])
                color = FONT_COLOR_ACTIVE if not starting_board[row][column] else FONT_COLOR_INACTIVE
                
                if (row, column) in invalid_cells:
                    draw_text(screen, text, DEFAULT_FONT, (255, 0, 0), x, y)  # Red color for invalid cells
                else:
                    draw_text(screen, text, DEFAULT_FONT, color, x, y)


# Funktio piirtää tektiä
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Piirtää vaikeustason valikon, ei ole vielä pelissä
def draw_difficulty_selection_menu(screen):
    screen.fill(COLOR_LIGHT_GRAY)
    difficulty_text.draw(screen)
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

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
    control_descriptions = {"ESC": ("Pauses the game",KEY_IMAGE_ESC), "Q": ("Quits the game", KEY_IMAGE_Q)}
    y_offset, x_offset = 100, 100
    gap_y, gap_x = 50, 10

    for key, (description, image) in control_descriptions.items():
        render_surface.blit(image, (x_offset, y_offset))
        description_surface = HELP_FONT.render(description, True, COLOR_DARK_GRAY)
        description_rect = description_surface.get_rect(topleft=(x_offset + image.get_width() + gap_x, y_offset + (image.get_height() - description_surface.get_height()) // 2))
        render_surface.blit(description_surface, description_rect)
        y_offset += gap_y

    screen.blit(render_surface, (0, 0))

def draw_completion_screen(screen):
    rect_width = WINDOW_WIDTH 
    rect_height = WINDOW_HEIGHT // 2
    
    victory_text = COMPLETION_FONT_TITLE.render("Congratulations!", True, COLOR_DARK_GRAY)
    victory_text2 = COMPLETION_FONT_PARAGRAPH.render("You solved the Sudoku", True, COLOR_DARK_GRAY)
    text_rect = victory_text.get_rect(center=(rect_width // 2, rect_height // 2))
    text_rect2 = victory_text2.get_rect(center=(rect_width // 2, (rect_height // 2) + 40))  # Use rect_height instead of rect_width
    
    screen.fill(COLOR_WHITE)
    screen.blit(victory_text, text_rect)
    screen.blit(victory_text2, text_rect2)
    completion_button.draw(screen)

# Funktio tarkistaa, voiko käyttäjä muokata hiiren alla olevaa solua.
def is_hoverable(hovered_cell: list, starting_board:list):
    return hovered_cell is not None and not starting_board[hovered_cell[0]][hovered_cell[1]]

def display_fps(screen: pygame.Surface, clock: pygame.time.Clock):
    fps_text = DEFAULT_FONT.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

def count_filled_cells(board):
    filled_count = 0
    for row in board:
        for cell in row:
            filled_count += -(-cell//9)
    return filled_count

# Funktio sammuttaa pelin
def exit_game():
    pygame.quit();
    sys.exit()

# Funktio avaa pelin
def run_game():
    #starting_board =          sudoku.create_solved_board()
    starting_board =        sudoku.create_starting_board(0.3 )
    active_board =          copy_board(starting_board)
    filled_cell_count =     count_filled_cells( active_board )
    total_cell_count =      9*9;
    hovered_cell =          None
    invalid_cells =         [];
    state =                 GameState(STATE_PAUSED)
    clock =                 pygame.time.Clock()
    
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
                        invalid_cells = sudoku.find_invalid_cells(active_board)
                        filled_cell_count = count_filled_cells( active_board )
            

            elif event.type == pygame.MOUSEWHEEL and state.get() is not STATE_PAUSED:
                if is_hoverable(hovered_cell, starting_board):
                    num = (active_board[hovered_cell[0]][hovered_cell[1]] + int(event.y)) % 10
                    active_board[hovered_cell[0]][hovered_cell[1]] = num
                    invalid_cells = sudoku.find_invalid_cells(active_board)
                    filled_cell_count = count_filled_cells( active_board )

            elif state.get(  ) is STATE_PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        row, column = get_mouse_pos()
                        if not starting_board[row][column]:
                            num = (active_board[row][column] + 1) % 10
                            active_board[row][column] = num
                            invalid_cells = sudoku.find_invalid_cells(active_board)
                            filled_cell_count = count_filled_cells( active_board )
                            
                if event.type == pygame.MOUSEMOTION:
                    hovered_cell = get_mouse_pos()
                

            elif state.get() is STATE_PAUSED:
                if play_button.is_pressed():
                    state.set(STATE_PLAYING)
                    filled_cell_count = count_filled_cells( active_board )
                   
                if restart_button.is_pressed():
                    starting_board = sudoku.create_starting_board( 0.3 )
                    active_board =   copy_board(starting_board)
                    invalid_cells = sudoku.find_invalid_cells(active_board)
                    filled_cell_count = count_filled_cells( active_board )

                    hovered_cell = None
                    invalid_cells =  []
                    state.set(STATE_PLAYING)
        
                if help_button.is_pressed():
                    state.set(STATE_HELP)
                if quit_button.is_pressed():
                    exit_game()

            elif state.get(  ) == STATE_COMPLETED:
                if completion_button.is_pressed():
                    play_button.set_text("Play")
                    starting_board =    sudoku.create_starting_board( 0.3 )
                    active_board =      copy_board(starting_board)
                    filled_cell_count = count_filled_cells( active_board )
                    hovered_cell =      None
                    invalid_cells =     []
                    state.set(STATE_PAUSED)
               
        if state.get() == STATE_PLAYING:
            draw_grid_background(screen, starting_board, hovered_cell)
            draw_grid(screen)
            draw_numbers(screen, active_board, starting_board, invalid_cells)
            if filled_cell_count == total_cell_count and sudoku.is_valid_sudoku(active_board):
                state.set( STATE_COMPLETED )

        if state.get() == STATE_COMPLETED:
                draw_completion_screen(screen)
           
        elif state.get() == STATE_PAUSED:
            draw_main_menu()
            
        elif state.get() == STATE_HELP:
            draw_help_menu()
        
        clock.tick(FRAMES_PER_SECOND)
        pygame.display.flip()
        

def main():
    run_game();

main()