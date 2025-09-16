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
from scripts.entities import PhysicsEntity, Player, Enemy, PlayerType
from scripts.utils import load_image, load_images, Animation, SceneType, GameData, convert_time
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.screens import Screens, ScreenType

BASE_PATH = os.getcwd()


#game class - object oriented
class Game:
    def __init__(self):
        #init and setup
        pygame.init()

        #handle window, clock, and icon
        self.width = 640 #1280
        self.height = 480 #960
        self.screen = pygame.display.set_mode((self.width, self.height)) #640, 480
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA) #second surface we use for rendering - render on small screen and scale up to create pixel art effect #320, 240
        #third display for effect stuff
        self.display_2 = pygame.Surface((320, 240))
        self.screen_rect = pygame.Rect(0, 0, 320, 340)
        #variables for setting screen size
        self.large_screen = 0

        icon = load_image('entities/player.png')
        pygame.display.set_caption("I41")
        pygame.display.set_icon(icon)

        #clock stuff - going to be used to give the player a score that factors in how long it took them to finish the game
        self.clock = pygame.time.Clock()
        self.start_point = pygame.time.get_ticks() #set it here but it will be changed to start when the first level begins

        #movement attribute
        self.movement = [False, False]
        
        #define assets
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

        self.clouds = Clouds(self.assets['clouds'], count=10)

        #define player!
        self.player = Player(self, (50, 50), (8, 15), PlayerType.ASSASSIN)
        #variables to keep track of the player score and deaths - maybe set up for time to clear later
        self.player_deaths = 0
        self.player_level_score = 0 #for each level - if respawn on, reset the score since enemies reset
        self.player_total_score = 0 #to keep track of score as you progress through levels, once cleared - add here

        #tile map
        self.tilemap = Tilemap(self, tile_size=16)

        #controls screen
        self.user_interface = self.load_screen(ScreenType.START)
        
        #declare save data container - list of GameData types
        self.save_data = []

        #load level
        self.number_levels = len(os.listdir(BASE_PATH + '/data/maps'))
        self.level = 'start'
        self.load_level(self.level)
        self.levels_passed = 0
        self.maps = {}

        #load maps - 0 for false, this is for random map selection
        i=0
        for j in range(self.number_levels - 2):
            self.maps[i] = 0
            i+=1


        #game stuff- title screen etc
        self.scene = SceneType.START
        #check for if input in the main loop should even be taken
        self.block_input = False

        #for screenshake
        self.screenshake = 0
        self.running = True

        #for mouse click timing
        self.count = 0

    #function to change the screen size
    def change_screen_size(self):
        if not self.large_screen:
            self.large_screen += 1
            self.width = 960 #1280
            self.height = 720 #960
            self.screen = pygame.display.set_mode((self.width, self.height)) #640, 480
        else:
            self.large_screen -= 1
            self.width = 640 #1280
            self.height = 480 #960
            self.screen = pygame.display.set_mode((self.width, self.height)) #640, 480
        
    #function to return a map id in int form
    # -should make sure that the map hasn't been used yet and also keeps track of how many maps cleared
    #  -this way, there can be a bunch of maps and it will be more randomized runs
    def get_map(self):
        choice = random.randint(1, self.number_levels - 3)
        if not self.maps[choice]:
            return choice
        else:
            while self.maps[choice]:
                choice = random.randint(1, self.number_levels - 3)
                if not self.maps[choice]:
                    return choice


    #function to load the map
    def load_level(self, map_id):
        self.tilemap.load(BASE_PATH + '/data/maps/' + str(map_id) + '.json')
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
        
        #reset dead and level score, as well as speed mod
        self.dead = 0
        self.player_level_score = 0


        #transition for between levels
        self.transition = -30

    #function to reset the ui state - passing false resets to menu, true resets a new run
    def reset(self, new_run=False):
        if new_run: # (true is passed, new run will start)
            #map reload
            i=0
            for j in range(self.number_levels - 2):
                self.maps[i] = 0
                i+=1
                
            #music
            pygame.mixer.music.fadeout(2000)
            pygame.mixer.music.unload()
            pygame.mixer.music.load('data/assassin.wav' if self.player.player_class == PlayerType.ASSASSIN else 'data/rogue.wav')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            #level
            self.levels_passed = 0
            self.level = 0
            self.load_level(self.level)
            #scene back to gameplay
            self.scene = SceneType.GAMEPLAY
            self.block_input = False
            #reset timer
            self.start_point = pygame.time.get_ticks()
            #player stats
            self.player_deaths = 0
            self.player_level_score = 0
            self.player_total_score = 0
            self.player.speed_mod = 2.0 if self.player.player_class == PlayerType.ASSASSIN else 1.7
            self.player.dash_mod = 4
        else:
            #music is already running from end game screen in this case
            self.level = 'start'
            self.load_level(self.level)
            #revert scene
            self.scene = SceneType.START
            self.user_interface = self.load_screen(ScreenType.START)
            self.block_input = False

    #the load game function should read the file (if exists) and then add GameData objects to the saveData in main
    def load_game(self):
        #try to open the file
        try:
            with open('save_game_data.txt', 'r') as file:
                while True:
                    #try and except only for the first line to control the loop
                    try:
                        deaths = int(file.readline().strip())
                    except ValueError:
                        break
                    time = file.readline().strip()
                    score = int(file.readline().strip())
                    rank = file.readline().strip()

                    #make GameData
                    save = GameData(deaths, time, score, rank)

                    #add to list
                    self.save_data.append(save)
        except FileNotFoundError:
            print('No save data found.')

    #the save game function should add the current run stats to the list of GameData, then write to the save file
    def save_game(self):
        #handle time
        self.seconds_passed = round(self.seconds_passed, 1)
        self.formatted_time = convert_time(self.seconds_passed)

        self.player_total_score = max((self.player_total_score + ((180 - self.seconds_passed) * 7) - self.player_deaths * 49), 0)


        #append the list
        try:
            #deaths, time passed, score, rank
            self.save_data.append(GameData(self.player_deaths, self.formatted_time, self.player_total_score, self.get_rank()))
        except AttributeError: #raised if the values needed to instantiate GameData are not present(dont exist)
            print('no GameData appended')

        #get the file set up to write 
        try:
            #using with automatically closes the file
            with open('save_game_data.txt', 'w') as file:
                for save in self.save_data:
                    #have to convert to str to write to a txt file
                    file.write(str(save.deaths) + '\n')
                    file.write(save.time + '\n')
                    file.write(str(save.score) + '\n')
                    file.write(save.rank + '\n')
        except:
            print('error with writing save to the file')

        #print('reading from the file for verification')
        #with open('save_game_data.txt', 'r') as file:
        #    while True:
        #        line = file.readline()
        #        if not line:
        #           break
        #        print(line.strip())
        
    #function to close the game - this does not include save game
    def close_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

    #function will take a designation and return the correct screen for use in the main loop - so we dont have extra screens just made and not used
    def load_screen(self, designation):
        return Screens(designation, self)

    #function that takes the player score and returns a letter grade based on that score
    def get_rank(self):
        if self.player_total_score > 2700:
            return 'S'
        elif self.player_total_score > 2200:
            return 'A'
        elif self.player_total_score > 1600:
            return 'B'
        elif self.player_total_score > 1100:
            return 'C'
        elif self.player_total_score > 800:
            return 'D'
        else:
            return 'F'

    def run(self):

        
        #music - load and start ambience as well
        pygame.mixer.music.load('data/TitleScene1.wav')
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1) #-1 loops forever


        self.sfx['ambience'].play(-1)

        self.load_game()

        while self.running:
            while self.scene == SceneType.START: #start screen
                #fill background
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))

                #handle screenshake
                self.screenshake = max(0, self.screenshake - 1)

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
                
                #get mouse coords for button interactions
                self.count = max(self.count - 1, 0)

                coords = pygame.mouse.get_pos()
                clicked = False
                if pygame.mouse.get_pressed()[0] and self.count == 0:
                    clicked = True #left mouse button
                    self.count = 30

                #render the title
                self.user_interface.update(coords, clicked=clicked)
                self.user_interface.render(self.display)

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
                        if event.key == pygame.K_TAB:
                            self.change_screen_size()


                #display stuff
                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)

            while self.scene == SceneType.GAMEPLAY:
                #fill background
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))
                #handle screenshake
                self.screenshake = max(0, self.screenshake - 1)

                #logic for game mode - clear the enemies then the level will progress
                if not len(self.enemies):
                    self.transition += 1
                    if self.transition > 30:
                        #check if last level is finished
                        if self.levels_passed + 3 < self.number_levels: #level is not the last one - account for two extra levels in start and game over screens
                            #use get_map to get a random map id, but first make sure to mark this one as used
                            self.maps[self.level] += 1 #increment to true
                            self.level = self.get_map()
                            
                            #self.level = min(self.level + 1, self.number_levels - 1) #increment to next level if all enemies are destroyed - levels must be names in ascending order
                            self.levels_passed +=1
                            #add score
                            self.player_total_score += self.player_level_score
                            #load new level
                            self.load_level(self.level)
                        else: #equal 
                            self.levels_passed += 1
                            self.maps[self.level] += 1

                            self.block_input = True
                            self.scene = SceneType.GAME_OVER
                            self.movement[0] = False
                            #score
                            self.player_total_score += self.player_level_score
                            #game over
                            self.load_level('game_over')
                            self.save_game()
                            #ui for game over

                            self.user_interface = self.load_screen(ScreenType.GAME_OVER)
                            pygame.mixer.music.fadeout(2000)
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load('data/TitleScene1.wav')
                            pygame.mixer.music.set_volume(0.6)
                            pygame.mixer.music.play(-1)

                if self.transition < 0:
                    self.transition +=1

                #PLAYER DEATH LOGIC
                if self.dead:
                    self.dead += 1
                    if self.dead == 10:
                        self.transition = min(30, self.transition + 1)
                    if self.dead > 40:
                        self.load_level(self.level)
                        self.player_deaths += 1
                        self.player.speed_mod = 2.2 if self.player.player_class == PlayerType.ASSASSIN else 1.7
                        self.player.dash_mod = 4

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


                #render clouds behind tiles - passing display_2 so it doesnt get an outline
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
                    elif abs(self.player.dashing) < 50 and not self.player.sliding: # give i frame if in dash or slide
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
                            if event.key == pygame.K_c or event.key == pygame.K_LCTRL:
                                self.player.slide()
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

                
                #count the time passed 
                self.seconds_passed = (pygame.time.get_ticks() - self.start_point) / 1000


                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)


            while self.scene == SceneType.GAME_OVER: #game over screen
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

                #get mouse coords for button interactions
                self.count = max(self.count - 1, 0)

                coords = pygame.mouse.get_pos()
                clicked = False
                if pygame.mouse.get_pressed()[0] and self.count == 0:
                    clicked = True #left mouse button
                    self.count = 30 #stop the mouse from sending clicked 

                #render and update the ui
                self.user_interface.update(coords, clicked=clicked)
                self.user_interface.render(self.display)

                #handle events - left and right movement
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
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

                #display stuff
                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                #screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)

            while self.scene == SceneType.UTILITY: #this scene is for any other screens like options, controls, credits, etc
                #fill background
                self.display.fill((0, 0, 0, 0))
                self.display_2.blit(self.assets['background'], (0, 0))

                #render clouds behind tiles
                self.clouds.update()
                self.clouds.render(self.display_2)

                #get mouse coords for button interactions
                self.count = max(self.count - 1, 0)
                coords = pygame.mouse.get_pos()
                clicked = False
                if pygame.mouse.get_pressed()[0] and self.count == 0:
                    clicked = True #left mouse button
                    self.count = 30 #set count down for click again (rate)


                #render the control screen
                self.user_interface.update(coords, clicked=clicked)
                self.user_interface.render(self.display)


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
                            self.start_point = pygame.time.get_ticks()
                        if event.key == pygame.K_TAB:
                            #reset to start
                            self.scene = 0
                            self.user_interface = self.load_screen(ScreenType.START)
                        if event.key == pygame.K_ESCAPE:
                            self.close_game()

                #display stuff
                #this adds the regular stuff back over the display -- take off for cool effect??
                self.display_2.blit(self.display, (0, 0))

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                #blit display onto screen, use scale to scale display to screen size
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (screenshake_offset))

                #update display, locked at 60 fps
                pygame.display.update()
                self.clock.tick(60)
        


Game().run() #initalizes a Game object, then calls run in same linw