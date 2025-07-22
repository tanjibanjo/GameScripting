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

counter = 0
rFish = 8
lFish = 8
lFishX = []
lFishY = []
lFishSpeed = []
lFishSpeedMod = []
lFishImage = []

while counter < lFish:
    lFishImage.append(random.choice(fishies))
    lFishX.append(0)
    #start between the score buffer and the bottom - fish size
    lFishY.append(random.randint(scoreBuffer * 2, height - fishies[0].get_height()))
    #speed
    lFishSpeed.append((.1 + random.random()) / 50)
    lFishSpeedMod.append((.1 + random.random()) /50)
    counter +=1

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

    #move left fish to the right
    i = 0
    while i < lFish:
        lFishX[i] += lFishSpeed[i]
        i+=1

    ###############
    #DRAW
    ###############

    #BACKGROUND STUFF
    count = 0 #count rows
    countx = 0 #count columns
    
    for i, item in enumerate(waterMap):
        screen.blit(waterMap[i], (0 + (waveW *countx), scoreBuffer + (waveH *count)))
        if (i+1) % tiles == 0:
            count +=1
            countx = 0
        else:
            countx +=1

    #DRAW FISH
    counter = 0
    while counter < lFish:
        screen.blit(lFishImage[counter], (lFishX[counter], lFishY[counter]))
        counter +=1


    #flip page - render dispplay
    pygame.display.flip()

###############
#QUIT
###############
pygame.display.quit()