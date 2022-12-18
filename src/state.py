import pygame

from src.board import Board, BoardDisplay, Cell
from src.player import Human, PlayerManager, MinimaxAI
from src.gui.text import Text
from src.gui.button import TexturedButton
from src import constants

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

class MenuState(State):
    def __init__(self):
        pass

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
        self.boardDisplay = BoardDisplay(self.board, (windowWidth / 2, windowHeight / 2), constants.BOARD_CELL_WIDTH,
                                         constants.BOARD_SPACING)
        self.playerManager = PlayerManager(Human(self.boardDisplay), MinimaxAI())
        self.font = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.resultText = None
        self.resetButton = None
        self.backButton = None
        self.initButtons()

    def initButtons(self):
        windowWidth, windowHeight = pygame.display.get_window_size()

        resetTexture = pygame.image.load(constants.RES_DIR + "reset.png")
        resetTexture = pygame.transform.smoothscale(resetTexture, (70, 70))

        resetTextureWidth, resetTextureHeight = resetTexture.get_rect().size
        self.resetButton = TexturedButton(resetTexture, (windowWidth / 1.5 - resetTextureWidth / 2,
                                                         windowHeight - resetTextureHeight - 5))

        backTexture = pygame.image.load(constants.RES_DIR + "back.png")
        backTexture = pygame.transform.smoothscale(backTexture, (90, 70))

        backTextureWidth, backTextureHeight = backTexture.get_rect().size
        self.backButton = TexturedButton(backTexture, (windowWidth / 4 - backTextureWidth / 2,
                                                        windowHeight - backTextureHeight - 5))

    def processEvent(self, event):
        pass

    def update(self):
        if not self.board.isGameOver():
            self.playerManager.play(self.board)
        elif self.resultText is None:
            windowWidth = pygame.display.get_window_size()[0]
            boardTop = self.boardDisplay.getBoundingRect().top
            self.resultText = Text(self.computeResult(), self.font, (windowWidth / 2, boardTop / 2),
                                   constants.TEXT_COLOR)

        if self.resetButton.isClicked():
            self.stateManager.setState(GameState())

        if self.backButton.isClicked():
            self.stateManager.setState(MenuState())

    def computeResult(self):
        if self.board.isWinner(Cell.X):
            return "X wins!"
        if self.board.isWinner(Cell.O):
            return "O wins!"

        return "Draw!"

    def render(self, screen):
        self.boardDisplay.render(screen)
        self.resetButton.render(screen)
        self.backButton.render(screen)

        if self.resultText is not None:
            self.resultText.render(screen)
