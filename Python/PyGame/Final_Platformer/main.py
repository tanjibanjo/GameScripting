#Lane Pollock
#Python - pygame
#23 July 2025
#Final project for Game Scripting - Platformer

#IMPORTS
import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image

#game class - object oriented
class Game:
    def __init__(self):
        #init and setup
        pygame.init()

        #handle window, clock, and icon
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240)) #second surface we use for rendering - render on small screen and scale up to create pixel art effect

        icon = load_image('entities/player.png')
        pygame.display.set_caption("I41")
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()

        #movement attribute
        self.movement = [False, False]
        #define player!
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))
        #definte assets
        self.assets = {
            'player': load_image('entities/player.png')
        }

    def run(self):
        while True:
            #fill background
            self.display.fill((14, 219, 248))

            #update and render the player
            #update the movement for left and right
            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            #handle events - left and right movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #movement inputs for up and down - uses keyboard keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False

            #blit display onto screen, use scale to scale display to screen size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            #update display, locked at 60 fps
            pygame.display.update()
            self.clock.tick(60)

Game().run() #initalizes a Game object, then calls run in same line