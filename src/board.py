import enum
import pygame
from src.gui.button import TexturedButton
from src import constants

class Cell(enum.Enum):
    EMPTY = 0
    X = 1
    O = 2

class Board:
    def __init__(self, starter):
        self.cells = [Cell.EMPTY] * 9
        self.lines = []
        self.turn = starter

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
            self.swapTurn()

    def swapTurn(self):
        self.turn = Board.getOppositePlayer(self.turn)

    @staticmethod
    def getOppositePlayer(player):
        return Cell.X if player == Cell.O else Cell.O

class BoardDisplay:
    def __init__(self, center, cellWidth, spacing):
        self.cellWidth = cellWidth
        self.totalCellWidth = cellWidth + spacing

        totalWidth = self.totalCellWidth * 3
        centerX, centerY = center
        self.origin = (centerX - totalWidth / 2, centerY - totalWidth / 2)

        self.XImage = pygame.image.load(constants.RES_DIR + "X.png")
        self.OImage = pygame.image.load(constants.RES_DIR + "O.png")
        self.emptyImage = pygame.image.load(constants.RES_DIR + "empty.png")

        self.buttons = []

        self.scaleImages()
        self.arrangeButtons()

    def scaleImages(self):
        cellSize = (self.cellWidth, self.cellWidth)
        self.XImage = pygame.transform.smoothscale(self.XImage, cellSize)
        self.OImage = pygame.transform.smoothscale(self.OImage, cellSize)
        self.emptyImage = pygame.transform.smoothscale(self.emptyImage, cellSize)

    def arrangeButtons(self):
        originX, originY = self.origin

        for y in range(3):
            for x in range(3):
                position = (x * self.totalCellWidth + originX, y * self.totalCellWidth + originY)
                button = TexturedButton(self.emptyImage, position)
                self.buttons.append(button)

    def render(self, screen, board):
        for cell, button in zip(board.cells, self.buttons):
            image = self.getImageForCell(cell)
            button.setTexture(image)
            button.render(screen)

    def getImageForCell(self, cell):
        if cell == Cell.X:
            image = self.XImage
        elif cell == Cell.O:
            image = self.OImage
        else:
            image = self.emptyImage

        return image

    def getClickedCell(self):
        for index, button in enumerate(self.buttons):
            if button.isClicked():
                return index

        return None

    def getBoundingRect(self):
        size = (self.totalCellWidth * 3, self.totalCellWidth * 3)
        return pygame.rect.Rect(self.origin, size)
