#this script will hold a couple classes that will work as control screens, and possibly rogue-lite selection screens

import pygame
import sys

red = (255, 0, 0)
yellow = (255, 255, 0)

class ControlScreen:
    def __init__(self):
        #fonts
        self.title_font = pygame.font.SysFont('Arial', 25)
        self.control_font = pygame.font.SysFont('Arial', 20)
        self.desc_font = pygame.font.SysFont('Arial', 10)
        #main controls
        self.control_screen_title = self.title_font.render('CONTROLS', False, (0, 0, 0))
        self.dash = self.control_font.render('DASH', False, red)
        self.move = self.control_font.render('MOVE', False, red)
        self.jump = self.control_font.render('JUMP', False, red)
        #descriptions
        self.desc_dash = self.desc_font.render("X or LSHIFT - Dash through enemies to eliminate them.", False, yellow)
        self.desc_move = self.desc_font.render('A/D or ARROW KEYS - Use to wallslide while in air.', False, yellow)
        self.desc_jump = self.desc_font.render('SPACE or W - You have two jumps.', False, yellow)

    def render(self, surf, game):

        #display stuff
        surf.blit(self.control_screen_title, (game.screen_rect.centerx - self.control_screen_title.get_width()/2, 10))
        surf.blit(self.dash, (game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height())))
        surf.blit(self.move, (game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 2)))
        surf.blit(self.jump, (game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 4)))

        surf.blit(self.desc_dash, (game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height())))
        surf.blit(self.desc_move, (game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 3)))
        surf.blit(self.desc_jump, (game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 5)))