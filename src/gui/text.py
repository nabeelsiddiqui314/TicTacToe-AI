import pygame


class Text:
    def __init__(self, text, font, position, color):
        self.text = text
        self.font = font
        self.color = color
        self.textSurface = self.font.render(text, True, color)

        positionX, positionY = position
        sizeX, sizeY = self.textSurface.get_size()
        self.drawPosition = (positionX - sizeX / 2, positionY - sizeY / 2)

    def render(self, screen):
        screen.blit(self.textSurface, self.drawPosition)
