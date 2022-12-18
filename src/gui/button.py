import pygame

class Button:
    clicked = False
    clickedLastFrame = False

    def __init__(self, position = None):
        self.position = position
        self.size = None
        self.clicked = False
        self.clickedLastFrame = False

    def setPosition(self, position):
        self.position = position

    def isClicked(self):
        boundingRect = pygame.rect.Rect(self.position, self.size)
        mousePosition = pygame.mouse.get_pos()

        if boundingRect.collidepoint(mousePosition):
            return Button.clicked and not Button.clickedLastFrame
        return False

    @staticmethod
    def update():
        Button.clickedLastFrame = Button.clicked
        Button.clicked = pygame.mouse.get_pressed()[0]

    def render(self, screen):
        pass

class TexturedButton(Button):
    def __init__(self, texture, position = None):
        super().__init__(position)
        self.texture = None
        self.size = None

        self.setTexture(texture)

    def setTexture(self, texture):
        self.texture = texture
        self.size = self.texture.get_size()

    def render(self, screen):
        screen.blit(self.texture, self.position)