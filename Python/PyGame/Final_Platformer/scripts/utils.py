#Lane Pollock
#Python- pygame
#created - 24 July 2025
#utility file 


import pygame

BASE_IMG_PATH = 'data/images/'

#loads image, takes path to add to base, returns the loaded image
def load_image(path):
    #convert internal representation of the image in pygame making it more efficient for rendering
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0)) #all our assets have a black background, so this takes black RGB and makes that invisible
    return img