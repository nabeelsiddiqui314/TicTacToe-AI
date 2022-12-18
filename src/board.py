import enum
import pygame
from os.path import dirname, abspath
from src.gui.button import TexturedButton

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
            self.swapTurn()

    def swapTurn(self):
        self.turn = Cell.X if self.turn == Cell.O else Cell.O

class BoardDisplay:
    def __init__(self, board, origin, cellWidth, spacing):
        self.board = board
        self.origin = origin
        self.cellWidth = cellWidth
        self.spacing = spacing

        resDirectory = abspath(dirname(dirname(__file__))) + "/res/"
        self.XImage = pygame.image.load(resDirectory + "X.png")
        self.OImage = pygame.image.load(resDirectory + "O.png")
        self.emptyImage = pygame.image.load(resDirectory + "empty.png")

        self.buttons = []

        self.scaleImages()
        self.arrangeButtons()

    def scaleImages(self):
        cellSize = (self.cellWidth, self.cellWidth)
        self.XImage = pygame.transform.smoothscale(self.XImage, cellSize)
        self.OImage = pygame.transform.smoothscale(self.OImage, cellSize)
        self.emptyImage = pygame.transform.smoothscale(self.emptyImage, cellSize)

    def arrangeButtons(self):
        totalWidth = self.cellWidth + self.spacing
        originX, originY = self.origin

        for y in range(3):
            for x in range(3):
                position = (x * totalWidth + originX, y * totalWidth + originY)
                button = TexturedButton(self.emptyImage, position)
                self.buttons.append(button)

    def render(self, screen):
        for cell, button in zip(self.board.cells, self.buttons):
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
