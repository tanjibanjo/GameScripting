#Lane Pollock
#18 July 2025
#dropGame in python

import sys
import pygame
import random

###############
#LOAD
###############

#setup
pygame.init()
#screen
width = 1280
height = 720
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#scenes and loop
scene = 2 #0 = title, 1 = game, 2 = gameover/replay
running = True
dt = 0

#load images
planet = pygame.image.load("planet_blue_smaller.png")
meteor = pygame.image.load("meteor_large.png")

#caption
pygame.display.set_caption("Meteors Incoming!")

#define colors
green = (74, 93, 35)
orange = (243, 121, 78)
black = (0,0,0)

pygame.display.set_icon(meteor)

#Title and game over stuff
titleY = 100
titleFont = pygame.font.SysFont("Arial", 65)
meteorTitle = titleFont.render("It's Raining Meteors", False, green)
gameOverTitle = titleFont.render("Collision", False, green)

#initialize buttons before use
playY = 300
btnMargin = 10
btnFont = pygame.font.SysFont("Arial", 30)
playWord = btnFont.render("PLAY", False, green)
quitWord = btnFont.render("QUIT", False, green)
restartWord = btnFont.render("RESTART", False, orange)
#screen, color, x, y, width, height, curve
playbtn = pygame.draw.rect(screen, black, ((width/2)-(playWord.get_width()/2) - btnMargin, playY - btnMargin, playWord.get_width() + (btnMargin * 2), playWord.get_height() + (btnMargin * 2)), 0)
quitbtn = pygame.draw.rect(screen, black, ((width/4)-(quitWord.get_width()/2) - btnMargin, playY - btnMargin, quitWord.get_width() + (btnMargin * 2), quitWord.get_height() + (btnMargin * 2)), 0)
restartbtn = pygame.draw.rect(screen, green, ((width * .75)-(restartWord.get_width()/2) - btnMargin, playY - btnMargin, restartWord.get_width() + (btnMargin * 2), restartWord.get_height() + (btnMargin * 2)), 0)
###################################
#gameplay setup
counter = 0
numThings = 7
planetX = []
planetY = []
planetSpeed = []
baseSpeed = .5
speedMulti = 1.2

while counter < numThings:
    #add random planet
    #x value
    planetX.append(random.randint(0, width - planet.get_width()))
    #y value
    planetY.append(0 - random.randint(planet.get_height(), planet.get_height() * 2)
)
    #speed
    planetSpeed.append((baseSpeed + random.random()) / 100)
    counter += 1


###############
#GAME LOOP
###############

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ###############
    #MOUSE CLICKS
    ###############
    if pygame.mouse.get_pressed()[0]: #if left click
        coords = pygame.mouse.get_pos()
        if scene == 0:
            if pygame.Rect.collidepoint(playbtn, coords):
                scene = 1
        elif scene == 1:
            counter = 0
            while counter < numThings:
                #box collision check
                if coords[0] >= planetX[counter] and coords[0] <= planetX[counter] + planet.get_width() and coords[1] >= planetY[counter] and coords[1] <= planetY[counter] + planet.get_height():
                    #send back to top
                    planetX[counter] = random.randint(0, width - planet.get_width())
                    planetY[counter] = 0 - random.randint(planet.get_height(), planet.get_height() * 2)

                    #increse speed
                    planetSpeed[counter] *= speedMulti
                counter += 1

    ###############
    #UPDATE
    ###############
    if scene == 1:
        counter = 0
        while counter < numThings:
            #check if hit bottom of screen
            if(planetY[counter] + planet.get_height() > height):
                scene = 2
            planetY[counter] += planetSpeed[counter]
            counter += 1

    ###############
    #DRAW
    ###############
    if scene == 0:
        screen.fill(orange)
        #draw title
        screen.blit(meteorTitle, ((width / 2) - (meteorTitle.get_width()/2), titleY))
        #planet left
        screen.blit(planet, ((width/2) - (meteorTitle.get_width() / 2) - planet.get_width(), titleY) )
        #planet right
        screen.blit(planet, ((width/2) + (meteorTitle.get_width() / 2), titleY) )

        #button changes if hovered over it
        coords = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(playbtn, coords): #make buton green
            playbtn = pygame.draw.rect(screen, green, ((width/2)-(playWord.get_width()/2) - btnMargin, playY - btnMargin, playWord.get_width() + (btnMargin * 2), playWord.get_height() + (btnMargin * 2)), 0)
        else:
            playbtn = pygame.draw.rect(screen, black, ((width/2)-(playWord.get_width()/2) - btnMargin, playY - btnMargin, playWord.get_width() + (btnMargin * 2), playWord.get_height() + (btnMargin * 2)), 0)
            screen.blit(playWord, ((width/2) - (playWord.get_width()/2), playY))
    
    elif scene == 1: #in game
        screen.fill(green)
        counter = 0
        #draw
        while counter < numThings:
            screen.blit(planet, (planetX[counter], planetY[counter]))
            counter +=1

    else: #scene is 2- game over
        screen.fill(black)
        #text
        screen.blit(gameOverTitle, (width/2 - gameOverTitle.get_width()/2, titleY))
        #planet left
        screen.blit(planet, ((width/2) - (gameOverTitle.get_width() / 2) - planet.get_width(), titleY) )
        #planet right
        screen.blit(planet, ((width/2) + (gameOverTitle.get_width() / 2), titleY) )

        #buttons
        coords = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(quitbtn, coords):
            quitbtn = pygame.draw.rect(screen, green, ((width/4)-(quitWord.get_width()/2) - btnMargin, playY - btnMargin, quitWord.get_width() + (btnMargin * 2), quitWord.get_height() + (btnMargin * 2)), 0)
            #restartbtn = pygame.draw.rect(screen, green, ((width * .75)-(restartWord.get_width()/2) - btnMargin, playY - btnMargin, restartWord.get_width() + (btnMargin * 2), restartWord.get_height() + (btnMargin * 2)), 0)

    
    #flip page - render dispplay
    pygame.display.flip()

###############
#QUIT
###############