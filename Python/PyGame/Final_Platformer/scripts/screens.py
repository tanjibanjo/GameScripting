#this script will hold a couple classes that will work as control screens, and possibly rogue-lite selection screens

import pygame
import sys
from enum import IntEnum
from scripts.utils import SceneType

WHITE = (255, 255, 255)
LAVENDER = (150, 120, 182)
RED = (255, 20, 0)

#enums for screen type
class ScreenType(IntEnum):
    START = 0
    CONTROLS = 1
    OPTIONS = 2
    GAME_OVER = 3

class Screens:
    def __init__(self, type, game):
        self.type = type
        self.game = game
        self.title_font = pygame.font.SysFont('Arial', 25)

        #handle designation
        if self.type == ScreenType.CONTROLS:
            #fonts
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
            self.objective = self.desc_font.render('Mission: Eliminate the enemies to clear the level.', False, RED)
            #button words
            self.play_button = self.control_font.render('PLAY', False, LAVENDER)
            self.exit_button = self.control_font.render('BACK', False, LAVENDER)
            
            button_margin = 10
            self.left_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 - button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            self.right_button_rect = pygame.Rect(self.game.screen_rect.centerx + button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
       
        if self.type == ScreenType.START:
            #fonts
            self.control_font = pygame.font.SysFont("Arial", 15)
            #title and button words
            self.start_title = self.title_font.render("2d.samurai", False, (150, 120, 182))
            self.play_button = self.control_font.render("PLAY", False, LAVENDER)
            self.exit_button = self.control_font.render('EXIT', False, LAVENDER)
            self.controls_button = self.control_font.render('CONTROLS', False, LAVENDER)
            self.options_button = self.control_font.render('OPTIONS', False, LAVENDER)
            #rects for buttons
            button_margin = 10
            self.exit_button_rect = pygame.Rect(self.game.screen_rect.centerx/8 - button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            self.options_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 + self.options_button.get_width()/2 - button_margin/2 , self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.options_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
            self.controls_button_rect = pygame.Rect(self.game.screen_rect.centerx - button_margin/2, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.controls_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
            self.play_button_rect = pygame.Rect(self.game.screen_rect.centerx + self.controls_button.get_width() + button_margin/2, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
        
        if self.type == ScreenType.GAME_OVER:
            #title and stats stuff
            self.title = self.title_font.render("Mission Passed", False, LAVENDER)
            self.rank = self.title_font.render('RANK:', False, LAVENDER)

    
    def update(self, mouse_pos, clicked=False):
        if self.type == ScreenType.CONTROLS:
            coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)
            #change colors if the player is hovering over the button
            if pygame.Rect.collidepoint(self.left_button_rect, coords): 
                self.exit_button = self.control_font.render('BACK', False, WHITE)
                #handle clicking on button
                if clicked:
                    self.game.scene = SceneType.START
                    self.game.user_interface = self.game.load_screen(ScreenType.START)
            else: #not hovering
                self.exit_button = self.control_font.render('BACK', False, LAVENDER)
            #play button
            if pygame.Rect.collidepoint(self.right_button_rect, coords):
                self.play_button = self.control_font.render('PLAY', False, WHITE)
                if clicked:
                    #reset
                    self.game.level = 0
                    self.game.load_level(self.game.level)
                    self.game.scene = SceneType.GAMEPLAY
                    self.game.start_point = pygame.time.get_ticks()
            else:
                self.play_button = self.control_font.render('PLAY', False, LAVENDER)

        if self.type == ScreenType.START:
            coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)
            #change colors if the player is hovering over the button

            #exit button
            if pygame.Rect.collidepoint(self.exit_button_rect, coords):
                self.exit_button = self.control_font.render('EXIT', False, WHITE)
                #handle clicking
                if clicked:
                    self.game.close_game()
            else:
                self.exit_button = self.control_font.render('EXIT', False, LAVENDER)

            #options button
            if pygame.Rect.collidepoint(self.options_button_rect, coords):
                self.options_button = self.control_font.render('OPTIONS', False, WHITE)
                #handle clicking
                if clicked:
                    pass
            else:
                self.options_button = self.control_font.render('OPTIONS', False, LAVENDER)
            
            #controls button
            if pygame.Rect.collidepoint(self.controls_button_rect, coords):
                self.controls_button = self.control_font.render('CONTROLS', False, WHITE)
                #handle clicking
                if clicked:
                    #switch scene and UI for screen 
                    self.game.scene = SceneType.CONTROLS
                    self.game.user_interface = self.game.load_screen(ScreenType.CONTROLS)
            else:
                self.controls_button = self.control_font.render('CONTROLS', False, LAVENDER)

            #play button
            if pygame.Rect.collidepoint(self.play_button_rect, coords):
                self.play_button = self.control_font.render('PLAY', False, WHITE)
                if clicked:
                    #reset
                    self.game.level = 0
                    self.game.load_level(self.game.level)
                    self.game.scene = SceneType.GAMEPLAY
                    self.game.start_point = pygame.time.get_ticks()
            else:
                self.play_button = self.control_font.render('PLAY', False, LAVENDER)

        if self.type == ScreenType.GAME_OVER:
            pass


    def render(self, surf):
        if self.type == ScreenType.CONTROLS:
            #display stuff
            #screen title
            self.game.display_2.blit(self.control_screen_title, (self.game.screen_rect.centerx - self.control_screen_title.get_width()/2, 10))
            #main controls
            surf.blit(self.dash, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height())))
            surf.blit(self.move, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 2)))
            surf.blit(self.jump, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 4)))
            #descriptions
            surf.blit(self.desc_dash, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height())))
            surf.blit(self.desc_move, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 3)))
            surf.blit(self.desc_jump, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 5)))
            surf.blit(self.objective, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 6)))

            #draw rectangles
            #left button
            pygame.draw.rect(surf, (150, 120, 182, 0), self.left_button_rect, 0)
            #right button
            pygame.draw.rect(surf, (150, 120, 182, 0), self.right_button_rect, 0)
            #draw the words
            surf.blit(self.exit_button, (self.left_button_rect.centerx - self.exit_button.get_width()/2, self.left_button_rect.centery - self.exit_button.get_height()/2))
            surf.blit(self.play_button, (self.right_button_rect.centerx - self.play_button.get_width()/2, self.right_button_rect.centery - self.play_button.get_height()/2))

        if self.type == ScreenType.START:
            button_margin = 10
            #render title
            surf.blit(self.start_title, (self.game.screen_rect.centerx - self.start_title.get_width()/2, 30))
            #draw rects
            pygame.draw.rect(surf, (150, 120, 182, 0), self.exit_button_rect, 0)
            pygame.draw.rect(surf, (150, 120, 182, 0), self.options_button_rect, 0)
            pygame.draw.rect(surf, (150, 120, 182, 0), self.controls_button_rect, 0)
            pygame.draw.rect(surf, (150, 120, 182, 0), self.play_button_rect, 0)

            #draw words
            surf.blit(self.exit_button, (self.exit_button_rect.centerx - self.exit_button.get_width()/2, self.exit_button_rect.centery - self.exit_button.get_height()/2))
            surf.blit(self.options_button, (self.options_button_rect.centerx - self.options_button.get_width()/2, self.options_button_rect.centery - self.options_button.get_height()/2))
            surf.blit(self.controls_button, (self.controls_button_rect.centerx - self.controls_button.get_width()/2, self.controls_button_rect.centery - self.controls_button.get_height()/2))
            surf.blit(self.play_button, (self.play_button_rect.centerx - self.play_button.get_width()/2, self.play_button_rect.centery - self.play_button.get_height()/2))

        if self.type == ScreenType.GAME_OVER:
            #title and rank
            surf.blit(self.title, (self.game.screen_rect.centerx / 8, (self.game.screen_rect.centery / 6)))
            

        