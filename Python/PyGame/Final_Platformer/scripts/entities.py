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
        self.jump_velocity = -3
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        #gravity is universal so we can add to the entity, which the player entity will inherit from

    #function creates a rect for the entity collision dynamically - so that it's not constantly updating when not needed
    def rect(self):
        return pygame.Rect(*self.pos, *self.size)
    
    #function takes the action string and checks if state has changed then handles
    def set_action(self, action):
        if action != self.action: #only fire if action has changed from what we already have
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy() #creating a new instance of the animation - copy is a user defined function

    #to update movement and position
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False} #reset collisions every frame
        #create a vector to represent how much the entity should move this frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        #update position coords - important to do each dimension seperate
        #update x position based on frame movement
        self.pos[0] += frame_movement[0]

        #collision for x axis
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos): #check for nearby tiles
            if entity_rect.colliderect(rect): #if collision
                if frame_movement[0] > 0: #moving right
                    #snap edges of the entities
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0: #moving left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True

                #update player location
                self.pos[0] = entity_rect.x

        #update y position based on the frame movement
        self.pos[1] += frame_movement[1]

        #collision for y axis
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos): #check for nearby tiles
            if entity_rect.colliderect(rect): #if collision
                if frame_movement[1] > 0: #moving down
                    #snap edges of the entities
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0: #moving up
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True

                #update player location
                self.pos[1] = entity_rect.y

        if movement[0] > 0: #if moving right
            self.flip = False
        if movement[0] < 0: #if moving left
            self.flip = True

        #min function takes the lesser of the values, so addds .1 then effectively caps the terminal velocity at 5
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    #render function, takes a surface
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


#player class
class Player(PhysicsEntity): #inherit from entity
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 #to keep track if in air

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

