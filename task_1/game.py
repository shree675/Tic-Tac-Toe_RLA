# import modules
import pygame
from pygame.locals import *


class Game:

    def __init__(self, board_size):
        # global game_over
        # global winner

        pygame.init()

        self.line_width = 6
        self.board_size = board_size
        self.screen_height = self.board_size*100
        self.screen_width = self.board_size*100
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption('Tic Tac Toe')

        # define colours
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        # define font
        self.font = pygame.font.SysFont(None, 40)

        # define variables
        self.clicked = False
        self.player = 1
        self.pos = (0, 0)
        self.markers = []
        self.game_over = False
        self.winner = 0

        # setup a rectangle for "Play Again" Option
        self.again_rect = Rect(self.screen_width // 2 -
                               80, self.screen_height // 2, 160, 50)

        # create empty board_size x board_size list to represent the grid
        for _ in range(self.board_size):
            self.row = [0] * self.board_size
            self.markers.append(self.row)

    def draw_board(self):
        bg = (255, 255, 210)
        grid = (50, 50, 50)
        self.screen.fill(bg)
        for x in range(1, self.board_size):
            pygame.draw.line(self.screen, grid, (0, 100 * x),
                             (self.screen_width, 100 * x), self.line_width)
            pygame.draw.line(self.screen, grid, (100 * x, 0),
                             (100 * x, self.screen_height), self.line_width)

    def draw_markers(self):
        x_pos = 0
        for x in self.markers:
            y_pos = 0
            for y in x:
                if y == 1:
                    pygame.draw.line(self.screen, self.red, (x_pos * 100 + 15, y_pos * 100 + 15),
                                     (x_pos * 100 + 85, y_pos * 100 + 85), self.line_width)
                    pygame.draw.line(self.screen, self.red, (x_pos * 100 + 85, y_pos * 100 + 15),
                                     (x_pos * 100 + 15, y_pos * 100 + 85), self.line_width)
                if y == -1:
                    pygame.draw.circle(
                        self.screen, self.green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, self.line_width)
                y_pos += 1
            x_pos += 1

    def check_game_over(self):

        x_pos = 0
        for x in self.markers:
            # check columns
            if sum(x) == self.board_size:
                self.winner = 1
                self.game_over = True
            if sum(x) == -self.board_size:
                self.winner = 2
                self.game_over = True
            # check rows
            row_sum = 0
            for i in range(self.board_size):
                row_sum += self.markers[i][x_pos]
            if row_sum == self.board_size:
                self.winner = 1
                self.game_over = True
            if row_sum == -self.board_size:
                self.winner = 2
                self.game_over = True
            x_pos += 1

        # check cross
        cross_sum_d = 0
        cross_sum = 0
        for i in range(self.board_size):
            cross_sum_d += self.markers[i][i]
            cross_sum += self.markers[i][self.board_size-i-1]
        if cross_sum_d == self.board_size or cross_sum == self.board_size:
            self.winner = 1
            self.game_over = True
        if cross_sum_d == -self.board_size or cross_sum == -self.board_size:
            self.winner = 2
            self.game_over = True

        # check for tie
        if self.game_over == False:
            tie = True
            for row in self.markers:
                for i in row:
                    if i == 0:
                        tie = False
            # if it is a tie, then call game over and set winner to 0 (no one)
            if tie == True:
                self.game_over = True
                self.winner = 0

    def draw_game_over(self, winner):

        if winner != 0:
            end_text = "Player " + str(winner) + " wins!"
        elif winner == 0:
            end_text = "You have tied!"

        end_img = self.font.render(end_text, True, self.blue)
        pygame.draw.rect(self.screen, self.green, (self.screen_width // 2 -
                                                   100, self.screen_height // 2 - 60, 200, 50))
        self.screen.blit(end_img, (self.screen_width //
                         2 - 100, self.screen_height // 2 - 50))

        again_text = 'Play Again?'
        again_img = self.font.render(again_text, True, self.blue)
        pygame.draw.rect(self.screen, self.green, self.again_rect)
        self.screen.blit(again_img, (self.screen_width //
                         2 - 80, self.screen_height // 2 + 10))
