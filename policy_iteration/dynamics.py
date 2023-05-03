from utils import Utils
from collections import defaultdict
import random
import copy


class Dynamics:

    def __init__(self, board_size) -> None:
        self.transitions = defaultdict(dict)
        self.board_size = board_size
        self.state_space = defaultdict(dict)
        self.actions_space = []
        self.utils = Utils(board_size)
        self.optimal_policy = defaultdict(tuple)
        self.gamma = 0.8

        self.generate_spaces()
        self.obtain_optimal_policy()

    def p_trans(self, prev_action, prev_state) -> tuple | Exception | None:
        """
        generating probability transition function on-the-fly
        for a given action and state
        """
        state = (tuple(prev_action), tuple(prev_state[:]))
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

    def policy(self, state) -> tuple | None:
        """
        a deterministic policy function
        """
        if(tuple(state) in self.optimal_policy):
            return self.optimal_policy[tuple(state)]
        return None

    def generate_spaces(self) -> None:
        self.state_space = self.utils.populate_state_space()

        self.action_space = [(i, j) for i in range(self.board_size)
                             for j in range(self.board_size)]
        # random.shuffle(self.action_space)

        # initializing the policy
        for state in self.state_space.keys():
            for (i, j) in self.action_space:
                if(self.utils.is_valid(state, (i, j))):
                    self.optimal_policy[state] = (i, j)

    def obtain_optimal_policy(self) -> None:
        """
        policy iteration
        """
        num_iterations = 0
        # start with a random policy function
        cur_policy = self.policy
        value = defaultdict(float)

        while True:
            num_iterations += 1
            new_value = defaultdict(float)
            pi = defaultdict(tuple)
            # policy evaluation
            for k in range(10):
                for s, _ in self.state_space.items():
                    action = cur_policy(s)
                    if(action is None):
                        continue
                    new_value[s] = self.reward(list(s), action)
                    if(k == 0):
                        __ = self.p_trans(action, list(s))
                    state = (tuple(action), s)
                    product_sum = 0
                    if(state in self.transitions):
                        for s_prime, probability in self.transitions[state].items():
                            product_sum += probability*value[s_prime]
                    new_value[s] += self.gamma*product_sum
                value = copy.deepcopy(new_value)
            # policy improvement
            for s, _ in self.state_space.items():
                best_action_val = float('-inf')
                best_action = None
                for action in self.action_space:
                    if(not self.utils.is_valid(s, action)):
                        continue
                    action_val = self.reward(list(s), action)
                    state = (tuple(action), s)
                    product_sum = 0
                    if(state in self.transitions):
                        for s_prime, probability in self.transitions[state].items():
                            product_sum += probability*value[s_prime]
                    action_val += self.gamma*product_sum
                    if(best_action_val < action_val):
                        best_action_val = action_val
                        best_action = action
                pi[s] = best_action   # type: ignore

            if(self.optimal_policy == pi):
                break
            self.optimal_policy = copy.deepcopy(pi)

        print('Number of policy iterations: {}'.format(num_iterations))

    def reward(self, prev_state, action) -> float:
        """
        a handcrafted reward function
        based on the number of paths blocked for the opponent

        one step average reward is the same as this
        reward function since this function does not
        depend on the next state, it purely evaluates
        the action taken by the policy
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

        if(self.utils.is_losing_configuration(next_state)):
            new_score -= 100
        elif(self.utils.is_winning_configuration(next_state)):
            new_score += 100

        return (new_score - prev_score)
