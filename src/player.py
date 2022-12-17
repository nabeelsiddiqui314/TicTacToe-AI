from board import Cell
import pygame
import random
from board import Board
import copy

class PlayerManager:
    def __init__(self, player1, player2):
        player1.setSymbol(Cell.X)
        player2.setSymbol(Cell.O)

        self.players = [player1, player2]
        self.playerMap = {Cell.X: 0,
                          Cell.O: 1}

    def play(self, board):
        playerIndex = self.playerMap[board.turn]
        player = self.players[playerIndex]

        move = player.getMove(board)
        if move is not None:
            board.playNext(move)

class Player:
    def __init__(self):
        self.symbol = None

    def setSymbol(self, cell):
        self.symbol = cell

    def getMove(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self, boardDisplay):
        self.boardDisplay = boardDisplay

    def getMove(self, board):
        if pygame.mouse.get_pressed()[0]:
            return self.boardDisplay.getCellIndexFromPoint(pygame.mouse.get_pos())
        return None

class RandomMovePlayer(Player):
    def getMove(self, board):
        return random.randrange(9)

class MinimaxPlayer(Player):
    def getOppositePlayer(self):
        return Cell.X if self.symbol == Cell.O else Cell.O

    def getBestMove(self, board, depth = 0, maximize = True):
        if board.isGameOver():
            if board.isWinner(self.symbol):
                return 10 - depth
            elif board.isWinner(self.getOppositePlayer()):
                return depth - 10
            return 0

        currentDepth = depth + 1
        emptyCells = board.getEmptyCells()
        scores = {}

        for cell in emptyCells:
            boardCopy = copy.deepcopy(board)
            boardCopy.playNext(cell)
            score = self.getBestMove(boardCopy, currentDepth, not maximize)
            scores[cell] = score

        if depth == 0:
            if maximize:
                return max(scores, key = scores.get)
            return min(scores, key = scores.get)

        if maximize:
            return max(scores.values())
        return min(scores.values())

    def getMove(self, board):
        if board.getEmptyCellCount() == 9:
            return random.randrange(9)

        return self.getBestMove(board)
