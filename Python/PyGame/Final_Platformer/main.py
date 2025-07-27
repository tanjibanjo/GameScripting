#Lane Pollock
#Python - pygame
#23 July 2025
#Final project for Game Scripting - Platformer

#IMPORTS
import pygame
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

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
        
        #definte assets
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        #define player!
        self.player = Player(self, (50, 50), (8, 15))

        #tile map
        self.tilemap = Tilemap(self, tile_size=16)

        #camera stuf
        self.scroll = [0, 0]


    def run(self):
        while True:
            #fill background
            self.display.blit(self.assets['background'], (0, 0))

            #camera focus on player
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #render clouds behind tiles
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            #render tile map behind the player
            self.tilemap.render(self.display, offset=render_scroll)

            #update and render the player
            #update the movement for left and right
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)



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
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.velocity[1] = self.player.jump_velocity #just set velocity to negative so player moves up, then physics system will bring the velocity back down
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