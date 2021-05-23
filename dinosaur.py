import pygame
from pygame.locals import *
import sys
import random
#import tflearn
pygame.init()

# you didn't install pip install git+https://github.com/Kojoley/atari-py.git
# you didn't install mujuco

"""network = input_data(shape=[None, 4, 1], name='input')
network = fully_connected(network, 1, activation='linear')
network = regression(network, optimizer='adam', learning_rate=1e-2, loss='mean_square', name='target')
model = tflearn.DNN(network)"""

# create the display surface object
# of specific dimension..e(500, 500).
win = pygame.display.set_mode((1000, 500))

pygame.display.set_caption("Dinosaur")
until = False
jump = False
score = 0
has = False
highscore = 0
duck = False
restored = True
havejump = False
gameover = False
myfont = pygame.font.SysFont("monospace", 15)

initialdinox = 100
initialdinoy = 350
initialdinowidth = 90
initialdinoheight = 98

class Dinosaur:
    def __init__(self):
        self.x = 100
        self.y = 350
        self.vel = 10
        self.width = 90
        self.height = 98
        self.color = (0, 0, 0)

class Cactus:
    def __init__(self):
        self.x = 1000
        self.y = 350
        self.vel = 10
        self.width = 55
        self.height = 98
        self.color = (0, 0, 0)

class Bird:
    def __init__(self):
        self.x = 1000
        self.y = 355
        self.vel = 10
        self.width = 60
        self.height = 35
        self.color = (0, 0, 0)

dinosaur = Dinosaur()
cactus = Cactus()
bird = Bird()
run = True
birdonscreen = False
currenttry = random.randint(0,1000)
pressdown = False
gameover = False
dinoimage = pygame.image.load("dinosaur.png")
dinoimage = pygame.transform.scale(dinoimage, (dinosaur.width, dinosaur.height))
cactusimage = pygame.image.load("cactus.png")
cactusimage = pygame.transform.scale(cactusimage, (cactus.width, cactus.height))
duckingimage = pygame.image.load("ducking.png")
duckingimage = pygame.transform.scale(duckingimage, (dinosaur.width*2, int(dinosaur.height/2)))
birdimage = pygame.image.load("bird.png")
birdimage = pygame.transform.scale(birdimage, (60, 35))
tries = {}

def genetic(currenttry, pressdown):
    if cactus.x - dinosaur.x < currenttry:
        pressdown = True
    return pressdown

def keys(jump, duck):
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or pressdown:
        jump = True

    if keys[pygame.K_DOWN]:
        duck = True
    else:
        duck = False
    return jump, duck

def jumping(jump, until, pressdown):
    if jump and dinosaur.y > 150 and until == False:
        dinosaur.y -= dinosaur.vel
    if dinosaur.y <= 150:
        until = True
    if until:
        dinosaur.y += dinosaur.vel
        if dinosaur.y >=350:
            until = False
            jump = False
            pressdown = False
    return jump, until, pressdown

def ducking(has, restored):
    if duck:
        dinosaur.height = initialdinoheight/2
        dinosaur.width = initialdinowidth*2
        if not has:
            dinosaur.y += initialdinoheight/2
            has = True
        restored = False
    else:
        dinosaur.height = initialdinoheight
        dinosaur.width = initialdinowidth
        if not restored and has:
            dinosaur.y -= initialdinoheight/2
            restored = True
            has = False
    return has, restored

def draw():
    win.fill((255, 255, 255))
    if duck:
        win.blit(duckingimage, (dinosaur.x, dinosaur.y))
    else:
        win.blit(dinoimage, (dinosaur.x, dinosaur.y))
    win.blit(cactusimage, (cactus.x, cactus.y))
    if birdonscreen:
        win.blit(birdimage, (bird.x, bird.y))
    #pygame.draw.rect(win, dinosaur.color, (dinosaur.x, dinosaur.y, dinosaur.width, dinosaur.height))
    #pygame.draw.rect(win, cactus.color, (cactus.x, cactus.y, cactus.width, cactus.height))
    showscore = myfont.render("SCORE: " + str(score), 1, (0,0,0))
    win.blit(showscore, (800, 50))
    showhighscore = myfont.render("HIGHSCORE: " + str(highscore), 1, (0,0,0))
    win.blit(showhighscore, (600, 50))
    pygame.display.update()

def cactuscheck(cactus):
    cactus.x -= cactus.vel
    if cactus.x <= 0:
        cactus = Cactus()

    return cactus

def birdcheck(bird, birdonscreen):
    if random.randint(1, 100) == 1 and birdonscreen == False:
        bird = Bird()
        birdonscreen = True
    try:
        if bird.x <= 0:
            birdonscreen = False
        bird.x -= bird.vel
    except:
        pass
    return bird, birdonscreen

def checkgameover(gameover):
    if dinosaur.x <= cactus.x <= dinosaur.x + dinosaur.width and dinosaur.y <= cactus.y + cactus.height <= dinosaur.y + dinosaur.height:
        gameover = True
    try:
        print(dinosaur.x, dinosaur.y, dinosaur.width, dinosaur.height, bird.x, bird.y)
        if dinosaur.x <= bird.x <= dinosaur.x + dinosaur.width and dinosaur.y <= bird.y + bird.height <= dinosaur.y + dinosaur.height:
            gameover = True
    except:
        pass
    return gameover

# infinite loop
while run:
    if not gameover:
        jump, duck = keys(jump, duck)
        pressdown = genetic(currenttry, pressdown)
        jump, until, pressdown = jumping(jump, until, pressdown)
        has, restored = ducking(has, restored)
        draw()
        cactus = cactuscheck(cactus)
        """try:
            bird, birdonscreen = birdcheck(bird, birdonscreen)
        except:
            pass"""
        gameover = checkgameover(gameover)
        score += 1
    else:
        pygame.time.delay(10)
        win.fill((255, 255, 255))
        showgameover = myfont.render("GAMEOVER", 1, (0,0,0))
        showplayagain = myfont.render("PRESS ANY KEY TO PLAY AGAIN", 1, (0,0,0))
        win.blit(showgameover, (500, 250))
        win.blit(showplayagain, (500, 350))
        tries[currenttry] = score
        currenttry = random.randint(0,1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(max(tries, key=tries.get))
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                highscore = score
                score = 0
                dinosaur = Dinosaur()
                cactus = Cactus()
                bird = Bird()
                gameover = False
        pygame.display.update()
