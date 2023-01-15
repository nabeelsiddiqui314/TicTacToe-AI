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
        self.scores = [0, 0]

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
            playerIndex = self.board.turn.value
            player = self.players[playerIndex]

            move = player.nextMove(self.board)
            if move is not None:
                self.board.playNext(move)
                if self.board.isGameOver():
                    self.gameOver = True
                    self.computeResult()

    def getScore(self, player):
        return self.scores[player.value]

    def isOver(self):
        return self.gameOver

    def computeResult(self):
            if self.board.isWinner(Cell.X):
                self.result = Result.WINNER_X
                playerIndex = Cell.X.value
                self.scores[playerIndex] += 1
            elif self.board.isWinner(Cell.O):
                self.result = Result.WINNER_O
                playerIndex = Cell.O.value
                self.scores[playerIndex] += 1
            else:
                self.result = Result.DRAW
