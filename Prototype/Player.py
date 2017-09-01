__author__ = 'Justin'

from colors import *

spriteHeight = 64
spriteWidth = 64

class Player(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Player, self).__init__()

        self.explosion = pygame.mixer.Sound("sounds/explosion.wav")
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.health = 1

    def setHealth(self, value):
        self.health = value
        self.explosion.play()
        if self.health <= 0:
            self.kill()

    def destroy(self):
        self.kill()

    def getHealth(self):
        return self.health

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def update_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)


    def update(self, loopCount):
        if loopCount % 9 == 0:
            self.image = pygame.image.load("img/hero1Thrust.png")
        else:
            self.image = pygame.image.load("img/hero1Thrust2.png")

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y