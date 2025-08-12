#Lane Pollock
#Python- pygame
#platformer - July 24 2025 - start
#entity file to hold different entities used in the game

import pygame
import math
import random
from scripts.particle import Particle
from scripts.spark import Spark


#class will handle physics later, takes the game, entity type, position to spawn, and size for entity
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) #to avoid reference 
        self.size = size
        self.velocity =[0, 0] # the derivative of position is velocity, and the derivative of velocity is acceleration
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.speed_mod = 1.7

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        #gravity is universal so we can add to the entity, which the player entity will inherit from
        self.gravity = .1

        #set last movement
        self.last_movement = [0, 0]

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
        self.pos[0] += (frame_movement[0] * self.speed_mod)

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

        self.last_movement = movement

        #min function takes the lesser of the values, so addds .1 then effectively caps the terminal velocity at 5
        self.velocity[1] = min(5, self.velocity[1] + self.gravity)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    #render function, takes a surface
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

#class for enemy
class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        #enemies should just be moving back and forth but not off the sides of the platforms
        #shoot only horizontally
        #timer for walking
        self.walking = 0
    
    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            #scan forward and into ground then pass to the solid check
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - .5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            
            self.walking = max(0, self.walking - 1)

            if not self.walking: #there is only one frame where this fires, before leaving loop
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0): #player is to the left, and looking left
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[1] > 0):
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))

        elif random.random() < 0.01: # has a 1-100 chance of firing, by 60 fps
            self.walking = random.randint(30, 120)
    

        super().update(tilemap, movement=movement)
    
        #movement anims
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        if abs(self.game.player.dashing) >= 50: #we are in dashing mvmnt
            if self.rect().colliderect(self.game.player.rect()): #player hit during dash
                self.game.sfx['hit'].play()
                self.game.screenshake = max(25, self.game.screenshake)
                for i in range(30): #spawn 30 sparks when player is hit
                    angle = random.random() * math.pi * 2 #random angle in a circle
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.game.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * .5, math.sin(angle + math.pi) * speed * .5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True #return true to remove enemy in main

    #modify render function to draw a gun for the enemies
    def render(self, surf, offset=(0, 0)):
        super().render(surf,offset=offset)

        #gun
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))


#player class
class Player(PhysicsEntity): #inherit from entity
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0 #to keep track if in air
        self.jumps = 2 # two jumps before must hit the ground
        self.wall_slide = False
        self.dashing = 0
        self.grounded = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1

        if self.air_time > 150:
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                for i in range(30): #spawn 30 sparks when player is hit
                    angle = random.random() * math.pi * 2 #random angle in a circle
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.game.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * .5, math.sin(angle + math.pi) * speed * .5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
            self.game.dead += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2
            if not self.grounded:
                self.jump(False)


        #reset wallslide every frame - has to be made true
        self.wall_slide = False

        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4: #hitting a wall on the side, and in air
            self.wall_slide = True
            self.air_time = 5 #reset air time so that death doesn't trigger from wall bouncing
            self.velocity[1] = min(self.velocity[1], 0.5) #capping the downward velocity at 0.5
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True

            self.set_action('wall_slide')
        #only check other states if not in wall slide action
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        if abs(self.dashing) in {60, 50}: #at start or end of dash
            for i in range(20): #create 20 particles with random angles and speeds
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5 #.5 to 1
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed] #convert into cartesian coordinates for velocity
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame= random.randint(0, 7)))

        #dashing logic
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        #if we are in first 10 frames of dash, go fast left or right
        #use absolute to remove the direction, keep the velocity - *4 to move faster
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 4
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1 #lower velocity very quickly after dash is over
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0] #set velocity so that particles move with the dash (0-3)
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame= random.randint(0, 7)))
            

        #normalize the horizontal velocity as well, similar to y axis
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0) #bring it slowly to 0
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0) #bring it slowly to 0

    #build on render
    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset) #makes player invisible if frames of anim are higher than 50

    #function to jump - active jump will be true if the button is held down, like in mario
    def jump(self, active_jump):
        if active_jump:
            #update grounded
            self.grounded = False

            #check wallslide first
            if self.wall_slide:
                if self.flip and self.last_movement[0] < 0: #checking if last mvmnt to left
                    self.gravity = .09 #make gravity less if the jump button is being held down
                    self.velocity[0] = 2.8 #push you away from the wall right
                    self.velocity[1] = -2.8 #pushes you up
                    self.air_time = 5 #for anim
                    self.jumps = max(0, self.jumps - 1) #min value is 0 - only use jump if have one left
                    return True
                elif not self.flip and self.last_movement[0] > 0:
                    self.gravity = .09 #make gravity less if the jump button is being held down
                    self.velocity[0] = -2.8 #push you away from the wall right
                    self.velocity[1] = -2.8 #pushes you up
                    self.air_time = 5 #for anim
                    self.jumps = max(0, self.jumps - 1) #min value is 0 - only use jump if have one left
                    return True
            #jumping logic
            elif self.jumps:
                self.gravity = .09 #make gravity less if the jump button is being held down
                self.velocity[1] = -3 #change velocity to move upward
                self.jumps -= 1 #decrements to 0, which ends loop bc it registers as false
                self.air_time = 5 #force to transition to in air animation immediately
                return True
            
        else: #called when release the jump button
            self.gravity = .15
            self.grounded = True

    #function for dash
    def dash(self):
        #set the direction and length of dash, based on which way player is turned
        if not self.dashing:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60