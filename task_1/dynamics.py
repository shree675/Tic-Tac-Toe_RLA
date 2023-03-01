from utils import Utils
from collections import defaultdict
import random


class Dynamics:

    def __init__(self, board_size) -> None:
        self.transitions = defaultdict(dict)
        self.board_size = board_size
        self.state_space = []
        self.actions_space = []
        self.utils = Utils(board_size)
        # generating spaces
        self.generate_spaces()

    def p_trans(self, prev_action, prev_state) -> tuple:
        """
        generating probability transition function on-the-fly
        for a given action and state
        """
        prev_state[prev_action[0]*self.board_size+prev_action[1]] = 1
        next_state = defaultdict(dict)

        sum_probabilities = 0
        for (i, j) in self.action_space:
            if(self.utils.is_valid(prev_state, (i, j))):
                probability = random.randint(
                    1, 3**(self.board_size**2))
                k = i*self.board_size+j
                prev_state[k] = -1
                next_state[tuple(prev_state)] = probability
                sum_probabilities += probability
                prev_state[k] = 0

        # normalizing the probabilities
        for key, value in next_state.items():
            next_state[tuple(key)] = value / sum_probabilities

        # choosing the next state based on the set probability distribution
        probability = random.random()
        probability_sum = 0
        for key, value in next_state.items():
            probability_sum += value
            if(probability_sum >= probability):
                return key

        if(probability_sum == 0):
            return Exception("No transition recorded for the given state and action")

    def generate_spaces(self) -> None:
        # uncomment below line to generate state space
        # self.state_space = self.utils.populate_state_space()

        self.action_space = [(i, j) for i in range(self.board_size)
                             for j in range(self.board_size)]
