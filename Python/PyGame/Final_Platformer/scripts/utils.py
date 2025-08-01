#Lane Pollock
#Python- pygame
#created - 24 July 2025
#utility file 

import os
import pygame

#this base path just navigates to the images folder, where all the sprites pngs are
BASE_IMG_PATH = 'data/images/'

#loads image, takes path to add to base, returns the loaded image
def load_image(path):
    #convert internal representation of the image in pygame making it more efficient for rendering
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0)) #all our assets have a black background, so this takes black RGB and makes that invisible
    return img

#function will bacth load images
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): # for all images in folder
        images.append(load_image(path + '/' + img_name)) # add the image name to the path- up to now its just directed to the folder

    #return list
    return images

#define animation class
class Animation:
    #restricting ourselves to having the same duration for each frame/sprite
    #simple - ish version of an animation system that is flipping through stuff
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False #set to true if not moving when reaches end
        self.frame = 0 #frame of the game

    #since this is an object, it is returning a reference to this animation object
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    #define update
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) #don't have to account for the index starting at 0 bc of modulo

        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1) #cap our frame to the last frame of anim - then account for index starting at 0 (frame starts at 1)
            if self.frame >= self.img_duration * len(self.images) - 1: 
                self.done = True #set done to true so frame can't go further and loops
    
    #return whatever image corresponds to the frame we are on
    def img(self):
        return self.images[int(self.frame / self.img_duration)]

