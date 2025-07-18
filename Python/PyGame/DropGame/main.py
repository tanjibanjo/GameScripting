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
scene = 0 #0 = title, 1 = game, 2 = gameover/replay
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

pygame.display.set_icon(planet)

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

    ###############
    #UPDATE
    ###############

    ###############
    #DRAW
    ###############

    screen.fill(orange)
    #flip page - render dispplay
    pygame.display.flip()

###############
#QUIT
###############