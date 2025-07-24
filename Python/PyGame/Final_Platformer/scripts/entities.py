#Lane Pollock
#Python- pygame
#platformer - July 24 2025 - start
#entity file to hold different entities used in the game

import pygame

#class will handle physics later, takes the game, entity type, position to spawn, and size for entity
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) #to avoid reference 
        self.size = size
        self.velocity =[0, 0] # the derivative of position is velocity, and the derivative of velocity is acceleration

    #to update movement and position
    def update(self, movement=(0, 0)):
        #create a vector to represent how much the entity should move this frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        #update position coords - important to do each dimension seperate
        #update x position based on frame movement
        self.pos[0] += frame_movement[0]
        #update y position based on the frame movement
        self.pos[1] += frame_movement[1]

    #render function, takes a surface
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)