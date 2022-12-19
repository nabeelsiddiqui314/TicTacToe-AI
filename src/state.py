import pygame

from src.board import Board, BoardDisplay, Cell
from src.player import PlayerManager, Human, MinimaxAI, RandomMoveMaker
from src.gui.text import Text
from src.gui.button import TexturedButton, TextButton, RadioButtonGroup
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
        self.titleFont = pygame.font.Font(pygame.font.get_default_font(), constants.TITLE_FONT_SIZE)
        self.regularFont = pygame.font.Font(pygame.font.get_default_font(), constants.REGULAR_FONT_SIZE)
        windowWidth, windowHeight = pygame.display.get_window_size()

        self.title = Text("Tic Tac Toe", self.titleFont, (windowWidth / 2, windowHeight / 8), constants.TITLE_TEXT_COLOR)
        self.subheaders = []
        self.playerSelectors = []

        self.buttonStyle = {
            "font": self.regularFont,
            "textColor": constants.BUTTON_TEXT_COLOR,
            "buttonColor": constants.BUTTON_COLOR,
            "padding": 5,
            "highlightColor": constants.BUTTON_HIGHLIGHT_COLOR
        }

        self.createPlayerSelector(windowWidth / 4)
        self.createPlayerSelector(windowWidth / 1.33)
        self.playButton = TextButton("Play", center=(windowWidth / 2, windowHeight / 1.2), **self.buttonStyle)

    def createPlayerSelector(self, column):
        windowWidth, windowHeight = pygame.display.get_window_size()

        playerNumber = len(self.subheaders) + 1
        headerY = windowHeight / 4
        header = Text("Player {0}".format(playerNumber), self.regularFont, (column, headerY), constants.TITLE_TEXT_COLOR)
        self.subheaders.append(header)

        labels = ["Human", "Random AI", "Perfect AI"]
        buttons = []

        for index, label in enumerate(labels):
            button = TextButton(label, center=(column, headerY + 70 * (index + 1)), **self.buttonStyle)
            buttons.append(button)

        playerSelector = RadioButtonGroup(buttons)
        self.playerSelectors.append(playerSelector)

    def processEvent(self, event):
        pass

    def update(self):
        for playerSelector in self.playerSelectors:
            playerSelector.update()

    def render(self, screen):
        self.title.render(screen)

        for header in self.subheaders:
            header.render(screen)

        for playerSelector in self.playerSelectors:
            playerSelector.render(screen)

        self.playButton.render(screen)


class GameState(State):
    def __init__(self):
        self.board = Board()
        windowWidth, windowHeight = pygame.display.get_window_size()
        self.boardDisplay = BoardDisplay(self.board, (windowWidth / 2, windowHeight / 2), constants.BOARD_CELL_WIDTH,
                                         constants.BOARD_SPACING)
        self.playerManager = PlayerManager(Human(self.boardDisplay), MinimaxAI())
        self.font = pygame.font.Font(pygame.font.get_default_font(), constants.REGULAR_FONT_SIZE)
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
