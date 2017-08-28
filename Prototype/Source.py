#I guess pygame doesn't need to be imported?
import pygame
import sys
import time
from colors import *

class Player(pygame.sprite.Sprite):
    def __init__(self, color = white, width = 64, height = 64):
        super(Player, self).__init__()

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

    def update(self, loopCount):
        if loopCount % 9 == 0:
            self.image = pygame.image.load("hero1Thrust.png")
        else:
            self.image = pygame.image.load("hero1Thrust2.png")

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color = white, width = 64, height = 64):
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

    def checkCollision(self, object1):
        if pygame.sprite.collide_rect(self, object1):
            return True
        return False

    def update(self):
        self.rect.y -= 10

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def destroy(self):
        self.rect.x = -1000
        self.rect.y = -1000
        self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color = white, width = 64, height = 64):
        super(Enemy, self).__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.health = 1
        self.index = 0
        self.spriteCounter = 0

        self.explosion = pygame.mixer.Sound("explosion.wav")

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

    def setSpriteCounter(self, value):
        self.spriteCounter = value

    def getSpriteCounter(self):
        return self.spriteCounter

    def get_Health(self):
        return self.health

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

class Background(pygame.sprite.Sprite):
    def __init__(self, color = white, width = 64, height = 64):
        super(Background, self).__init__()

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

    def get_image(self):
        return self.image

    def get_size(self):
        return self.image.get_size()

    def get_rect(self):
        return self.image.get_rect()

