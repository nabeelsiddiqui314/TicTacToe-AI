import pygame
from src.state import StateManager, GameState
from src.gui.button import Button

def main():
    pygame.init()

    background_colour = (228, 217, 255)
    (width, height) = (800, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tic Tac Toe")

    stateManager = StateManager(GameState())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            stateManager.processEvent(event)

        stateManager.update()
        Button.update()

        screen.fill(background_colour)
        stateManager.render(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()