import enum
import pygame

class Cell(enum.Enum):
    EMPTY = 0
    X = 1
    O = 2

class Board:
    def __init__(self):
        self.cells = [Cell.EMPTY] * 9

    @staticmethod
    def getIndex(x, y):
        return x + y * 3

    def getCell(self, x, y):
        return self.cells[self.getIndex(x, y)]

class BoardDisplay:
    def __init__(self, board, cellWidth):
        self.board = board
        self.XImage = pygame.image.load("res/X.png")
        self.OImage = pygame.image.load("res/O.png")
        self.emptyImage = pygame.image.load("res/empty.png")
        self.cellWidth = cellWidth

        cellSize = (cellWidth, cellWidth)
        self.XImage = pygame.transform.smoothscale(self.XImage, cellSize)
        self.OImage = pygame.transform.smoothscale(self.OImage, cellSize)
        self.emptyImage = pygame.transform.smoothscale(self.emptyImage, cellSize)

    def render(self, screen):
        for y in range(3):
            for x in range(3):
                cell = self.board.getCell(x, y)
                image = self.getImageForCell(cell)
                screen.blit(image, (x * self.cellWidth, y * self.cellWidth))

    def getImageForCell(self, cell):
        if cell == Cell.X:
            image = self.XImage
        elif cell == Cell.O:
            image = self.OImage
        else:
            image = self.emptyImage

        return image
