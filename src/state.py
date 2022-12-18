import pygame

from src.board import Board, BoardDisplay, Cell
from src.player import Human, PlayerManager, MinimaxAI
from src.gui.text import Text

class StateManager:
    def __init__(self, state):
        self.state = None
        self.setState(state)

    def setState(self, state):
        state.stateManager = self
        self.state = state

    def processEvent(self, event):
        self.state.processEvent(event)

    def update(self):
        self.state.update()

    def render(self, screen):
        self.state.render(screen)

class State:
    def __init__(self):
        self.stateManager = None

    def processEvent(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass

class GameState(State):
    def __init__(self):
        self.board = Board()
        windowWidth, windowHeight = pygame.display.get_window_size()
        self.boardDisplay = BoardDisplay(self.board, (windowWidth / 2, windowHeight / 2), 120, 5)
        self.playerManager = PlayerManager(Human(self.boardDisplay), MinimaxAI())
        self.font = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.resultText = None

    def processEvent(self, event):
        pass

    def update(self):
        if not self.board.isGameOver():
            self.playerManager.play(self.board)
        elif self.resultText is None:
            self.resultText = Text(self.computeResult(), self.font, (385, 50), (48, 52, 63))

    def computeResult(self):
        if self.board.isWinner(Cell.X):
            return "X wins!"
        if self.board.isWinner(Cell.O):
            return "O wins!"

        return "Draw!"

    def render(self, screen):
        self.boardDisplay.render(screen)
        if self.resultText is not None:
            self.resultText.render(screen)