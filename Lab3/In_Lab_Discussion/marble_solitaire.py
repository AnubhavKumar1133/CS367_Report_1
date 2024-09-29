class MarbleSolitaire:
    initial_state = [
        [-1,-1, 1, 1, 1,-1,-1],
        [-1,-1, 1, 1, 1,-1,-1],
        [ 1, 1, 1, 1, 1, 1, 1],
        [ 1, 1, 1, 0, 1, 1, 1],
        [ 1, 1, 1, 1, 1, 1, 1],
        [-1,-1, 1, 1, 1,-1,-1],
        [-1,-1, 1, 1, 1,-1,-1]
    ]
    goal_state = [
        [-1,-1, 0, 0, 0,-1,-1],
        [-1,-1, 0, 0, 0,-1,-1],
        [ 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 1, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0],
        [-1,-1, 0, 0, 0,-1,-1],
        [-1,-1, 0, 0, 0,-1,-1]
    ]
    def __init__(self):
        pass
    def is_goal_state(self, state) -> bool:
        return state == self.goal_state
    def display_board(self, curr_state) -> None:
        for row in curr_state:
            print(' '.join(map(str, row)))
        print()
    def is_valid_position(self, row, col) -> bool:
        return 0 <= row < 7 and 0 <= col < 7
    def is_valid_move(self, curr_state, start_row, start_col, end_row, end_col) -> bool:
        # Check if a move is valid
        if not (self.is_valid_position(start_row, start_col) and self.is_valid_position(end_row, end_col)):
            return False      
        if (
            abs(start_row - end_row) == 2 and start_col == end_col and
            curr_state[(start_row + end_row) // 2][start_col] == 1 and
            curr_state[end_row][end_col] == 0
        ) or (
            abs(start_col - end_col) == 2 and start_row == end_row and
            curr_state[start_row][(start_col + end_col) // 2] == 1 and
            curr_state[end_row][end_col] == 0
        ):
            return True
        return False
    def apply_move(self, current_state, start_row, start_col, end_row, end_col):
        if not self.is_valid_move(current_state, start_row, start_col, end_row, end_col):
            print("Invalid move. Please try again.")
            return       
        curr_state = [list(row) for row in current_state]       
        curr_state[start_row][start_col] = 0
        curr_state[(start_row + end_row) // 2][(start_col + end_col) // 2] = 0
        curr_state[end_row][end_col] = 1
        return curr_state
    
    def get_next_states(self, current_state):
        new_states = []
        for row in range(len(current_state)):
                for col in range(len(current_state[0])):
                    if current_state[row][col] == 1:
                        for move in [(row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]:
                            new_row, new_col = move
                            if self.is_valid_move(current_state, row, col, new_row, new_col):
                                new_state = self.apply_move(current_state, row, col, new_row, new_col)
                                new_states.append(new_state)                              
        return new_states

    def man_heuristic(self, state) -> int:
        center_row, center_col = 7 // 2, 7 // 2
        distance = 0
        for row in range(7):
            for col in range(7):
                if state[row][col] == 1:
                    distance += abs(row - center_row) + abs(col - center_col)
        return distance
    
    def marbles_left_heuristic(self, state) -> int:
        marbles = 0
        for row in range(7):
            for col in range(7):
                if state[row][col] == 1:
                    marbles += 1
        return marbles