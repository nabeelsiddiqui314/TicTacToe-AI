import enum
import pygame

class Cell(enum.Enum):
    EMPTY = 0
    X = 1
    O = 2

class Board:
    def __init__(self):
        self.cells = [Cell.EMPTY] * 9
        self.lines = []
        self.turn = Cell.X

        self.initLines()

    def initLines(self):
        rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        columns = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
        diagonals = [[0, 4, 8], [2, 4, 6]]

        self.lines.extend(rows)
        self.lines.extend(columns)
        self.lines.extend(diagonals)

    def setCell(self, index, cell):
        self.cells[index] = cell

    def getCell(self, index):
        return self.cells[index]

    def checkLine(self, line, cell):
        return all(self.cells[index] == cell for index in line)

    def isWinner(self, player):
        return any(self.checkLine(line, player) for line in self.lines)

    def getEmptyCells(self):
        return [index for index, cell in enumerate(self.cells) if cell == Cell.EMPTY]

    def getEmptyCellCount(self):
        return self.cells.count(Cell.EMPTY)

    def isGameOver(self):
        return self.isWinner(Cell.X) or self.isWinner(Cell.O) or self.getEmptyCellCount() == 0

    def playNext(self, index):
        if self.cells[index] == Cell.EMPTY:
            self.cells[index] = self.turn
            self.turn = Cell.X if self.turn == Cell.O else Cell.O

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
