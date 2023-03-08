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
        self.optimal_policy = None

        self.generate_spaces()
        self.obtain_optimal_policy()

    def p_trans(self, prev_action, prev_state) -> tuple | Exception | None:
        """
        generating probability transition function on-the-fly
        for a given action and state
        """
        state = (tuple(prev_action[:]), tuple(prev_state))
        if(not state in self.transitions):
            prev_state[prev_action[0]*self.board_size+prev_action[1]] = 1

            sum_probabilities = 0
            for (i, j) in self.action_space:
                if(self.utils.is_valid(prev_state, (i, j))):
                    probability = random.randint(
                        1, 3**(self.board_size**2))
                    k = i*self.board_size+j
                    prev_state[k] = -1
                    self.transitions[state][tuple(prev_state)] = probability
                    sum_probabilities += probability
                    prev_state[k] = 0

            # normalizing the probabilities
            for key, value in self.transitions[state].items():
                self.transitions[state][tuple(
                    key)] = value / sum_probabilities

        # choosing the next state based on the set probability distribution
        probability = random.random()
        probability_sum = 0
        for key, value in self.transitions[state].items():
            probability_sum += value
            if(probability_sum >= probability):
                return key

        if(probability_sum == 0):
            return Exception("No transition recorded for the given state and action")

    def policy(self, state) -> tuple | Exception:
        """
        a deterministic arbitrary policy function
        """
        for (i, j) in self.action_space:
            if(self.utils.is_valid(state, (i, j))):
                return (i, j)

        return Exception("Invalid state")

    def generate_spaces(self) -> None:
        # uncomment below line to generate state space
        # self.state_space = self.utils.populate_state_space()

        self.action_space = [(i, j) for i in range(self.board_size)
                             for j in range(self.board_size)]
        random.shuffle(self.action_space)

    def obtain_optimal_policy(self) -> None:
        """
        policy iteration
        """
        # start with a random policy function
        cur_policy = self.policy
        pass

    def reward(self, prev_state, action) -> int:
        """
        a handcrafted reward function
        based on the number of paths blocked for the opponent
        """
        prev_score = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if(prev_state[i*self.board_size+j] == 1):
                    prev_score += 1
                    break
        for i in range(self.board_size):
            for j in range(self.board_size):
                if(prev_state[j*self.board_size+i] == 1):
                    prev_score += 1
                    break
        for i in range(self.board_size):
            if(prev_state[i*self.board_size+i] == 1):
                prev_score += 1
                break
        for i in range(self.board_size):
            if(prev_state[i*self.board_size+(self.board_size-i-1)] == 1):
                prev_score += 1
                break

        next_state = prev_state[:]
        next_state[action[0]*self.board_size+action[1]] = 1
        new_score = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if(next_state[i*self.board_size+j] == 1):
                    new_score += 1
                    break
        for i in range(self.board_size):
            for j in range(self.board_size):
                if(next_state[j*self.board_size+i] == 1):
                    new_score += 1
                    break
        for i in range(self.board_size):
            if(next_state[i*self.board_size+i] == 1):
                new_score += 1
                break
        for i in range(self.board_size):
            if(next_state[i*self.board_size+(self.board_size-i-1)] == 1):
                new_score += 1
                break

        return (new_score - prev_score)
