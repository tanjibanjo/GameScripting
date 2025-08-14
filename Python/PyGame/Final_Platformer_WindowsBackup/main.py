#Lane Pollock
#Python - pygame
#23 July 2025
#Final project for Game Scripting - Platformer

#IMPORTS
import pygame
import random
import math
import sys
import os
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark

#game class - object oriented
class Game:
    def __init__(self):
        #init and setup
        pygame.init()

        #handle window, clock, and icon
        self.width = 640 #1040
        self.height = 480 #880
        self.screen = pygame.display.set_mode((self.width, self.height)) #640, 480
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA) #second surface we use for rendering - render on small screen and scale up to create pixel art effect #320, 240
        #third display for effect stuff
        self.display_2 = pygame.Surface((320, 240))
        self.screen_rect = pygame.Rect(0, 0, 320, 340)

        icon = load_image('entities/player.png')
        pygame.display.set_caption("I41")
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()

        #Title and game over stuff
        self.titley = 30
        self.title_font = pygame.font.SysFont("Arial", 20)
        self.options_font = pygame.font.SysFont("Arial", 10)
        self.start_title = self.title_font.render("2d.samurai", False, (0, 0, 0))
        self.start_title_options = self.options_font.render("[press enter to begin, clear all enemies to advance]", False, (255, 255, 255))
        self.game_over_title = self.title_font.render("To be contined...", False, (0, 0, 0))
        self.game_over_options = self.options_font.render("[press enter to replay, or escape to exit]", False, (255, 255, 255))

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
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png')
        }

        #sound effects
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.7)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.85)

        self.clouds = Clouds(self.assets['clouds'], count=16)

        #define player!
        self.player = Player(self, (50, 50), (8, 15))

        #tile map
        self.tilemap = Tilemap(self, tile_size=16)

        #load level
        self.number_levels = len(os.listdir('data/maps'))
        self.level = 'start'
        self.load_level(self.level)

        #game stuff- title screen etc
        self.scene = 0
        #check for if input in the main loop should even be taken
        self.block_input = False

        #for screenshake
        self.screenshake = 0
        self.running = True

    #function to load the map
    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        #getting info like position from only tree assets - for spawning leaves
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) #offset spawn of leaves to fit the image better
        
        #enemy spawning
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0: #player
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))


        #particles and projectiles
        self.projectiles = []

        self.particles = []

        self.sparks = []


        #camera stuff
        self.scroll = [0, 0]
        
        self.dead = 0

        #transition for between levels
        self.transition = -30




    def run(self):
        #music - load and start ambience as well
        pygame.mixer.music.load('data/music2.wav')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) #-1 loops forever
        self.sfx['ambience'].play(-1)

        while self.running:
            while self.scene == 0: #start screen
                #fill background
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))

                #camera focus on player
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]) - 30)

                #spawn particle
                for rect in self.leaf_spawners:
                    #multiply by large number so that it doesn't always fire - don't want leaves every frame
                    if random.random() * 49999 < rect.width * rect.height: # the amount of leaves spawned should be proportional to how large the tree is
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0,20))) #random frame to spawn into


                #render clouds behind tiles
                self.clouds.update()
                self.clouds.render(self.display_2, offset=render_scroll)


                #render tile map behind the player
                self.tilemap.render(self.display, offset=render_scroll)

                #update and render the player
                #update the movement for left and right
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

                #handle particles
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

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            #reset
                            self.level = 0
                            self.load_level(self.level)
                            self.scene = 1
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                            pygame.quit()
                            sys.exit()

                #render the title
                self.display.blit(self.start_title, (self.screen_rect.centerx - self.start_title.get_width()/2, self.titley))
                self.display.blit(self.start_title_options,(self.screen_rect.centerx - self.start_title_options.get_width()/2, self.titley + 18) )

                #display stuff
                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)

            while self.scene == 1:
                #fill background
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))
                #handle screenshake
                self.screenshake = max(0, self.screenshake - 1)

                if not len(self.enemies):
                    self.transition += 1
                    if self.transition > 30:
                        #check if last level is finished
                        if self.level + 3 < self.number_levels: #level is not the last one - account for two extra levels in start and game over screens
                            self.level = min(self.level + 1, self.number_levels - 1) #increment to next level if all enemies are destroyed - levels must be names in ascending order
                            self.load_level(self.level)
                        else: #equal 
                            self.block_input = True
                            self.scene = 2
                            self.load_level('game_over')
                            self.movement[0] = False
                if self.transition < 0:
                    self.transition +=1

                if self.dead:
                    self.dead += 1
                    if self.dead == 10:
                        self.transition = min(30, self.transition + 1)
                    if self.dead > 40:
                        self.load_level(self.level)

                #camera focus on player
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                #spawn particle
                for rect in self.leaf_spawners:
                    #multiply by large number so that it doesn't always fire - don't want leaves every frame
                    if random.random() * 49999 < rect.width * rect.height: # the amount of leaves spawned should be proportional to how large the tree is
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0,20))) #random frame to spawn into


                #render clouds behind tiles
                self.clouds.update()
                self.clouds.render(self.display_2, offset=render_scroll)


                #render tile map behind the player
                self.tilemap.render(self.display, offset=render_scroll)

                #render enemies
                for enemy in self.enemies.copy():
                    kill = enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if kill:
                        self.enemies.remove(enemy)


                if not self.dead:
                    #update and render the player
                    #update the movement for left and right
                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)

                #render the projecvtiles
                #[[x, y], direction, timer]
                for projectile in self.projectiles.copy():
                    projectile[0][0] += projectile[1]
                    projectile[2] += 1
                    img = self.assets['projectile']

                    self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                    if self.tilemap.solid_check(projectile[0]): #hits something solid
                        self.projectiles.remove(projectile)
                        for i in range(4):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif projectile[2] > 360: #if timer is greater than 6s
                        self.projectiles.remove(projectile)
                    elif abs(self.player.dashing) < 50: # give i frame
                        if self.player.rect().collidepoint(projectile[0]):
                            self.projectiles.remove(projectile)
                            self.dead += 1
                            self.sfx['hit'].play()
                            self.screenshake = max(25, self.screenshake)
                            for i in range(30): #spawn 30 sparks when player is hit
                                angle = random.random() * math.pi * 2 #random angle in a circle
                                speed = random.random() * 5
                                self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                                self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * .5, math.sin(angle + math.pi) * speed * .5], frame=random.randint(0, 7)))

                #handle sparks
                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display, offset=render_scroll)
                    if kill:
                        self.sparks.remove(spark)

                #create display mask - to convert many colors to two
                display_mask = pygame.mask.from_surface(self.display)
                display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0)) #first argument is the color of the outlines (0000 is black)
            

                #blit the sillhouette, underneath other stuff
                for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]: #1 pixel in each direction gives outline
                    self.display_2.blit(display_sillhouette, offset)
                
                #handle particles
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
                    if not self.block_input:
                        #movement inputs for up and down - uses keyboard keys
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                self.movement[0] = True
                            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                self.movement[1] = True
                            if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                                if self.player.jump(True): #just set velocity to negative so player moves up, then physics system will bring the velocity back down
                                    self.sfx['jump'].play()
                            if event.key == pygame.K_LSHIFT or event.key == pygame.K_x:
                                self.player.dash()
                            if event.key == pygame.K_ESCAPE:
                                self.running = False
                                pygame.quit()
                                sys.exit()
                    if event.type == pygame.KEYUP: #release key
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.movement[1] = False
                        if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                            if not self.player.grounded:
                                self.player.jump(False) #passing false means the jump button is disengaged, and brings gravity back

                #only when transitioning
                if self.transition:
                    transition_surf = pygame.Surface(self.display.get_size())
                    pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                    transition_surf.set_colorkey((255, 255, 255))
                    self.display.blit(transition_surf, (0, 0))


                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)

            while self.scene == 2: #game over screen
                #fill background
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))

                #camera focus on player
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

                #spawn particle
                for rect in self.leaf_spawners:
                    #multiply by large number so that it doesn't always fire - don't want leaves every frame
                    if random.random() * 49999 < rect.width * rect.height: # the amount of leaves spawned should be proportional to how large the tree is
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0,20))) #random frame to spawn into


                #render clouds behind tiles
                self.clouds.update()
                self.clouds.render(self.display_2, offset=render_scroll)


                #render tile map behind the player
                self.tilemap.render(self.display, offset=render_scroll)

                #update and render the player
                #update the movement for left and right
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

                if self.dead:
                    self.dead += 1
                    if self.dead == 10:
                        self.transition = min(30, self.transition + 1)
                    if self.dead > 40:
                        self.load_level('game_over')

                #handle particles
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

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            #reset
                            self.level = 0
                            self.load_level(self.level)
                            self.scene = 1
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                            pygame.quit()
                            sys.exit()
                    if event.type == pygame.KEYUP: #release key
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.movement[1] = False
                        if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                            if not self.player.grounded:
                                self.player.jump(False) #passing false means the jump button is disengaged, and brings gravity back


                #render the title
                self.display.blit(self.game_over_title, (self.width/4 - self.game_over_title.get_width()/1.5, self.titley))
                self.display.blit(self.game_over_options,(self.width/4 - self.game_over_title.get_width(), self.titley + 18) )

                #display stuff
                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)


Game().run() #initalizes a Game object, then calls run in same line