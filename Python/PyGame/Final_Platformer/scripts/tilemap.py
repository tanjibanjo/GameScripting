import pygame


NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'} #if no k/v pair, becomes like a set - no duplicates

#creating a class to hold a system of tiles
class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} #keeping most of tiles on a grid is more efficient (dictionary)
        self.offgrid_tiles = [] #list

        #load tilemap
        for i in range(10):
            #tile is represented by the dictionary - type of tile, variant, and position 
            #this one is going left/right I think
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            #other way
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    #pass in a pixel location and get the surrounding tiles to aid in collision
    def tiles_around(self, pos):
        tiles = []
        #convert to grid pos
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)) #// rounds off remainder into int then convert
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap: #check that there is a location
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    #convert all tiles that have physics into pygame.Rect which we can use for collisions - returns the rects created by the tiles
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))

        return rects

    #funtion for rendering tiles using the tilemap    
    def render(self, surf, offset=(0, 0)):
        #for offgrid tiles - render behind the grid since they are more decoration
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        #when iterating over a dict, it returns the keys
        for loc in self.tilemap:
            tile = self.tilemap[loc] # get the location - access with the key

            #render
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        
        

