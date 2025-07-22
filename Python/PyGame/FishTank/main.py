#Lane Pollock
#Python
#Fish tank demo in pygame

import sys
import pygame
import random

###############
#LOAD
###############
pygame.init()

tiles = 8
scoreBuffer = 30
wave = pygame.image.load("wave.png")
water = pygame.image.load("water.png")
waveW = wave.get_width()
waveH = wave.get_height()

#placeholder table to represent what background looks like
v = "v" #wave
o = "o" #water
waterMap = {v, v, v, v, v, v, v, v,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o}

#switch values to images
for i in waterMap:
    if i == v:
        i = wave
    if i == o:
        i = water

#screen
width = tiles * waveW
height = tiles * waveH
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Fish Tank")

###############
#GAME LOOP
###############
gameOver = False
while(not gameOver):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    ###############
    #Mouse Clicks
    ###############

    ###############
    #UPDATE
    ###############

    ###############
    #DRAW
    ###############
    #flip page - render dispplay
    pygame.display.flip()

###############
#QUIT
###############
pygame.display.quit()