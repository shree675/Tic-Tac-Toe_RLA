from utils import Utils
from collections import defaultdict
import random


class Dynamics:

    def __init__(self, board_size) -> None:
        self.board_size = board_size
        self.actions_space = []
        self.utils = Utils(board_size)
        self.transitions = defaultdict(dict)
        self.state_space = defaultdict(dict)
        self.optimal_policy = defaultdict(tuple)
        self.q = defaultdict(lambda: defaultdict(float))
        self.gamma = 0.9
        self.alpha = 0.7
        self.epsilon = 0.5

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
            return None

    def policy(self, state) -> tuple | None:
        """
        a deterministic arbitrary policy function
        """
        if(tuple(state) in self.optimal_policy):
            return self.optimal_policy[tuple(state)]
        return None

    def generate_spaces(self) -> None:
        # uncomment below line to generate state space
        self.state_space = self.utils.populate_state_space()

        self.action_space = [(i, j) for i in range(self.board_size)
                             for j in range(self.board_size)]
        random.shuffle(self.action_space)

        # initializing the policy
        for state in self.state_space.keys():
            for (i, j) in self.action_space:
                if(self.utils.is_valid(state, (i, j))):
                    self.optimal_policy[state] = (i, j)

    def obtain_optimal_policy(self) -> None:
        """
        epsilon-greedy Q learning
        """
        num_episodes = 20000
        episode = 0
        cur_state = [0 for _ in range(self.board_size**2)]

        while(episode < num_episodes):
            probability = random.random()
            action = None
            if(probability <= self.epsilon or not tuple(cur_state) in self.q):
                # explore
                action = random.choice(self.action_space)
                while(not self.utils.is_valid(cur_state, action)):
                    action = random.choice(self.action_space)
            else:
                # exploit
                max_val = float('-inf')
                for a, q_val in self.q[tuple(cur_state)].items():
                    if(max_val < q_val):
                        max_val = q_val
                        action = a
            if(action is None):
                action = random.choice(self.action_space)
                while(not self.utils.is_valid(cur_state, action)):
                    action = random.choice(self.action_space)

            # opponent's turn
            next_state = self.p_trans(action, cur_state[:])
            reward = (None, True)
            if(next_state is not None):
                reward = self.reward(cur_state, action)
                # update equation
                max_q_val = 0
                if(next_state in self.q):
                    for q_val in self.q[next_state].values():
                        max_q_val = max(max_q_val, q_val)

                self.q[tuple(cur_state)][action] = self.q[tuple(cur_state)][action] + self.alpha * (
                    reward[0] + self.gamma*max_q_val - self.q[tuple(cur_state)][action])

            if(reward[1] == True):
                # reset the board
                next_state = [0 for _ in range(self.board_size**2)]
                episode += 1

            cur_state = list(next_state)[:]

        # setting the optimal policy
        for s in self.q.keys():
            action = None
            max_q_val = float('-inf')
            for a in self.q[s].keys():
                val = self.q[s][a]
                if(max_q_val < val):
                    max_q_val = val
                    action = a
            self.optimal_policy[s] = action  # type: ignore

    def reward(self, prev_state, action) -> tuple:
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

        end_configuration = False
        if(self.utils.is_losing_configuration(next_state)):
            new_score -= 100
            end_configuration = True
        elif(self.utils.is_winning_configuration(next_state)):
            new_score += 100
            end_configuration = True

        return (new_score - prev_score, end_configuration)
