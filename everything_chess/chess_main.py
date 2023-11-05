# Main driver file which will be responsible with for user input and displaying the current Game State object
import pygame
import pygame.image
from everything_chess import chess_engine

WIDTH = 512  # Another option is 400
HEIGHT = 512
DIMENSION = 8  # Dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animations
IMAGES = {}


# Initialize a global dictionary of images. This will be called exactly once in the main.
def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB", "bK", "bQ"]
    # We can access an image by saying: "IMAGES['wP']"
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("chess_pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# Main driver for user input and updating the graphics
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = chess_engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False     # Flag variable for when a move is made
    load_images()         # Only do this once, before the while loop
    running = True
    square_selected = ()  # No square is selected initially; keeps track of the last click of the user (tuple: (# row, col))
    player_clicks = []    # Keep track of player clicks (two tuples: [(6, 4), (4, 4)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mouse handler
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # (x, y) location of mouse
                location = pygame.mouse.get_pos()
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                # First click is to select and second click is to deselect
                # Clicked the same square twice (undo)
                if square_selected == (row, column):
                    square_selected = ()  # Deselect
                    player_clicks = []    # Clear player clicks
                else:
                    square_selected = (row, column)
                    player_clicks.append(square_selected)    # Append for both 1st and 2nd clicks
                # Was that the user's second click
                # If it's after the 2nd click
                if len(player_clicks) == 2:
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notation())
                    if move in valid_moves:
                        game_state.make_move(move)
                        move_made = True
                    square_selected = ()  # Reset user clicks
                    player_clicks = []    # Have to reset player_clicks to empty
            # Key handlers
            elif event.type == pygame.KEYDOWN:
                # Undo when 'z' is pressed
                if event.key == pygame.K_z:
                    game_state.undo_move()
                    move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        pygame.display.flip()


# Responsible for all the graphics within a current game state
def draw_game_state(screen, game_state):
    # Draw squares on the board
    draw_board(screen)
    # Add in piece highlighting
    # Draw pieces on top of those squares
    draw_pieces(screen, game_state.board)


# Draw the squares on the board
def draw_board(screen):
    # Top left square is light
    # Light squares = even
    # Dark squares = odd
    colors = [pygame.Color("white"), pygame.Color("burlywood3")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Draw the pieces on the board using the current GameState.board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            # Not empty square
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
