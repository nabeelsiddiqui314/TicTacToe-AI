import enum

from src.board import Board, Cell
from src.player import PlayerManager

class Result(enum.Enum):
    WINNER_X = 0
    WINNER_O = 1
    DRAW = 2

class Game:
    def __init__(self, playerX, playerO):
        self.playerManager = PlayerManager(playerX, playerO)
        self.starter = Cell.X
        self.board = Board(self.starter)

    def nextRound(self):
        self.starter = Board.getOppositePlayer(self.starter)
        self.board = Board(self.starter)

    def play(self):
        if not self.board.isGameOver():
            self.playerManager.play(self.board)
            return True
        return False

    def computeResult(self):
        if self.board.isWinner(Cell.X):
            return Result.WINNER_X
        if self.board.isWinner(Cell.O):
            return Result.WINNER_O

        return Result.DRAW

