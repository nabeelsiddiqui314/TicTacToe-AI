import pygame


class Text:
    def __init__(self, text, font, center, color):
        self.text = text
        self.font = font
        self.color = color
        self.textSurface = self.font.render(text, True, color)

        centerX, centerY = center
        sizeX, sizeY = self.getSize()
        self.drawPosition = (centerX - sizeX / 2, centerY - sizeY / 2)

    def getSize(self):
        return self.textSurface.get_size()

    def render(self, screen):
        screen.blit(self.textSurface, self.drawPosition)
