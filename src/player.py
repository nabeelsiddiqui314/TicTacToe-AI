from board import Cell
import pygame
import random

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
