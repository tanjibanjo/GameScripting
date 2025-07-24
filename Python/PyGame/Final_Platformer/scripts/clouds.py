import random

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos) #convert to copy - not reference
        self.img = img # dont convert or anything to use reference because not changing
        self.speed = speed
        self.depth = depth
    
    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth) #if depth is 0.5, cloud will move less since it is further away - easy paralax effect
        surf.blit(self.img, (render_pos[0]))