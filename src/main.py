import pygame

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

        screen.fill(background_colour)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()