#main
if (__name__ == "__main__"):

    pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=4096)
    pygame.init()

    #Initial setup stuff =============================
    windowSize = windowWidth, windowHeight = 540, 702
    window = pygame.display.set_mode(windowSize, 0, 32)
    pygame.display.set_caption("asdf")
    clock = pygame.time.Clock()
    fps = 60
    clock.tick(fps)


    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.play()

    # ================================================

    #pygame.sprite.Group() is a group that will hold our objects(blocks)
    # idk why I need two groups, for some reason they wont all show up on the screen if they're in 1 group
    block_group = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    # ==================================================================
    # declare our objects, so far we only have 4.
    # the player's missile could be 5th, enemy missiles 6th (assuming they're the same image), + whatever else
    player = Player()
    #missile = Player()
    #enemy1 = Enemy()
    #enemy2 = Enemy()
    #enemy3 = Enemy()
    background = Background()
    background2 = Background()

    width, height = background.get_image().get_size()
    height += 200
    background_rect = background.get_rect()
    x = 0
    #y = 0

    x1 = 0
    y1 = -height

    # set images using our set_image(fileName) function
    background.set_image("starfield2.png")
    background2.set_image("starfield2.png")
    player.set_image("hero1Thrust.png")
    #missile.set_image("playerMissile.png")
    playerImageList = ["hero1Thrust.png", "hero1Thrust2.png"]

    #enemy1.set_image("lightenemy1.png")
    #enemy2.set_image("lightenemy3.png")
    #enemy3.set_image("lightenemy3.png")

    deathAnimation = []
    deathAnimation.append("lightenemy3Death1.png")
    deathAnimation.append("lightenemy3Death2.png")
    deathAnimation.append("lightenemy3Death3.png")
    deathAnimation.append("lightenemy3Death4.png")
    deathAnimation.append("lightenemy3Death5.png")
    deathAnimation.append("lightenemy3Death6.png")
    deathAnimation.append("lightenemy3Death7.png")
    deathAnimation.append("enemyDeath.png")

    # add our objects to the groups we declared in lines 40,41.
    # again, idk why i needed two groups
    block_group.add(player)
    #objectGroup.add(missile)
    #block_group.add(enemy1)
    #block_group.add(enemy2)
    #block_group.add(enemy3)
    backgroundGroup.add(background) #2nd group
    backgroundGroup.add(background2)

    #Draw the group containing the background first.
   # backgroundGroup.draw(window)

    # Set variables to hold player's x,y coordinates to the bottom/center of the window
    # updating these in the game loop will move the player object
    playerXLocation = windowWidth/2
    playerYLocation = windowHeight - 100

    #enemy 1 and 2's starting x coordinates. updating these will move the enemy objects
    #I only manipulated the x coordinates for these just to learn how to move them.
    # that's why the enemies only move left/right right now.
    start1X = 1
    start1Y = 0
    start2X = 210
    start2Y = -100

    leftFlankX = start2X-75
    leftFlankY = start2Y

    #these are for the enemys patrolling. they're manipulated in the game loop inlines 106-129
    #basically as long as patrolRight = true, keep moving it right. once it reaches the max width of the window,
    # patrolRight = left and move it left. patrolRight1 for enemy 1 and patrolright2 for enemy2.
    # there must be a better way to do this, especially since our enemies should be dynamically allocated.
    patrolRight1 = True
    patrolRight2 = True

    #scrollValue is the y coordinate of the background. it i incrementd to
    # have the bg scroll. We need to figure out how to infinite scroll. right now
    # everything goes to shit once there's no more image left to scroll
    scrollValue = -1800
    processRunning = True

    #bulletGroup.add(missile)
    #bulletGroup.add(missile2)

    y = 0
    loopCount = 0
    spriteCounter = 0
    enemy2Dead = False
    liveBullet = False
    bulletAnimationCounter = 0

    enemy2Group = pygame.sprite.Group()
    enemy1List = [Enemy() ,Enemy(), Enemy(), Enemy(), Enemy(), Enemy(), Enemy(),Enemy(), Enemy(), Enemy(), Enemy(), Enemy()]
    for enemy in enemy1List:
        enemy.set_image("lightenemy1.png")
        enemy2Group.add(enemy)

    enemy2List = [Enemy() ,Enemy(), Enemy(), Enemy(), Enemy(), Enemy(), Enemy(),Enemy(), Enemy(), Enemy(), Enemy(), Enemy()]
    for enemy in enemy2List:
        enemy.set_image("lightenemy3.png")
        enemy2Group.add(enemy)


    missile = Bullet()
    missile.set_position(-100, 0)
    missile2 = Bullet()
    missile2.set_position(-100, 0)

    playerFire = pygame.mixer.Sound("fire.wav")

    #game loop
    while (processRunning):

        loopCount += 1

        background.set_position(0, y-702)
        background2.set_position(0, y)

        y += 4
        if y >= 702:
            y = 0

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                processRunning = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.set_image("hero1.png")
                    player.set_position(playerXLocation, playerYLocation)
                elif event.key == pygame.K_RIGHT:
                    player.set_image("hero1.png")
                    player.set_position(playerXLocation, playerYLocation)
                elif event.key == pygame.K_UP:
                    player.set_image("hero1.png")
                    player.set_position(playerXLocation, playerYLocation)
                elif event.key == pygame.K_SPACE:
                    #missile = Bullet()
                    '''missile1X = playerXLocation+8
                    missile1Y = playerYLocation+4
                    missile.update_image("playerMissile.png")
                    missile.set_position(missile1X, missile1Y)

                    #missile2 = Bullet()
                    missile2X = playerXLocation+32
                    missile2Y = playerYLocation+4
                    missile2.update_image("playerMissile.png")
                    missile2.set_position(missile2X, missile2Y)

                    bulletGroup.add(missile)
                    bulletGroup.add(missile2)

                    liveBullet = True'''

        #the values in the arguments are updated each loop iteration
        #start1X and start2X are handled by the patrolling

        #enemy1.set_position(start1X, 0)
        #enemy2.set_position(start2X, start2Y)
        #enemy3.set_position(start2X-75, start2Y-100)

        #for enemy in enemy2List:
        #    enemy.set_position(start2X, start2Y)

        enemy2List[0].set_position(start2X, start2Y)
        enemy2List[1].set_position(start2X-75, start2Y-75)
        enemy2List[2].set_position(start2X-150, start2Y-150)
        enemy2List[3].set_position(start2X-225, start2Y-225)
        enemy2List[4].set_position(start2X-300, start2Y-300)
        enemy2List[5].set_position(start2X-375, start2Y-375)

        enemy2List[6].set_position(leftFlankX, leftFlankY)
        enemy2List[7].set_position(leftFlankX-75, leftFlankY-75)
        enemy2List[8].set_position(leftFlankX-150, leftFlankY-150)
        enemy2List[9].set_position(leftFlankX-225, leftFlankY-225)
        enemy2List[10].set_position(leftFlankX-300, leftFlankY-300)
        enemy2List[11].set_position(leftFlankX-375, leftFlankY-375)

        enemy1List[0].set_position(start2X-200, start2Y)
        enemy1List[1].set_position(start2X-275, start2Y-75)
        enemy1List[2].set_position(start2X-350, start2Y-150)
        enemy1List[3].set_position(start2X-425, start2Y-225)
        enemy1List[4].set_position(start2X-500, start2Y-300)
        enemy1List[5].set_position(start2X-575, start2Y-375)

        enemy1List[6].set_position(leftFlankX-200, leftFlankY)
        enemy1List[7].set_position(leftFlankX-275, leftFlankY-75)
        enemy1List[8].set_position(leftFlankX-350, leftFlankY-150)
        enemy1List[9].set_position(leftFlankX-425, leftFlankY-225)
        enemy1List[10].set_position(leftFlankX-500, leftFlankY-300)
        enemy1List[11].set_position(leftFlankX-575, leftFlankY-375)

        # when the enemies start spawning
        if loopCount > 100:
            start2Y += 2
            leftFlankY += 2
            if loopCount > 150:
                start2X += 2.5
                start2Y += 2

                leftFlankX += 2.5
                leftFlankY += 2

                if start2X-375 > windowWidth and start2Y-375 > windowHeight:
                    start2X = 210
                    start2Y = -100
                if leftFlankX-275 > windowWidth and leftFlankY-375 > windowHeight:
                    leftFlankX = 210-75
                    leftFlankY = -100


        #playerXLocation and playerYLocation handled by lines 100-108
        player.set_position(playerXLocation, playerYLocation)

        # this handles if keys are pressed AND HELD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            playerYLocation = playerYLocation + 6
            player.set_image("hero1Thrust.png")
            player.set_position(playerXLocation, playerYLocation)

        if keys[pygame.K_LEFT]:
            playerXLocation = playerXLocation - 6
            player.set_image("hero1Left.png")
            player.set_position(playerXLocation, playerYLocation)

        if keys[pygame.K_RIGHT]:
            playerXLocation = playerXLocation + 6
            player.set_image("hero1Right.png")
            player.set_position(playerXLocation, playerYLocation)

        if keys[pygame.K_UP]:
            playerYLocation = playerYLocation - 6
            player.set_image("hero1Thrust2.png")
            player.set_position(playerXLocation, playerYLocation)

        if keys[pygame.K_SPACE]:
            if loopCount % 7 == 0:
                playerFire.play()
                missile = Bullet()
                missile1X = playerXLocation+8
                missile1Y = playerYLocation+4
                missile.update_image("playerMissile.png")
                missile.set_position(missile1X, missile1Y)

                missile2 = Bullet()
                missile2X = playerXLocation+32
                missile2Y = playerYLocation+4
                missile2.update_image("playerMissile.png")
                missile2.set_position(missile2X, missile2Y)

                bulletGroup.add(missile)
                bulletGroup.add(missile2)

                liveBullet = True

        for missile in bulletGroup:
            if (missile.getY() < 0):
                bulletGroup.remove(missile)
            missile.update()

        # patrolling enemies
        #if patrolRight == true, increment start1X to push itto the right.
        if (patrolRight1 == True):
            start1X += 3
            #once the object hits the edge of the screen, set the variable to False so it does the same thing but left.
            if (start1X > windowWidth - 170):
                patrolRight1 = False
            else:
                patrolRight1 = True
        else:
            start1X -= 3
            if (start1X < 1):
                patrolRight1 = True
            else:
                patrolRight1 = False
        #this is for enemy 2
        #again, i think the patrolling should be taken care of in an enemy class. like an update()
        if (patrolRight2 == True):
            start2X += 0
            if (start2X > windowWidth - 170):
                patrolRight2 = False
            else:
                patrolRight2 = True
        else:
            start2X -= 0
            if (start2X < 1):
                patrolRight2 = True
            else:
                patrolRight2 = False

        # collision detection
        for enemy2 in enemy2List:
            if missile.checkCollision(enemy2):
                enemy2.update_image("lightenemy3Damaged.png")
                missile.destroy()

                enemy2.decrement_Health()
                if enemy2.get_Health() < 0:
                    enemy2.enemyDead() == True
            else:
                if enemy2.enemyDead() == False:
                   enemy2.update_image("lightenemy3.png")

            if enemy2.enemyDead() == True:
                if loopCount % 7 == 0:
                    if (enemy2.getSpriteCounter() < len(deathAnimation)-1):

                        enemy2.update_image(deathAnimation[enemy2.getSpriteCounter()])
                        enemy2.setSpriteCounter(enemy2.getSpriteCounter() + 1)
                    else:
                        enemy2.destroy()

        for enemy1 in enemy1List:
            if missile.checkCollision(enemy1):
                enemy1.update_image("lightenemy3Damaged.png")
                missile.destroy()

                enemy1.decrement_Health()
                if enemy1.get_Health() < 0:
                    enemy1.enemyDead() == True
            else:
                if enemy1.enemyDead() == False:
                   enemy1.update_image("lightenemy1.png")

            if enemy1.enemyDead() == True:
                if loopCount % 7 == 0:
                    if (enemy1.getSpriteCounter() < len(deathAnimation)-1):

                        enemy1.update_image(deathAnimation[enemy1.getSpriteCounter()])
                        enemy1.setSpriteCounter(enemy1.getSpriteCounter() + 1)
                    else:
                        enemy1.destroy()


        # draw the background
        backgroundGroup.draw(window)
        # draw the group with player and enemy objects with their new positions

        enemy2Group.draw(window)

        #player.update(loopCount)
        block_group.draw(window)
        bulletGroup.draw(window)
        # adjust the fps to adjust game speed. fps set to 60 in line 35

        # i dont remember exactly what this does but it's needed
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    sys.exit()