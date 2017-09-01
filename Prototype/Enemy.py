__author__ = 'Justin'

from colors import *

spriteHeight = 64
spriteWidth = 64


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Enemy, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.health = 1
        self.index = 0
        self.spriteCounter = 0

        self.explosion = pygame.mixer.Sound("sounds/explosion.wav")

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def set_rect(self, width, height):
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect

    def update_image(self, filename=None):
        if (filename != None):
            self.image = pygame.image.load(filename)

    def checkCollision(self, object1, object2, spriteWidth=spriteWidth, spriteHeight=spriteHeight):
        if (object1.getX() >= object2.getX() and object1.getX() <= (object2.getX() + spriteWidth)) and \
                (object1.getY() >= object2.getY() and object1.getY() <= (object2.getY() + spriteHeight)):
            return True
        return False

    def setSpriteCounter(self, value):
        self.spriteCounter = value

    def getSpriteCounter(self):
        return self.spriteCounter

    def set_Health(self, value):
        self.health = value

    def get_Health(self):
        return self.health

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def decrement_Health(self):
        self.explosion.play()
        self.health -= 2

    def enemyDead(self):
        if self.health < 0:
            return True
        return False

    def destroy(self):
        #move rect out of window
        self.rect.x = -500
        self.rect.y = -500
        self.kill()