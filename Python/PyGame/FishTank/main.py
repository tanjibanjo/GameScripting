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