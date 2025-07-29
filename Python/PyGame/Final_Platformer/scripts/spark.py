

import math
import pygame

class Spark():
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

    def update(self):
        #speed and angle together make like a vector
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        #spark slows and shrinks over time till it dissapears
        self.speed = max(0, self.speed - 1)
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        render_points = [
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi * .5) * self.speed * .5 - offset[0], self.pos[1] + math.sin(self.angle + math.pi * .5) * self.speed * .5 - offset[1]),
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),
            (self.pos[0] + math.cos(self.angle - math.pi * .5) * self.speed * .5 - offset[0], self.pos[1] + math.sin(self.angle - math.pi * .5) * self.speed * .5 - offset[1]),
        ]
        

        pygame.draw.polygon(surf, (255, 255, 255), render_points) #this creates a polygon