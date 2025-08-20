#this script will hold a couple classes that will work as control screens, and possibly rogue-lite selection screens

import pygame
import sys

WHITE = (255, 255, 255)
LAVENDER = (150, 120, 182)

class Screens:
    def __init__(self, designation):
        self.designation = designation

        #handle designation
        if self.designation == 'controls':
            #fonts
            self.title_font = pygame.font.SysFont('Arial', 25)
            self.control_font = pygame.font.SysFont('Arial', 20)
            self.desc_font = pygame.font.SysFont('Arial', 10)
            #main controls
            self.control_screen_title = self.title_font.render('CONTROLS', False, (LAVENDER))
            self.dash = self.control_font.render('DASH', False, LAVENDER)
            self.move = self.control_font.render('MOVE', False, LAVENDER)
            self.jump = self.control_font.render('JUMP', False, LAVENDER)
            #descriptions
            self.desc_dash = self.desc_font.render("X or LSHIFT - Dash through enemies to eliminate them.", False, WHITE)
            self.desc_move = self.desc_font.render('A/D or ARROW KEYS - Use to wallslide while in air.', False, WHITE)
            self.desc_jump = self.desc_font.render('SPACE or W - You have two jumps.', False, WHITE)
            #button words
            self.play_button_color = LAVENDER
            self.exit_button_color = LAVENDER
            self.play_button = self.control_font.render('PLAY', False, self.play_button_color)
            self.exit_button = self.control_font.render('EXIT', False, self.exit_button_color)

    
    def update(self, mouse_pos):
        pass
        

    def render(self, surf, game):
        if self.designation == 'controls':
            button_margin = 10
            left_button_rect = pygame.Rect(surf.get_width()/4 - self.play_button.get_width()/2 - button_margin, surf.get_height() - self.play_button.get_height() - button_margin * 2, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            right_button_rect = pygame.Rect(surf.get_width() - self.play_button.get_width() * 2 - button_margin, surf.get_height() - self.play_button.get_height() - button_margin * 2, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            #display stuff
            #screen title
            game.display_2.blit(self.control_screen_title, (game.screen_rect.centerx - self.control_screen_title.get_width()/2, 10))
            #main controls
            surf.blit(self.dash, (game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height())))
            surf.blit(self.move, (game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 2)))
            surf.blit(self.jump, (game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 4)))
            #descriptions
            surf.blit(self.desc_dash, (game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height())))
            surf.blit(self.desc_move, (game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 3)))
            surf.blit(self.desc_jump, (game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 5)))
            #draw rectangles
            #left button
            pygame.draw.rect(surf, (150, 120, 182, 50), left_button_rect, 0)
            #right button
            pygame.draw.rect(surf, (150, 120, 182, 50), right_button_rect, 0)
            #draw the words
            surf.blit(self.exit_button, (left_button_rect.centerx - self.exit_button.get_width()/2, left_button_rect.centery - self.exit_button.get_height()/2))
            surf.blit(self.play_button, (right_button_rect.centerx - self.play_button.get_width()/2, right_button_rect.centery - self.play_button.get_height()/2))




        