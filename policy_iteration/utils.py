from collections import defaultdict
import numpy as np


class Utils:

    def __init__(self, board_size) -> None:
        self.state_space = defaultdict(int)
        self.board_size = board_size

    def _populate_state_space(self, state, i, j) -> None:
        if(i == self.board_size):
            s = sum(state)
            if(s == 0):
                self.state_space[tuple(state[:])]
            return

        next_i = i+1 if j == self.board_size-1 else i
        next_j = (j+1) % self.board_size

        state[self.board_size*i+j] = 0
        self._populate_state_space(
            state, next_i, next_j)
        state[self.board_size*i+j] = 1
        self._populate_state_space(
            state, next_i, next_j)
        state[self.board_size*i+j] = -1
        self._populate_state_space(
            state, next_i, next_j)

    def populate_state_space(self) -> dict:
        state = [0 for _ in range(self.board_size*self.board_size)]

        self._populate_state_space(state, 0, 0)

        return self.state_space

    def is_valid(self, state, action) -> bool:
        i, j = action[0], action[1]

        if(state[i*self.board_size+j] != 0):
            return False
        return True

    def is_winning_configuration(self, state) -> bool:
        board = np.array(state).reshape(
            self.board_size, self.board_size)
        for i in range(self.board_size):
            if(board[i].sum() == self.board_size):
                return True
            if(board[:, i].sum() == self.board_size):
                return True
        s = 0
        for i in range(self.board_size):
            s += board[i][i]
        if(s == self.board_size):
            return True
        s = 0
        for i in range(self.board_size):
            s += board[i][self.board_size-i-1]
        return s == self.board_size

    def is_losing_configuration(self, state) -> bool:
        board = np.array(state).reshape(
            self.board_size, self.board_size)
        for i in range(self.board_size):
            if(board[i].sum() == -self.board_size):
                return True
            if(board[:, i].sum() == -self.board_size):
                return True
        s = 0
        for i in range(self.board_size):
            s += board[i][i]
        if(s == -self.board_size):
            return True
        s = 0
        for i in range(self.board_size):
            s += board[i][self.board_size-i-1]
        return s == -self.board_size
