import enum
import pygame

class Cell(enum.Enum):
    EMPTY = 0
    X = 1
    O = 2

class Board:
    def __init__(self):
        self.cells = [Cell.EMPTY] * 9

    def getCell(self, index):
        return self.cells[index]

class BoardDisplay:
    def __init__(self, board, cellWidth):
        self.board = board
        self.cellWidth = cellWidth
        self.XImage = pygame.image.load("res/X.png")
        self.OImage = pygame.image.load("res/O.png")
        self.emptyImage = pygame.image.load("res/empty.png")
        self.cellRects = []

        self.scaleImages()
        self.initCellRects()

    def scaleImages(self):
        cellSize = (self.cellWidth, self.cellWidth)
        self.XImage = pygame.transform.smoothscale(self.XImage, cellSize)
        self.OImage = pygame.transform.smoothscale(self.OImage, cellSize)
        self.emptyImage = pygame.transform.smoothscale(self.emptyImage, cellSize)

    def initCellRects(self):
        for y in range(3):
            for x in range(3):
                position = (x * self.cellWidth, y * self.cellWidth)
                size = (self.cellWidth, self.cellWidth)
                cellRect = pygame.rect.Rect(position, size)
                self.cellRects.append(cellRect)

    def render(self, screen):
        for cell, cellRect in zip(self.board.cells, self.cellRects):
            image = self.getImageForCell(cell)
            screen.blit(image, cellRect.topleft)

    def getImageForCell(self, cell):
        if cell == Cell.X:
            image = self.XImage
        elif cell == Cell.O:
            image = self.OImage
        else:
            image = self.emptyImage

        return image

    def getCellIndexFromPoint(self, point):
        for index, cellRect in enumerate(self.cellRects):
            if cellRect.collidepoint(point):
                return index

        return None
