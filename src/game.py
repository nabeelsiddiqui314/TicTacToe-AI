import enum
from src.board import Board, Cell

class Result(enum.Enum):
    WINNER_X = 0
    WINNER_O = 1
    DRAW = 2

class Game:
    def __init__(self, playerX, playerO):
        playerX.setSymbol(Cell.X)
        playerO.setSymbol(Cell.O)

        self.players = [playerX, playerO]
        self.playerMap = {Cell.X: 0,
                          Cell.O: 1}

        self.starter = Cell.X
        self.board = Board(self.starter)
        self.gameOver = False
        self.result = None

    def nextRound(self):
        self.starter = Board.getOppositePlayer(self.starter)
        self.board = Board(self.starter)
        self.result = None
        self.gameOver = False

    def play(self):
        if not self.gameOver:
            playerIndex = self.playerMap[self.board.turn]
            player = self.players[playerIndex]

            move = player.nextMove(self.board)
            if move is not None:
                self.board.playNext(move)
                if self.board.isGameOver():
                    self.gameOver = True
                    self.computeResult()

    def isOver(self):
        return self.gameOver

    def computeResult(self):
            if self.board.isWinner(Cell.X):
                self.result = Result.WINNER_X
            elif self.board.isWinner(Cell.O):
                self.result = Result.WINNER_O
            else:
                self.result = Result.DRAW
