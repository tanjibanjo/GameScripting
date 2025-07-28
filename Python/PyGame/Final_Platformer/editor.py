#Lane Pollock
#Python - pygame
#23 July 2025
#script for a basic level editor

#IMPORTS
import pygame
import sys
from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

#game class - object oriented
class Editor:
    def __init__(self):
        #init and setup
        pygame.init()

        #handle window, clock, and icon
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240)) #second surface we use for rendering - render on small screen and scale up to create pixel art effect

        pygame.display.set_caption("Editor")

        self.clock = pygame.time.Clock()
        
        #definte assets
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone')
        }

        
        #movement attributes for camera
        self.movement = [False, False, False, False]

        #tile map
        self.tilemap = Tilemap(self, tile_size=16)

        #camera stuff
        self.scroll = [0, 0]

        #convert assets to a list - which gives the key values
        self.tile_list = list(self.assets) 
        self.tile_group = 0 #which group -decor, grass, etc
        self.tile_variant = 0 #which tile within that group

        self.clicking = False
        self.right_clicking = False


    def run(self):
        while True:
            #fill background
            self.display.fill((0, 0, 0))

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100) #semi transparent - 0-255 range

            self.display.blit(current_tile_img, (5, 5))

            #handle events - left and right movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                    #scroll between groups of decor
                    if event.button == 4:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list) # loops through the list
                    if event.button == 5:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list) # loops through the list
                #movement inputs for up and down - uses keyboard keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            #blit display onto screen, use scale to scale display to screen size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            #update display, locked at 60 fps
            pygame.display.update()
            self.clock.tick(60)

Editor().run() #initalizes a Game object, then calls run in same line