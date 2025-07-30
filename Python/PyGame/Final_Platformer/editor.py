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
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners')
        }

        
        #movement attributes for camera
        self.movement = [False, False, False, False]

        #tile map
        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load('data/maps/new_map.json')
        except FileNotFoundError:
            pass

        #camera stuff
        self.scroll = [0, 0]

        #convert assets to a list - which gives the key values
        self.tile_list = list(self.assets) 
        self.tile_group = 0 #which group -decor, grass, etc
        self.tile_variant = 0 #which tile within that group

        #input stuff
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.on_grid = True


    def run(self):
        while True:
            #fill background
            self.display.fill((0, 0, 0))

            #scroll calc for moving camera - 
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2 #right - left
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2 #down, up

            #offset, truncated
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #rendering our tile map
            self.tilemap.render(self.display, offset=render_scroll)
            
            #set the current image in the editor
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(170) #semi transparent - 0-255 range

            #get mouse position
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) 
            #changes coordinates of mouse position to the tile scale -important to align to grid
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))


            if self.on_grid:
                #converting back to pixel format then accounting for the offset - important to align to the grid
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            #converting index selection to the string names - this is for placing new tiles into the level
            if self.clicking and self.on_grid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            
            #this will be for deleting tiles from the level
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap: #this place exists
                    del self.tilemap.tilemap[tile_loc]

                #logic for deleting offgrid tiles
                for tile in self.tilemap.offgrid_tiles.copy(): #use a copy so we dont use reference
                    tile_img = self.assets[tile['type']][tile['variant']] #get the image
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos): #if tile collides with mouse
                        self.tilemap.offgrid_tiles.remove(tile)

            #sending out current tile to the screen
            self.display.blit(current_tile_img, (5, 5))

            #handle events - left and right movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        #scroll between groups of decor
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]]) # loops through the variants
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]]) # loops through the variants
                    else:
                        #scroll between groups of decor
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list) # loops through the groups
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list) # loops through the groups
                            self.tile_variant = 0
                #update variables based on mouse state
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                #movement inputs for up and down - uses keyboard keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid #flips every time 
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('data/maps/new_map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            #blit display onto screen, use scale to scale display to screen size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            #update display, locked at 60 fps
            pygame.display.update()
            self.clock.tick(60)

Editor().run() #initalizes a Game object, then calls run in same line