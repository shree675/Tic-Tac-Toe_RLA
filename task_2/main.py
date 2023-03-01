import pygame
import numpy as np
from game import Game
from dynamics import Dynamics

if __name__ == '__main__':

    board_size = 3
    game = Game(board_size)
    dynamics = Dynamics(board_size)

    game.player = 1

    # main loop
    run = True
    while run:
        # draw board and markers first
        game.draw_board()
        game.draw_markers()

        # handle events
        for event in pygame.event.get():
            # handle game exit
            if event.type == pygame.QUIT:
                run = False

        # run new game
        if game.game_over == False:
            cur_state = np.array(game.markers).reshape(
                1, board_size**2).tolist()[0]
            action = dynamics.policy(cur_state)
            cur_state[action[0]*board_size+action[1]] = game.player
            game.markers = np.array(cur_state).reshape(
                board_size, board_size).tolist()
            game.check_game_over()
            if game.game_over == False:
                next_state = dynamics.p_trans(action, cur_state)
                game.markers = np.array(next_state).reshape(
                    board_size, board_size).tolist()
                game.check_game_over()

        # check if game has been won
        if game.game_over == True:
            game.draw_game_over(game.winner)
            # check for mouseclick to see if we clicked on Play Again
            if event.type == pygame.MOUSEBUTTONDOWN and game.clicked == False:
                game.clicked = True
            if event.type == pygame.MOUSEBUTTONUP and game.clicked == True:
                game.clicked = False
                pos = pygame.mouse.get_pos()
                if game.again_rect.collidepoint(pos):
                    # reset variables
                    game.game_over = False
                    game.player = 1
                    game.pos = (0, 0)
                    game.markers = []
                    game.winner = 0
                    # create empty board_size x board_size list to represent the grid
                    for x in range(game.board_size):
                        game.row = [0] * game.board_size
                        game.markers.append(game.row)

        # update display
        pygame.display.update()

    pygame.quit()
