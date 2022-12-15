import pygame
from Board import Board, BoardDisplay, Cell

board = Board()
boardDisplay = BoardDisplay(board, 120)

def main():
    pygame.init()

    background_colour = (0, 0, 0)
    (width, height) = (800, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tic Tac Toe")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cellIndex = boardDisplay.getCellIndexFromPoint(event.pos)
                if cellIndex is not None:
                    board.cells[cellIndex] = Cell.X

        screen.fill(background_colour)
        boardDisplay.render(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()