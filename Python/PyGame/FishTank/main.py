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
waterMap = [v, v, v, v, v, v, v, v,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o,
            o, o, o, o, o, o, o, o]

#switch values to images
for i, item in enumerate(waterMap):
    if waterMap[i] == v:
        waterMap[i] = wave
    if waterMap[i] == o:
        waterMap[i] = water

#screen
width = tiles * waveW
height = tiles * waveH + scoreBuffer
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Fish Tank")

#load fish
fishies = [pygame.image.load("fish_blue.png"),
           pygame.image.load("fish_brown.png"),
           pygame.image.load("fish_green.png"),
           pygame.image.load("fish_orange.png"),
           pygame.image.load("fish_red.png"),] 

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
    count = 0 #count rows
    countx = 0 #count columns

    for i, item in enumerate(waterMap):
        screen.blit(waterMap[i], (0 + (waveW *countx), scoreBuffer + (waveH *count)))
        if (i+1) % tiles == 0:
            count +=1
            countx = 0
        else:
            countx +=1


    #flip page - render dispplay
    pygame.display.flip()

###############
#QUIT
###############
pygame.display.quit()