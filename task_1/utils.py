class Utils:

    def __init__(self, board_size) -> None:
        self.state_space = []
        self.board_size = board_size

    def _populate_state_space(self, state, i, j, board_size) -> None:
        if(i == board_size):
            self.state_space.append(state[:])
            return

        next_i = i+1 if j == board_size-1 else i
        next_j = (j+1) % board_size

        state[board_size*i+j] = 0
        self._populate_state_space(
            state, next_i, next_j, board_size)
        state[board_size*i+j] = 1
        self._populate_state_space(
            state, next_i, next_j, board_size)
        state[board_size*i+j] = -1
        self._populate_state_space(
            state, next_i, next_j, board_size)
        state[board_size*i+j] = 0

    def populate_state_space(self) -> list:
        state = [0 for _ in range(self.board_size*self.board_size)]

        self._populate_state_space(state, 0, 0, self.board_size)

        return self.state_space

    def is_valid(self, state, action) -> bool:
        i, j = action[0], action[1]

        if(state[i*self.board_size+j] != 0):
            return False
        return True


# utils = Utils()
# utils.populate_state_space(3)
