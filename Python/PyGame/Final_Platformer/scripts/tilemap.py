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
        
        

