#Lane Pollock
#Python - pygame
#23 July 2025
#Final project for Game Scripting - Platformer

#IMPORTS
import pygame
import sys

#game class - object oriented
class Game:
    def __init__(self):
        #init and setup
        pygame.init()

        #handle window, clock, and icon
        icon = pygame.image.load("data/images/entities/player/idle/00.png")
        pygame.display.set_caption("I41")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        #load images
        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0, 0, 0)) # sets color key for cloud image - 0,0,0 represents black, so black color will be made transparent

        #attributes
        self.img_pos = [160, 260]
        self.movement = [False, False]
        self.collision_area = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            #fill background
            self.screen.fill((14, 219, 248))

            #collision render test
            img_r = pygame.Rect(*self.img_pos, *self.img.get_size())
            #img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height() )
            #collision check
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 100, 155), self.collision_area)

            self.img_pos[1] += self.movement[1] - self.movement[0] #this is to control movment through the impplicit conversion of boolean to int
            self.screen.blit(self.img, self.img_pos)

            #handle events - including k up and down
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #movement inputs for up and down - uses keyboard keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[1] = False

            #update display, locked at 60 fps
            pygame.display.update()
            self.clock.tick(60)

Game().run() #initalizes a Game object, then calls run in same line