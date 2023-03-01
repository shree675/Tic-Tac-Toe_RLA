from utils import Utils
from collections import defaultdict
import random


class Dynamics:

    def __init__(self, board_size) -> None:
        self.transitions = defaultdict(dict)
        self.actions = []
        self.board_size = board_size
        self.state_space = []
        self.utils = Utils(board_size)
        # create a random transition function
        self.gen_transitions()

    def p_trans(self, prev_action, prev_state) -> tuple:
        probability = random.random()
        probability_sum = 0
        for key, value in self.transitions[(tuple(prev_state), tuple(prev_action))].items():
            probability_sum += value
            if(probability_sum >= probability):
                return key

        if(probability_sum == 0):
            return Exception("No transition recorded for the given state and action")

    def gen_transitions(self) -> None:
        self.state_space = self.utils.populate_state_space()

        self.actions = [(i, j) for i in range(self.board_size)
                        for j in range(self.board_size)]

        for state in self.state_space:
            for action in self.actions:
                sum_probabilities = 0

                if(self.utils.is_valid(state, action)):
                    new_state = state[:]
                    new_state[action[0]*self.board_size+action[1]] = 1
                    for k in range(self.board_size**2):
                        i = k//self.board_size
                        j = k % self.board_size

                        if(self.utils.is_valid(new_state, (i, j))):
                            probability = random.randint(
                                1, len(self.state_space))
                            new_state[k] = -1
                            self.transitions[(tuple(state), tuple(
                                action))][tuple(new_state)] = probability
                            sum_probabilities += probability
                            new_state[k] = 0

                    # normalizing the probabilities
                    for key, value in self.transitions[(tuple(state), tuple(action))].items():
                        self.transitions[(tuple(state), tuple(action))][tuple(key)] = value / \
                            sum_probabilities


# (n^4)(3^(n**2)) = 11e9
