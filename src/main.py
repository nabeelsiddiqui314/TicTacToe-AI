import pygame
from Board import Board, BoardDisplay, Cell

board = Board()
boardDisplay = BoardDisplay(board, 120)

def main():
    pygame.init()

    background_colour = (0, 0, 0)
    (width, height) = (800, 600)

    board.cells[0] = Cell.X
    board.cells[4] = Cell.O
    board.cells[8] = Cell.X

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tic Tac Toe")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_colour)
        boardDisplay.render(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()