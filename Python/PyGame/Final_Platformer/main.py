#Lane Pollock
#Python - pygame
#23 July 2025
#Final project for Game Scripting - Platformer

#IMPORTS
import pygame
import random
import math
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

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
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False)
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        #define player!
        self.player = Player(self, (50, 50), (8, 15))

        #tile map
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        #getting info like position from only tree assets - for spawning leaves
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) #offset spawn of leaves to fit the image better
        
        self.particles = []


        #camera stuff
        self.scroll = [0, 0]


    def run(self):
        while True:
            #fill background
            self.display.blit(self.assets['background'], (0, 0))

            #camera focus on player
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #spawn particle
            for rect in self.leaf_spawners:
                #multiply by large number so that it doesn't always fire - don't want leaves every frame
                if random.random() * 49999 < rect.width * rect.height: # the amount of leaves spawned should be proportional to how large the tree is
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0,20))) #random frame to spawn into


            #render clouds behind tiles
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            #render tile map behind the player
            self.tilemap.render(self.display, offset=render_scroll)

            #update and render the player
            #update the movement for left and right
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3 #sin function gives number between -1 and 1. more natural movement
                if kill:
                    self.particles.remove(particle)

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
                        self.player.jump() #just set velocity to negative so player moves up, then physics system will bring the velocity back down
                    if event.key == pygame.K_LSHIFT:
                        self.player.dash()
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