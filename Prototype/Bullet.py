__author__ = 'Justin'

from colors import *

spriteHeight = 64
spriteWidth = 64

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color=white, width=spriteWidth, height=spriteHeight):
        super(Bullet, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()


    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

    def update_image(self, filename = None):
        if (filename != None):
            self.image = pygame.image.load(filename)

    def checkCollision(self, object1, object2, spriteWidth=spriteWidth, spriteHeight=spriteHeight):
        if (object1.getX() >= object2.getX() and object1.getX() <= (object2.getX() + spriteWidth)) and \
                (object1.getY() >= object2.getY() and object1.getY() <= (object2.getY() + spriteHeight)):
            return True
        return False

    def update(self, type):
        if type == "player":
            self.rect.y -= 10
        elif type == "enemy":
            self.rect.y += 10

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def destroy(self):
        self.rect.x = -1000
        self.rect.y = -1000
        self.kill()
