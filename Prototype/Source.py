#I guess pygame doesn't need to be imported?
import pygame
import sys
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color = white, width = 64, height = 64):
        super(Enemy, self).__init__()

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
    pygame.init()

    #Initial setup stuff =============================
    windowSize = windowWidth, windowHeight = 540, 702
    window = pygame.display.set_mode(windowSize, 0, 32)
    pygame.display.set_caption("asdf")
    clock = pygame.time.Clock()
    fps = 60
    # ================================================

    #pygame.sprite.Group() is a group that will hold our objects(blocks)
    # idk why I need two groups, for some reason they wont all show up on the screen if they're in 1 group
    block_group = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    # ==================================================================
    # declare our objects, so far we only have 4.
    # the player's missile could be 5th, enemy missiles 6th (assuming they're the same image), + whatever else
    player = Player()
    enemy1 = Enemy()
    enemy2 = Enemy()
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
    player.set_image("hero1.png")
    enemy1.set_image("lightenemy1.png")
    enemy2.set_image("lightenemy2.png")

    # add our objects to the groups we declared in lines 40,41.
    # again, idk why i needed two groups
    block_group.add(player)
    block_group.add(enemy1)
    block_group.add(enemy2)
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
    start2X = 500

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


    y = 0
    #game loop
    while (processRunning):
        #set the position with an updated y coordinate
        #window.blit(background.get_image(), background_rect)
        #scrollValue += 1

        #window.blit(background.get_image(), (0, y))
        background.set_position(0, y-702)
        #window.blit(background.get_image(), (0,y-540))
        background2.set_position(0, y)

        y += 4
        if y >= 702:
            y = 0

        #heighth was 702. i tested speeds 9 and 6 and thought it worked. i tried speed4, went to shit. realized speed needed to be div by height. realized 702 was div by 3, thats why 6,9 worked -_-



        #if y > height:
         #   y = -height
        #if y1 > height:
         #   y1 = -height

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                processRunning = False

        #the values in the arguments are updated each loop iteration
        #start1X and start2X are handled by the patrolling
        enemy1.set_position(start1X, 0)
        enemy2.set_position(start2X, 250)
        # playerXLocation and playerYLocation handled by lines 100-108
        player.set_position(playerXLocation, playerYLocation)

        # this handles if keys are pressed AND HELD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerXLocation = playerXLocation - 6
        if keys[pygame.K_RIGHT]:
            playerXLocation = playerXLocation + 6
        if keys[pygame.K_UP]:
            playerYLocation = playerYLocation - 6
        if keys[pygame.K_DOWN]:
            playerYLocation = playerYLocation + 6

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
        #this isfor enemy 2
        #again, i think the patrolling should be taken care of in an enemy class.
        if (patrolRight2 == True):
            start2X += 7
            if (start2X > windowWidth - 170):
                patrolRight2 = False
            else:
                patrolRight2 = True
        else:
            start2X -= 7
            if (start2X < 1):
                patrolRight2 = True
            else:
                patrolRight2 = False



        # draw the background
        backgroundGroup.draw(window)
        # draw the group with player and enemy objects with their new positions
        block_group.draw(window)
        # adjust the fps to adjust game speed. fps set to 60 in line 35
        clock.tick(fps)
        # i dont remember exactly what this does but it's needed
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    sys.exit()