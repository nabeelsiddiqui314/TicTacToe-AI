import pygame

from src.board import BoardDisplay, Cell
from src.player import PlayerFactory
from src.game import Game, Result
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

        playerNumber = len(self.subheaders)
        playerSymbol = "X" if playerNumber == 0 else "O"
        headerY = windowHeight / 4
        header = Text("Player {0}".format(playerSymbol), self.regularFont, (column, headerY), constants.TITLE_TEXT_COLOR)
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

        player1Button = self.playerSelectors[0].getSelectedButton()
        player2Button = self.playerSelectors[1].getSelectedButton()

        if self.playButton.isClicked():
            if player1Button is not None and player2Button is not None:
                self.stateManager.setState(GameState(player1Button.label, player2Button.label))

    def render(self, screen):
        self.title.render(screen)

        for header in self.subheaders:
            header.render(screen)

        for playerSelector in self.playerSelectors:
            playerSelector.render(screen)

        self.playButton.render(screen)


class GameState(State):
    def __init__(self, playerXName, playerOName):
        windowWidth, windowHeight = pygame.display.get_window_size()
        self.boardDisplay = BoardDisplay((windowWidth / 2, windowHeight / 2), constants.BOARD_CELL_WIDTH,
                                         constants.BOARD_SPACING)

        self.playerXName = playerXName
        self.playerOName = playerOName

        playerFactory = PlayerFactory(self.boardDisplay)
        playerX = playerFactory.getPlayer(playerXName)
        playerO = playerFactory.getPlayer(playerOName)

        self.game = Game(playerX, playerO)

        self.font = pygame.font.Font(pygame.font.get_default_font(), constants.REGULAR_FONT_SIZE)
        self.resultText = None
        self.resetButton = None
        self.backButton = None
        self.XScoreText = None
        self.OScoreText = None
        self.initButtons()
        self.updateScoreText()

    def initButtons(self):
        windowWidth, windowHeight = pygame.display.get_window_size()

        resetTexture = pygame.image.load(constants.RES_DIR + "reset.png")
        resetTexture = pygame.transform.smoothscale(resetTexture, (70, 70))

        resetTextureWidth, resetTextureHeight = resetTexture.get_rect().size
        self.resetButton = TexturedButton(resetTexture, (windowWidth * (3 / 4) - resetTextureWidth / 2,
                                                         windowHeight - resetTextureHeight - 5))

        backTexture = pygame.image.load(constants.RES_DIR + "back.png")
        backTexture = pygame.transform.smoothscale(backTexture, (90, 70))

        backTextureWidth, backTextureHeight = backTexture.get_rect().size
        self.backButton = TexturedButton(backTexture, (windowWidth / 4 - backTextureWidth / 2,
                                                        windowHeight - backTextureHeight - 5))

    def updateScoreText(self):
        textStyle = {
            "color": constants.SCORE_TEXT_COLOR,
            "font": self.font
        }

        windowWidth, windowHeight = pygame.display.get_window_size()

        XScore = self.game.getScore(Cell.X)
        OScore = self.game.getScore(Cell.O)

        self.XScoreText = Text(f"Player X : {XScore}", center=(windowWidth / 8, windowHeight / 8), **textStyle)
        self.OScoreText = Text(f"Player O : {OScore}", center=(windowWidth * (7 / 8), windowHeight / 8), **textStyle)

    def processEvent(self, event):
        pass

    def update(self):
        self.game.play()

        if self.game.isOver() and self.resultText is None:
            windowWidth = pygame.display.get_window_size()[0]
            boardTop = self.boardDisplay.getBoundingRect().top
            self.resultText = Text(self.getResultText(), self.font, (windowWidth / 2, boardTop / 2),
                                   constants.TEXT_COLOR)
            self.updateScoreText()

        if self.game.isOver() and self.resetButton.isClicked():
            self.game.nextRound()
            self.resultText = None

        if self.backButton.isClicked():
            self.stateManager.setState(MenuState())

    def render(self, screen):
        self.boardDisplay.render(screen, self.game.board)

        if self.game.isOver():
            self.resetButton.render(screen)
        self.backButton.render(screen)

        if self.resultText is not None:
            self.resultText.render(screen)

        self.XScoreText.render(screen)
        self.OScoreText.render(screen)

    def getResultText(self):
        result = self.game.result
        if result == Result.WINNER_X:
            return "X wins!"
        if result == Result.WINNER_O:
            return "O wins!"
        return "Draw!"
