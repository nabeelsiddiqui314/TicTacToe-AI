import pygame
from src.gui.text import Text

class Button:
    clicked = False
    clickedLastFrame = False

    def __init__(self, position = None):
        self.position = position
        self.size = None
        self.clicked = False
        self.clickedLastFrame = False
        self.highlighted = False

    def setPosition(self, position):
        self.position = position

    def isClicked(self):
        boundingRect = pygame.rect.Rect(self.position, self.size)
        mousePosition = pygame.mouse.get_pos()
        isMouseInButton = boundingRect.collidepoint(mousePosition)
        self.highlighted = isMouseInButton

        if isMouseInButton:
            return Button.clicked and not Button.clickedLastFrame
        return False

    @staticmethod
    def update():
        Button.clickedLastFrame = Button.clicked
        Button.clicked = pygame.mouse.get_pressed()[0]

    def render(self, screen):
        pass

class TexturedButton(Button):
    def __init__(self, regularTexture, position, highlightTexture = None):
        super().__init__(position)
        self.regularTexture = None
        self.highlightTexture = None
        self.size = None

        self.setTexture(regularTexture, highlightTexture)

    def setTexture(self, regularTexture, highlightTexture = None):
        self.regularTexture = regularTexture
        self.highlightTexture = highlightTexture
        self.size = self.regularTexture.get_size()

    def render(self, screen):
        if self.highlighted and self.highlightTexture is not None:
            texture = self.highlightTexture
        else:
            texture = self.regularTexture

        screen.blit(texture, self.position)

class TextButton(Button):
    def __init__(self, label, font, center, textColor, buttonColor, padding, highlightColor = None):
        super().__init__()

        self.label = label
        self.text = Text(label, font, center, textColor)
        self.buttonColor = buttonColor
        self.highlightColor = highlightColor
        centerX, centerY = center
        textWidth, textHeight = self.text.getSize()
        self.position = (centerX - textWidth / 2 - padding, centerY - textHeight / 2 - padding)
        self.size = (textWidth + padding * 2, textHeight + padding * 2)

    def render(self, screen):
        if self.highlighted and self.highlightColor is not None:
            color = self.highlightColor
        else:
            color = self.buttonColor

        pygame.draw.rect(screen, color, (self.position, self.size))
        self.text.render(screen)

class RadioButtonGroup:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selectedButton = None

    def update(self):
        for button in self.buttons:
            if button.isClicked():
                self.selectedButton = button
                break
        if self.getSelectedButton() is not None:
            self.selectedButton.highlighted = True

    def getSelectedButton(self):
        return self.selectedButton

    def render(self, screen):
        for button in self.buttons:
            button.render(screen)
