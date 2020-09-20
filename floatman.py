import pygame, sys, os # import pygame and sys
import random
import time
clock = pygame.time.Clock() # set up the clock
 
from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

WIDTH = 800
HEIGHT = 800
FPS = 60

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x , y, img, spd):
        pygame.sprite.Sprite.__init__(self)
        self.speed = spd
        self.realx = x
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.x > 900:
            self.rect.x -= random.randint(1100,1500)
        if self.speed < 0 and self.rect.x < -200:
            self.rect.x += random.randint(1100,1500)

    def moveY(self, x):
        self.rect.y += 0

    def moveX(self, x):
        self.rect.x += 0

    def hide(self):
        self.rect.x = -200

    def appear(self):
        self.rect.x = self.realx
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load("./assets/balloons/l1.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/balloons/l2.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/balloons/balloon.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/balloons/r1.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/balloons/r2.png").convert_alpha())   
        self.images.append(pygame.image.load("./assets/balloons/deflated.png").convert_alpha())
        self.index = 2
        self.image = self.images[int(self.index)]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20
        self.gravity = 0
        self.movingUp = False
        self.speedx = 0
        self.lock = False
        self.animate = False
        self.progress = 0
        self.hasFuel = True
        self.hitGround = False
        self.dead = False
        self.movingScreen = False
        self.animateDirection = 0
        self.layerOne = -2
        self.layerTwo = 5
        self.layerThree = -1
        
    def update(self):
        if int(self.progress) == 9:
            self.hasFuel = False
        self.animateDirection = 0

        if self.hasFuel:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.rect.x -= 4
                self.animateDirection = -1
                self.index = 4
            if keystate[pygame.K_RIGHT]:
                self.rect.x += 4
                self.animateDirection = 1
                self.index = 0
            if keystate[pygame.K_UP] and self.lock == False:
                self.rect.y -= 2
                self.movingUp = True
                self.gravity = 0
                self.progress += 0.02
            else: 
                self.movingUp = False
                self.rect.y += self.gravity
                self.gravity += 0.5
        else:
            self.movingUp = False
            self.rect.y += self.gravity
            self.gravity += 0.5
        if self.hasFuel:
            self.wind()

    def wind(self):
        if self.rect.x < 10 and self.rect.bottom < HEIGHT - 30:
            self.rect.y += 10
            self.rect.x += 1
            self.movingUp = False
        if self.rect.x > 740 and self.rect.bottom < HEIGHT - 30:
            self.rect.y += 10
            self.rect.x -= 1
            self.movingUp = False

        if self.rect.y > 400 and self.rect.y < 570:
            self.speedx = self.layerOne
            self.rect.x += self.speedx

        if self.rect.y > 300 and self.rect.y < 400:
            self.speedx = self.layerTwo
            self.rect.x += self.speedx
        
        if self.rect.y > 150 and self.rect.y < 300:
            self.speedx = self.layerThree
            self.rect.x += self.speedx
        if self.rect.y > 150:
            self.speedx = 0
        
        if self.animateDirection == 1:
            self.index = ((random.randint(0,199))/100)
        if self.animateDirection == -1:
            self.index = ((random.randint(300,499))/100)
        if self.animateDirection == 0 and self.hasFuel:
            self.index = 2
        
        self.image = self.images[int(self.index)]

    def moveY(self, x):
        if self.movingScreen:
            self.rect.y += x

    def moveX(self, x):
        if self.movingScreen:
            self.rect.x += x

    def balloonPop(self):
        if self.hasFuel == False and self.rect.bottom > HEIGHT - 30:
            self.index = 5
            self.rect.y = 750
            self.hitGround = True
            self.dead = True
            
        self.image = self.images[int(self.index)]
    

