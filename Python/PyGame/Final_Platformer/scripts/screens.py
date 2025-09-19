#this script will hold a couple classes that will work as control screens, and possibly rogue-lite selection screens

import pygame
import sys
from enum import IntEnum
from scripts.utils import SceneType
from scripts.entities import PlayerType

WHITE = (255, 255, 255)
LAVENDER = (150, 120, 182)
RED = (255, 20, 0)

#enums for screen type
class ScreenType(IntEnum):
    START = 0
    CONTROLS = 1
    OPTIONS = 2
    GAME_OVER = 3
    LEADERBOARD = 4
    CREDITS = 5
    PLAYER_SELECT = 6

class Screens:
    def __init__(self, type, game):
        self.type = type
        self.game = game

        self.title_font = pygame.font.SysFont('Arial', 25)
        self.med_font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 15)


        #handle designation
        match(self.type):
            case ScreenType.CONTROLS:
                #fonts
                self.desc_font = pygame.font.SysFont('Arial', 10)

                #main controls
                self.control_screen_title = self.title_font.render('controls', False, (LAVENDER))
                self.dash = self.med_font.render('dash', False, LAVENDER)
                self.move = self.med_font.render('move', False, LAVENDER)
                self.jump = self.med_font.render('jump', False, LAVENDER)
                self.slide = self.med_font.render('slide', False, LAVENDER)
                #descriptions
                self.desc_dash = self.desc_font.render("X or LSHIFT - dash through enemies to eliminate them.", False, WHITE)
                self.desc_move = self.desc_font.render('A/D or ARROW KEYS - use to wallslide while in air.', False, WHITE)
                self.desc_jump = self.desc_font.render('SPACE or W - you have two jumps.', False, WHITE)
                self.desc_slide = self.desc_font.render('C or CTRL - slide to avoid projectiles', False, WHITE)
                self.objective = self.desc_font.render('mission: eliminate the enemies to clear the level.', False, RED)
                #button words
                self.play_button = self.med_font.render('play', False, LAVENDER)
                self.exit_button = self.med_font.render('back', False, LAVENDER)
                
                button_margin = 10
                self.left_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 - button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
                self.right_button_rect = pygame.Rect(self.game.screen_rect.centerx + button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            case ScreenType.START:
                #title and button words
                self.start_title = self.title_font.render("samurai41", False, (150, 120, 182))
                self.play_button = self.small_font.render("play", False, LAVENDER)
                self.exit_button = self.small_font.render('exit', False, LAVENDER)
                self.controls_button = self.small_font.render('controls', False, LAVENDER)
                self.options_button = self.small_font.render('leaderboard', False, LAVENDER)
                #rects for buttons
                button_margin = 10
                self.exit_button_rect = pygame.Rect(self.game.screen_rect.centerx/8 - button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
                self.options_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 + self.options_button.get_width()/2 - button_margin/2 , self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.options_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
                self.controls_button_rect = pygame.Rect(self.game.screen_rect.centerx + button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.controls_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
                self.play_button_rect = pygame.Rect(self.game.screen_rect.centerx + self.controls_button.get_width() + button_margin*3, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            case ScreenType.GAME_OVER:
                #title and stats stuff
                self.title = self.title_font.render("mission passed", False, RED)
                self.rank = self.title_font.render('rank:', False, LAVENDER)
                self.stats = ['time:', 'deaths:', 'score:']
                #buttons for play again and exit
                self.play_button = self.med_font.render('play again', False, LAVENDER)
                self.exit_button = self.med_font.render('menu', False, LAVENDER)
                self.credits_button = self.med_font.render('credits', False, LAVENDER)
                #rects
                button_margin = 10
                self.play_button_rect = pygame.Rect(self.game.screen_rect.centerx/4, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
                self.exit_button_rect = pygame.Rect(self.game.screen_rect.centerx + button_margin*2 + self.credits_button.get_width(), self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.exit_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
                self.credits_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 + self.play_button.get_width() + button_margin*3, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.credits_button.get_width() + button_margin, self.play_button.get_height() + button_margin)
            case ScreenType.LEADERBOARD:

                self.stats = []
                self.title = self.title_font.render('recent runs', False, LAVENDER)

                #play and back buttons
                self.play_button = self.med_font.render('play', False, LAVENDER)
                self.exit_button = self.med_font.render('back', False, LAVENDER)

                #rects for play and back
                button_margin = 10
                self.exit_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 - button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
                self.play_button_rect = pygame.Rect(self.game.screen_rect.centerx + button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
                i = len(self.game.save_data) - 1


                #recent runs need to be capped at 6 + best run to keep from words going off the screen
                if len(self.game.save_data) > 0 and len(self.game.save_data) < 7:
                    #get best run and save those stats first
                    best_run = self.get_best_run()
                    self.stats.append(str(best_run.deaths))
                    self.stats.append(str(best_run.time))
                    self.stats.append(str(best_run.score))
                    self.stats.append(str(best_run.rank))
                    #now save the rest
                    for save in self.game.save_data:
                        self.stats.append(str(save.deaths))
                        self.stats.append(str(save.time))
                        self.stats.append(str(save.score))
                        self.stats.append(str(save.rank))
                elif len(self.game.save_data) > 6:
                    #get best run and save those stats first
                    best_run = self.get_best_run()
                    self.stats.append(str(best_run.deaths))
                    self.stats.append(str(best_run.time))
                    self.stats.append(str(best_run.score))
                    self.stats.append(str(best_run.rank))
                    #now get the most recent 6 runs - only append those
                    for save in self.game.save_data:
                        if i < 6:
                            self.stats.append(str(save.deaths))
                            self.stats.append(str(save.time))
                            self.stats.append(str(save.score))
                            self.stats.append(str(save.rank))
                        else:
                            pass
                        i-=1

                else: #0 data
                    self.stats = ['no previous runs recorded']
            case ScreenType.CREDITS:
                self.title = self.title_font.render('credits', False, WHITE)

                #play and back buttons
                self.play_button = self.med_font.render('play', False, LAVENDER)
                self.exit_button = self.med_font.render('back', False, LAVENDER)

                #rects for play and back
                button_margin = 10
                self.exit_button_rect = pygame.Rect(self.game.screen_rect.centerx/4 - button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
                self.play_button_rect = pygame.Rect(self.game.screen_rect.centerx + button_margin, self.game.screen_rect.centery + self.play_button.get_height() + button_margin, self.play_button.get_width() + button_margin * 2, self.play_button.get_height() + button_margin)
            case ScreenType.PLAYER_SELECT:
                self.xt_small = pygame.font.SysFont('Arial', 10)

                self.title = self.title_font.render('choose skillset', False, LAVENDER)
                self.desc = self.xt_small.render('status is increased when enemies are eliminated without dying', False, RED)

                self.player_btn1 = self.med_font.render('rogue', False, LAVENDER)

                self.player_btn2 = self.med_font.render('assassin', False, LAVENDER)

                self.descriptions = ['methodical and percise', 'slower movement, three jumps', 'builds momentum - dash length grows', 'fast and ferocious', 'quicker movement, short attack', 'builds intensity - speed increases']

                button_margin = 10
                
                self.rogue_rect = pygame.Rect(self.game.screen_rect.centerx/4 + button_margin, self.game.screen_rect.centery/4 + self.player_btn1.get_height() - button_margin, self.player_btn1.get_width() + button_margin, self.player_btn1.get_height() + button_margin)
                self.assassin_rect = pygame.Rect(self.game.screen_rect.centerx + (self.game.screen_rect.centerx/3) - button_margin, self.game.screen_rect.centery/4 + self.player_btn1.get_height() - button_margin, self.player_btn1.get_width() + button_margin, self.player_btn1.get_height() + button_margin)

                self.r = False
                self.a = False #these are for the player selection descriptions

            case _:
                pass
    
    def get_best_run(self):
        stats = []
        i=0
        for save in self.game.save_data:
            stats.append(save.score)
            i+=1 #lcv, and key to serve as the index as well
        #sort stats in descending order, first element will be the highest score
        stats = sorted(stats, reverse=True)
        best_score = stats[0]

        for save in self.game.save_data:
            if best_score == save.score:
                return save

    def update(self, mouse_pos, clicked=False):
        match(self.type):
            case ScreenType.CONTROLS:
                if self.game.large_screen:
                    coords = (mouse_pos[0] / 3, mouse_pos[1] / 3)
                else:
                    coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)
                #change colors if the player is hovering over the button
                if pygame.Rect.collidepoint(self.left_button_rect, coords): 
                    self.exit_button = self.med_font.render('back', False, WHITE)
                    #handle clicking on button
                    if clicked:
                        self.game.scene = SceneType.START
                        self.game.user_interface = self.game.load_screen(ScreenType.START)
                else: #not hovering
                    self.exit_button = self.med_font.render('back', False, LAVENDER)
                #play button
                if pygame.Rect.collidepoint(self.right_button_rect, coords):
                    self.play_button = self.med_font.render('play', False, WHITE)
                    if clicked:
                        self.game.user_interface = self.game.load_screen(ScreenType.PLAYER_SELECT)
                else:
                    self.play_button = self.med_font.render('play', False, LAVENDER)
            case ScreenType.START:
                if self.game.large_screen:
                    coords = (mouse_pos[0] / 3, mouse_pos[1] / 3)
                else:
                    coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)
                #change colors if the player is hovering over the button

                #exit button
                if pygame.Rect.collidepoint(self.exit_button_rect, coords):
                    self.exit_button = self.small_font.render('exit', False, WHITE)
                    #handle clicking
                    if clicked:
                        self.game.close_game()
                else:
                    self.exit_button = self.small_font.render('exit', False, LAVENDER)

                #options button
                if pygame.Rect.collidepoint(self.options_button_rect, coords):
                    self.options_button = self.small_font.render('leaderboard', False, WHITE)
                    #handle clicking
                    if clicked:
                        #switch scene to utility and ui to leaderboard
                        self.game.scene = SceneType.UTILITY
                        self.game.user_interface = self.game.load_screen(ScreenType.LEADERBOARD)
                else:
                    self.options_button = self.small_font.render('leaderboard', False, LAVENDER)
                
                #controls button
                if pygame.Rect.collidepoint(self.controls_button_rect, coords):
                    self.controls_button = self.small_font.render('controls', False, WHITE)
                    #handle clicking
                    if clicked:
                        #switch scene and UI for screen 
                        self.game.scene = SceneType.UTILITY
                        self.game.user_interface = self.game.load_screen(ScreenType.CONTROLS)
                else:
                    self.controls_button = self.small_font.render('controls', False, LAVENDER)

                #play button
                if pygame.Rect.collidepoint(self.play_button_rect, coords):
                    self.play_button = self.small_font.render('play', False, WHITE)
                    if clicked:
                        #reset
                        #self.game.reset(new_run=True)
                        self.game.scene = SceneType.UTILITY
                        self.game.user_interface = self.game.load_screen(ScreenType.PLAYER_SELECT)
                else:
                    self.play_button = self.small_font.render('play', False, LAVENDER)
            case ScreenType.GAME_OVER:
                if self.game.large_screen:
                    coords = (mouse_pos[0] / 3, mouse_pos[1] / 3)
                else:
                    coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)
                #play again button
                if pygame.Rect.collidepoint(self.play_button_rect, coords):
                    self.play_button = self.med_font.render('play again', False, WHITE)
                    if clicked:
                        #save the run and then reset to start again, game is saved before this screen
                        self.game.scene = SceneType.UTILITY
                        self.game.user_interface = self.game.load_screen(ScreenType.PLAYER_SELECT)
                else:
                    self.play_button = self.med_font.render('play again', False, LAVENDER)

                #credits button
                if pygame.Rect.collidepoint(self.credits_button_rect, coords):
                    self.credits_button = self.med_font.render('credits', False, WHITE)
                    if clicked:
                        #switch scene to utility and ui to credits
                        self.game.scene = SceneType.UTILITY
                        self.game.user_interface = self.game.load_screen(ScreenType.CREDITS)
                else:
                    self.credits_button = self.med_font.render('credits', False, LAVENDER)

                #exit button
                if pygame.Rect.collidepoint(self.exit_button_rect, coords):
                    self.exit_button = self.med_font.render('menu', False, WHITE)
                    if clicked:
                        #close the game
                        self.game.reset(new_run=False)
                else:
                    self.exit_button = self.med_font.render('menu', False, LAVENDER)
            case ScreenType.LEADERBOARD:
                if self.game.large_screen:
                    coords = (mouse_pos[0] / 3, mouse_pos[1] / 3)
                else:
                    coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)

                #handle color change for mouse hover
                if pygame.Rect.collidepoint(self.exit_button_rect, coords):
                    self.exit_button = self.med_font.render('back', False, WHITE)
                    #handle clicking
                    if clicked:
                        self.game.scene = SceneType.START
                        self.game.user_interface = self.game.load_screen(ScreenType.START)
                else:
                    self.exit_button = self.med_font.render('back', False, LAVENDER)
            #play button
                if pygame.Rect.collidepoint(self.play_button_rect, coords):
                    self.play_button = self.med_font.render('play', False, WHITE)
                    #clicking
                    if clicked:
                        self.game.user_interface = self.game.load_screen(ScreenType.PLAYER_SELECT)
                else:
                    self.play_button = self.med_font.render('play', False, LAVENDER)
            case ScreenType.CREDITS:
                if self.game.large_screen:
                    coords = (mouse_pos[0] / 3, mouse_pos[1] / 3)
                else:
                    coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)

                #handle color change for mouse hover
                if pygame.Rect.collidepoint(self.exit_button_rect, coords):
                    self.exit_button = self.med_font.render('back', False, WHITE)
                    #handle clicking
                    if clicked:
                        self.game.scene = SceneType.GAME_OVER
                        self.game.user_interface = self.game.load_screen(ScreenType.GAME_OVER)
                else:
                    self.exit_button = self.med_font.render('back', False, LAVENDER)
                #play button
                if pygame.Rect.collidepoint(self.play_button_rect, coords):
                    self.play_button = self.med_font.render('play', False, WHITE)
                    #clicking
                    if clicked:
                        self.game.scene = SceneType.UTILITY
                        self.game.user_interface = self.game.load_screen(ScreenType.PLAYER_SELECT)
                else:
                    self.play_button = self.med_font.render('play', False, LAVENDER)
            case ScreenType.PLAYER_SELECT:
                if self.game.large_screen:
                    coords = (mouse_pos[0] / 3, mouse_pos[1] / 3)
                else:
                    coords = (mouse_pos[0] / 2, mouse_pos[1] / 2)

                if pygame.Rect.collidepoint(self.rogue_rect, coords):
                    self.player_btn1 = self.med_font.render('rogue', False, WHITE)
                    self.r = True
                    if clicked:
                        self.game.player.player_class = PlayerType.ROGUE
                        self.game.reset(True)
                else:
                    self.player_btn1 = self.med_font.render('rogue', False, LAVENDER)
                    self.r = False

                if pygame.Rect.collidepoint(self.assassin_rect, coords):
                    self.player_btn2 = self.med_font.render('assassin', False, WHITE)
                    self.a = True
                    if clicked:
                        self.game.player.player_class = PlayerType.ASSASSIN
                        self.game.reset(True)
                else:
                    self.player_btn2 = self.med_font.render('assassin', False, LAVENDER)
                    self.a = False

            case _:
                pass

    def render(self, surf):
        match(self.type):
            case ScreenType.CONTROLS:
                margin = 20
                #display stuff
                #screen title
                self.game.display_2.blit(self.control_screen_title, (self.game.screen_rect.centerx - self.control_screen_title.get_width()/2, self.control_screen_title.get_height() - margin))
                #main controls
                surf.blit(self.dash, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height()) - margin))
                surf.blit(self.move, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 2) - margin))
                surf.blit(self.jump, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 4) - margin))
                surf.blit(self.slide, (self.game.screen_rect.centerx / 4, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 6) - margin))

                #descriptions
                surf.blit(self.desc_dash, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height()) - margin))
                surf.blit(self.desc_move, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 3) - margin))
                surf.blit(self.desc_jump, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 5) - margin))
                surf.blit(self.desc_slide, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 7) - margin))

                surf.blit(self.objective, (self.game.screen_rect.centerx / 4 + 5, (15 + self.control_screen_title.get_height() + self.dash.get_height() * 7) - margin * .5))
                #draw the words
                surf.blit(self.exit_button, (self.left_button_rect.centerx - self.exit_button.get_width()/2, self.left_button_rect.centery - self.exit_button.get_height()/2))
                surf.blit(self.play_button, (self.right_button_rect.centerx - self.play_button.get_width()/2, self.right_button_rect.centery - self.play_button.get_height()/2))

            case ScreenType.START:
                button_margin = 10
                #render title
                surf.blit(self.start_title, (self.game.screen_rect.centerx - self.start_title.get_width()/2, 30))

                #draw words
                surf.blit(self.exit_button, (self.exit_button_rect.centerx - self.exit_button.get_width()/2, self.exit_button_rect.centery - self.exit_button.get_height()/2))
                surf.blit(self.options_button, (self.options_button_rect.centerx - self.options_button.get_width()/2, self.options_button_rect.centery - self.options_button.get_height()/2))
                surf.blit(self.controls_button, (self.controls_button_rect.centerx - self.controls_button.get_width()/2, self.controls_button_rect.centery - self.controls_button.get_height()/2))
                surf.blit(self.play_button, (self.play_button_rect.centerx - self.play_button.get_width()/2, self.play_button_rect.centery - self.play_button.get_height()/2))

            case ScreenType.GAME_OVER:
                #title and rank
                surf.blit(self.title, (self.game.screen_rect.centerx / 8, (self.game.screen_rect.centery / 6)))
                surf.blit(self.rank, (self.game.screen_rect.centerx + self.rank.get_width()/2, self.game.screen_rect.centery/2))
                surf.blit(self.title_font.render(self.game.get_rank(), False, RED), (self.game.screen_rect.centerx + self.rank.get_width() *1.5, self.game.screen_rect.centery/2)) 
                #stat titles rendered in a for for ease
                i = 0
                for stat in self.stats:
                    i+=1 #increment multiplier for height
                    surf.blit(self.small_font.render(stat, False, WHITE), (self.game.screen_rect.centerx + self.rank.get_width()/2, self.game.screen_rect.centery/2 + self.title.get_height() * i))
                #now render actual stats
                surf.blit(self.small_font.render((self.game.formatted_time), False, RED), (self.game.screen_rect.centerx + self.rank.get_width()/2 + self.rank.get_width(), self.game.screen_rect.centery/2 + self.title.get_height()))
                surf.blit(self.small_font.render(str(self.game.player_deaths), False, RED), (self.game.screen_rect.centerx + self.rank.get_width()/2 + self.rank.get_width() + 10, self.game.screen_rect.centery/2 + self.title.get_height() * 2))
                surf.blit(self.small_font.render(str(int(self.game.player_total_score)), False, RED), (self.game.screen_rect.centerx + self.rank.get_width()/2 + self.rank.get_width(), self.game.screen_rect.centery/2 + self.title.get_height()* 3))
                
                #buttons
                surf.blit(self.exit_button, (self.exit_button_rect.centerx - self.exit_button.get_width()/2, self.exit_button_rect.centery - self.exit_button.get_height()/2))
                surf.blit(self.play_button, (self.play_button_rect.centerx - self.play_button.get_width()/2, self.play_button_rect.centery - self.play_button.get_height()/2))
                surf.blit(self.credits_button, (self.credits_button_rect.centerx - self.credits_button.get_width()/2, self.credits_button_rect.centery - self.play_button.get_height()/2))
            
            case ScreenType.LEADERBOARD:
                button_margin=10
                surf.blit(self.title, (self.game.screen_rect.centerx - self.title.get_width()/2, self.title.get_height()/2))

                xt_small = pygame.font.SysFont('Arial', 12)

                #draw the play and exit words
                surf.blit(self.exit_button, (self.exit_button_rect.centerx - self.exit_button.get_width()/2, self.exit_button_rect.centery - self.exit_button.get_height()/2))
                surf.blit(self.play_button, (self.play_button_rect.centerx - self.play_button.get_width()/2, self.play_button_rect.centery - self.play_button.get_height()/2))
                #to use for spacing
                sm_btn = self.small_font.render('run 1', False, LAVENDER)
                
                #blit the stat header, (deaths, time(sec), score, Rank)
                header = ['deaths', 'time', 'score', 'rank']
                j = 0
                for heading in header:
                    surf.blit(xt_small.render(heading, False, WHITE), (self.game.screen_rect.centerx/2 - button_margin + (self.exit_button.get_width() + button_margin) * j, self.title.get_height() + sm_btn.get_height() + button_margin))
                    j+=1
                #blit the stats for the previous runs, if any
                
                j= -1 #to keep track of how many elements in each row
                i=2 #for the height

                for stat in self.stats:

                    j+=1 #0 to start
                    if (j%4) == 0: # will be true when j = multiples of 4, how many stats we have
                        i+=1 #increment to the next row down
                        j = 0 #reset the column location
                    if i < 4:
                        surf.blit(self.small_font.render(stat, False, RED), (self.game.screen_rect.centerx/2 - button_margin + (self.exit_button.get_width() + button_margin) * j, self.title.get_height() + sm_btn.get_height() * i))
                    else:
                        surf.blit(self.small_font.render(stat, False, WHITE), (self.game.screen_rect.centerx/2 - button_margin + (self.exit_button.get_width() + button_margin) * j, self.title.get_height() + sm_btn.get_height() * i))
                    
            case ScreenType.CREDITS:
                surf.blit(self.title, (self.game.screen_rect.centerx - self.title.get_width()/2, self.title.get_height()/2))

                #draw the words
                surf.blit(self.exit_button, (self.exit_button_rect.centerx - self.exit_button.get_width()/2, self.exit_button_rect.centery - self.exit_button.get_height()/2))
                surf.blit(self.play_button, (self.play_button_rect.centerx - self.play_button.get_width()/2, self.play_button_rect.centery - self.play_button.get_height()/2))

            case ScreenType.PLAYER_SELECT:
                #title
                surf.blit(self.title, (self.game.screen_rect.centerx - self.title.get_width()/2, self.title.get_height()/2))

                surf.blit(self.desc, (self.game.screen_rect.centerx - self.desc.get_width()/2, self.title.get_height()/2 + self.title.get_height()))
                
                #choices
                surf.blit(self.player_btn1, (self.rogue_rect.centerx - self.player_btn1.get_width()/2, self.rogue_rect.centery - self.player_btn1.get_height()/2))
                surf.blit(self.player_btn2, (self.assassin_rect.centerx - self.player_btn2.get_width()/2, self.assassin_rect.centery - self.player_btn2.get_height()/2))

                #descriptions - three for each 
                i = 0 #keep track of which item in list
                j = 0 #for the spacing

                button_margin = 10

                for desc in self.descriptions:
                    if i == 2 or i == 5:
                        surface = self.small_font.render(desc, False, RED)
                    else:
                        surface = self.small_font.render(desc, False, WHITE)

                    #blit the item to underneath the skillset
                    if self.a:
                        if i > 2:
                            surf.blit(surface, (self.game.screen_rect.centerx - surface.get_width()/2, self.rogue_rect.centery + self.player_btn1.get_height() + (self.player_btn1.get_height() * j)))
                        else:
                            pass
                    elif self.r:
                        if i < 3:
                            surf.blit(surface, (self.game.screen_rect.centerx - surface.get_width()/2, self.assassin_rect.centery + self.player_btn1.get_height() + (self.player_btn2.get_height() * j)))
                        else:
                            pass
                    i+=1 #increment i for height of descs to increment as well'
                    j+=1
                    if(i == 3):
                        j = 0
                

            case _:
                pass