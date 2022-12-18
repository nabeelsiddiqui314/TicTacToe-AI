import pygame

class Button:
    def __init__(self, position = None):
        self.position = position
        self.size = None
        self.clicked = False
        self.clickedLastFrame = False

    def setPosition(self, position):
        self.position = position

    def setSize(self, size):
        self.size = size

    def isClicked(self):
        return self.clicked and not self.clickedLastFrame

    def update(self):
        self.clickedLastFrame = self.clicked

        boundingRect = pygame.rect.Rect(self.position, self.size)
        mousePosition = pygame.mouse.get_pos()
        isLeftPressed = pygame.mouse.get_pressed()[0]

        self.clicked = boundingRect.collidepoint(mousePosition) and isLeftPressed

    def render(self, screen):
        pass

class TexturedButton(Button):
    def __init__(self, texturePath, position = None):
        super().__init__(position)
        self.texture = pygame.image.load(texturePath)
        self.size = self.texture.get_size()

    def setSize(self, size):
        super().setSize(size)
        self.texture = pygame.transform.smoothscale(self.texture)

    def render(self, screen):
        screen.blit(self.texture, self.position)