class Visuals(pygame.sprite.Sprite):
    def __init__(self, x , y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movingScreen = True

    def moveY(self, x):
        if self.movingScreen:
            self.rect.y += x

    def moveX(self, x):
        if self.movingScreen:
            self.rect.x += x

class Entities(pygame.sprite.Sprite):
    def __init__(self, x , y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill((0,0,255))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movingScreen = True

    def moveY(self, x):
        if self.movingScreen:
            self.rect.y += x

    def moveX(self, x):
        if self.movingScreen:
            self.rect.x += x


class fuelProgress(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load("./assets/fuel/full.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-1.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-2.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-3.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-4.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-5.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-6.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-7.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/full-8.png").convert_alpha())
        self.images.append(pygame.image.load("./assets/fuel/empty.png").convert_alpha())
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 160
        self.rect.bottom = 70
        self.empty = False
        self.movingScreen = False
    
    def setImage(self):
        if int(self.index) >= 10:
            self.empty = True
            self.index = 10
        else:
            self.image = self.images[int(self.index)]
    
    def getProgress(self, prog):
        self.index = prog

    def moveY(self, x):
        if self.movingScreen:
            self.rect.y += x

    def moveX(self, x):
        if self.movingScreen:
            self.rect.x += x

def gameLoop():
    pygame.display.set_caption('FloatMan') # set the window name

    WINDOW_SIZE = (800,800) # set up window size

    coords = [0,0]
    screen = pygame.display.set_mode(WINDOW_SIZE,coords[0],coords[1]) # initiate screen

    all_sprites = pygame.sprite.Group()
    ground = pygame.sprite.Group()
    platform = pygame.sprite.Group()
    boundaries = pygame.sprite.Group()

    player = Player()

    #end screen
    endimg = pygame.image.load('./assets/images/gameover.png').convert_alpha()
    winimg = pygame.image.load('./assets/images/winner.png').convert_alpha()
    endScreen = pygame.transform.scale(endimg, (800,800))
    winner = pygame.transform.scale(winimg, (800,800))

    #level one 
    sky_img = pygame.image.load('./assets/images/background.png').convert_alpha()
    island_img = pygame.image.load('./assets/images/island.png').convert_alpha()
    sky = Visuals(0,-3200, sky_img)
    groundHB = Entities(0,780,800,20)
    island = Visuals(200,140, island_img)
    islandHB = Entities(222,168,52,10)
    islandBottom = Entities(222,178,52,35)
    islandRight = Entities(276,168,5,45)
    islandLeft = Entities(216,168,5,45)
    progressBar = fuelProgress()

    clouds = []
    movables = []
    movables.append(player)
    movables.append(islandHB)
    movables.append(island)
    movables.append(islandBottom)
    movables.append(islandLeft)
    movables.append(islandRight)

    clearables = []
    clearables.append(islandHB)
    clearables.append(island)
    clearables.append(islandBottom)
    clearables.append(islandLeft)
    clearables.append(islandRight)

    cloud1 = Cloud(900,400,'./assets/images/cloud.png',-5)
    cloud2 = Cloud(1100,450,'./assets/images/cloud.png',-5)
    cloud3 = Cloud(-100,350,'./assets/images/cloud.png',8)
    cloud4 = Cloud(-50,300,'./assets/images/cloud.png',8)
    cloud5 = Cloud(-400,250,'./assets/images/cloud.png',8)
    cloud6 = Cloud(1100,200,'./assets/images/cloud.png',-5)
    cloud7= Cloud(925,150,'./assets/images/cloud.png',-5)
    cloud8 = Cloud(900,420,'./assets/images/secondcloud.png',-5)
    cloud9 = Cloud(-100,330,'./assets/images/secondcloud.png',8)
    cloud10 = Cloud(1100,210,'./assets/images/secondcloud.png',-5)

    clouds.append(cloud1)
    clouds.append(cloud2) 
    clouds.append(cloud3)
    clouds.append(cloud4)
    clouds.append(cloud5)
    clouds.append(cloud6)
    clouds.append(cloud7) 
    clouds.append(cloud8)
    clouds.append(cloud9)
    clouds.append(cloud10)
    all_sprites.add(sky)
    all_sprites.add(cloud1)
    all_sprites.add(cloud2)
    all_sprites.add(cloud3)
    all_sprites.add(cloud4)
    all_sprites.add(cloud5)
    all_sprites.add(cloud6)
    all_sprites.add(cloud7)
    all_sprites.add(cloud8)
    all_sprites.add(cloud9)
    all_sprites.add(cloud10)
    all_sprites.add(island)
    all_sprites.add(player)
    all_sprites.add(progressBar)
    platform.add(islandHB)
    ground.add(groundHB)
    boundaries.add(islandBottom)
    # #level two
    # sky2_load = pygame.image.load('./images/sky2.png').convert_alpha()
    # island_img = pygame.image.load('./images/island.png').convert_alpha()
    # sky_img = pygame.transform.scale(sky_load, (800,800))
    # sky = Visuals(0,0, sky_img)
    # ground = Visuals(0,600, sun_img)
    # groungHB = Entities(0,780,800,20)
    # island = Visuals(200,200, island_img)
    # islandHB = Entities(220,222,50,20)
    # islandBottom = Entities(200,235,100,45)

    i = 0
    level = 1
    running = True
    move = True
    levelUp = 0
    while running:
        #keep loop at right speed
        clock.tick(FPS)

        #events
        for event in pygame.event.get():
            #close window
            if event.type == pygame.QUIT:
                running = False
        
        #update sprites
        all_sprites.update()
        progressBar.getProgress(player.progress)
        progressBar.setImage()

        collision = pygame.sprite.spritecollide(player, boundaries, False)
        if collision:
            player.lock = True
            player.hasFuel = False
            locked = True

        if collision or player.hasFuel == False and sky.rect.y >= -3180:
            player.hasFuel = False
            islandBottom.rect.x = -100
            islandHB.rect.x = -100
            for cl in clouds:
                cl.hide()
            for obj in all_sprites:
                obj.moveY(-player.gravity)
            all_sprites.draw(screen)    

                


        onGround = pygame.sprite.spritecollide(player, ground, False)
        if onGround:
            player.gravity = 0
            player.movingUp = False
            if player.hasFuel == False:
                player.balloonPop()
                locked = False

                
        
        onPlatform = pygame.sprite.spritecollide(player, platform, False)

        if move == True:
            if onPlatform and not collision:
                if level == 5:
                    screen.blit(winner, (0,0))
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                    break
                player.gravity = 0
                player.movingUp = False
                player.movingScreen = False
                player.layerOne -= 2
                player.layerTwo += 2
                player.layerThree -= 2
                island.movingScreen = False
                groundHB.movingScreen = True
                for cl in clouds:
                    if cl.speed > 0:
                        cl.speed += 2
                    else:
                        cl.speed -= 2
                    cl.hide()
                while move:
                    groundHB.moveY(1)
                    for obj in all_sprites:
                        obj.moveY(1)
                    if sky.rect.y == -2400 + i:
                        i += 800
                        break
                    all_sprites.draw(screen)
                    pygame.display.flip()
                player.movingScreen = True
                island.movingScreen = True
                while move:
                    if player.progress > 0:
                        player.progress -= 0.011
                    
                    progressBar.getProgress(player.progress)
                    progressBar.setImage()
                    for ob in movables:
                        ob.moveY(1)
                    all_sprites.draw(screen)
                    pygame.display.flip()
                    if player.rect.y == 650:
                        move = False

                for cl in clouds:
                    cl.appear()
        
        if onPlatform and not collision:
            player.gravity = 0
            player.movingUp = False
            if levelUp == 0:
                levelUp = 1
                level += 1
            if levelUp == 2:
                levelUp = 3
                level += 1
            
        
        if levelUp == 1:
            if island.rect.x > -100 and island.rect.x < 500:
                for ob in clearables:
                    ob.moveX(-2)
            if island.rect.x <= -100:
                for ob in clearables:
                    ob.rect.x = 900
                    ob.rect.y -= 537
            if island.rect.x > 600 and island.rect.x < 901:
                for ob in clearables:
                    ob.moveX(-2)
            if island.rect.x == 600:
                levelUp = 2
                move = True
        
        if levelUp == 3:
            if island.rect.x > 500 and island.rect.x < 900:
                for obj in clearables:
                    obj.moveX(2)
            if island.rect.x >= 900:
                for obj in clearables:
                    obj.rect.y -= 537
                    obj.rect.x = -100
            if island.rect.x < 200 and island.rect.x > -101:
                for obj in clearables:
                    obj.moveX(2)
            if island.rect.x == 200:
                levelUp = 0
                move = True
                    
        #draw sprites
        all_sprites.draw(screen)
        # pygame.draw.rect(screen, (0,255,255),(222,178,52,35))
        # pygame.draw.rect(screen, (255,255,255),(222,168,52,10))
        # pygame.draw.rect(screen, (255,0,255),(216,168,5,45))
        # pygame.draw.rect(screen, (255,0,255),(276,168,5,45))
        pygame.display.flip()
        
        
        if player.dead:
            time.sleep(2)
            while player.dead:
                screen.blit(endScreen, (0,0))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                            player.dead = False
                        if event.key == pygame.K_c:
                            gameLoop()

gameLoop() 
pygame.quit()
