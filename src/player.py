from src.board import Board
from src.board import Cell
import random
import math

class PlayerManager:
    def __init__(self, playerX, playerO):
        playerX.setSymbol(Cell.X)
        playerO.setSymbol(Cell.O)

        self.players = [playerX, playerO]
        self.playerMap = {Cell.X: 0,
                          Cell.O: 1}

    def play(self, board):
        playerIndex = self.playerMap[board.turn]
        player = self.players[playerIndex]

        move = player.nextMove(board)
        if move is not None:
            board.playNext(move)

class Player:
    def __init__(self):
        self.symbol = None

    def setSymbol(self, cell):
        self.symbol = cell

    def nextMove(self, board):
        pass

class PlayerFactory:
    def __init__(self, boardDisplay):
        self.playerMap = {
            "Human": lambda:  Human(boardDisplay),
            "Random AI": RandomMoveMaker,
            "Perfect AI": MinimaxAI
        }

    def getPlayerNames(self):
        return self.playerMap.keys()

    def getPlayer(self, name):
        return self.playerMap[name]()

class Human(Player):
    def __init__(self, boardDisplay):
        self.boardDisplay = boardDisplay

    def nextMove(self, board):
        return self.boardDisplay.getClickedCell()

class RandomMoveMaker(Player):
    def nextMove(self, board):
        return random.randrange(9)

class MinimaxAI(Player):
    def getBestMove(self, board, depth = 0, maximize = True, alpha = -math.inf, beta = math.inf):
        if board.isGameOver():
            if board.isWinner(self.symbol):
                return 10 - depth
            elif board.isWinner(Board.getOppositePlayer(self.symbol)):
                return depth - 10
            return 0

        currentDepth = depth + 1
        emptyCells = board.getEmptyCells()
        scores = {}

        for cell in emptyCells:
            board.playNext(cell)
            score = self.getBestMove(board, currentDepth, not maximize, alpha, beta)
            scores[cell] = score

            # undo move
            board.setCell(cell, Cell.EMPTY)
            board.swapTurn()

            if maximize:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)

            # prune
            if alpha >= beta:
                break

        if depth == 0:
            if maximize:
                return max(scores, key = scores.get)
            return min(scores, key = scores.get)

        if maximize:
            return max(scores.values())
        return min(scores.values())

    def nextMove(self, board):
        if board.getEmptyCellCount() == 9:
            return random.randrange(9)

        return self.getBestMove(board)
