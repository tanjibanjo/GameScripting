import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0, #if those are the neighbors, use 0 
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8
}


NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'} #if no k/v pair, becomes like a set - no duplicates
AUTOTILE_TYPES = {'grass', 'stone'}

#creating a class to hold a system of tiles
class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {} #keeping most of tiles on a grid is more efficient (dictionary)
        self.offgrid_tiles = [] #list

    #function takes a bunch of tiles and gets information about them - can choose to keep or remove as well
    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                #convert to pixels
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

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
    
    #function for saving 
    # a level map 
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        #close
        f.close

    def load(self, path):
        #open file
        f = open(path, 'r')
        #load data
        map_data = json.load(f)
        #close file
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']

    #checking for a solid tile
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size)) #take location and convert to grid location
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc] #returns true or falase if something was found
    
    #convert all tiles that have physics into pygame.Rect which we can use for collisions - returns the rects created by the tiles
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))

        return rects
    
    #function for auto tiling
    def autotile(self):
        #iterate through tilemap
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set() #get the neighbors of the tile
            for shift in [(1, 0), (-1, 0), (0,1), (0, -1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap: #this location exists in the map
                    if self.tilemap[check_loc]['type'] == tile['type']: #check if same group
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]


    #funtion for rendering tiles using the tilemap    
    def render(self, surf, offset=(0, 0)):
        #for offgrid tiles - render behind the grid since they are more decoration
        for tile in self.offgrid_tiles:
           surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))


        #optimized workflow** 
        #use ditionary bc it has O1 lookup time
        #now iterate through the tiles around the player
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                #create the key with the loop indexes
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap: #
                    tile = self.tilemap[loc]
                    #render the tile
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        
        

