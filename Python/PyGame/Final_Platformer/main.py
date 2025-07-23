#Lane Pollock
#Python - pygame
#23 July 2025
#Final project for Game Scripting - Platformer

#IMPORTS
import pygame
import sys

#init and setup
pygame.init()

screen = pygame.display.set_mode(640,480)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #update display, locked at 60 fps
    pygame.display.update()
    clock.tick(60)