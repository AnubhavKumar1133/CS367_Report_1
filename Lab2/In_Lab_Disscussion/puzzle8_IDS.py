import random
from collections import deque

class PuzzleState:
    def __init__(self, board, empty_tile_pos, depth=0, path=None):
        self.board = board
        self.empty_tile_pos = empty_tile_pos
        self.depth = depth
        self.path = path if path is not None else []

    def is_goal(self):
        return self.board == list(range(1, 9)) + [0]

    def get_possible_moves(self):
        moves = []
        x, y = self.empty_tile_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = self.board[:]
                new_board[x * 3 + y], new_board[new_x * 3 + new_y] = new_board[new_x * 3 + new_y], new_board[x * 3 + y]
                moves.append((new_board, (new_x, new_y)))
        return moves

def generate_solvable_puzzle():
    base_board = list(range(1, 9)) + [0]
    random.shuffle(base_board)
    while not is_solvable(base_board):
        random.shuffle(base_board)
    empty_pos = base_board.index(0)
    return base_board, (empty_pos // 3, empty_pos % 3)

def is_solvable(board):
    # Count inversions
    inversions = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] != 0 and board[j] != 0 and board[i] > board[j]:
                inversions += 1
    return inversions % 2 == 0

def depth_limited_search(state, limit):
    if state.is_goal():
        return state.path
    if state.depth == limit:
        return None

    for next_board, empty_pos in state.get_possible_moves():
        new_path = state.path + [next_board]
        new_state = PuzzleState(next_board, empty_pos, state.depth + 1, new_path)
        result = depth_limited_search(new_state, limit)
        if result is not None:
            return result
    return None

def iterative_deepening_search(initial_state):
    for depth in range(1, 14):#adjust the depth from here
        result = depth_limited_search(initial_state, depth)
        if result is not None:
            return result, depth
    return None, None

def main():
    initial_board, empty_pos = generate_solvable_puzzle()
    initial_state = PuzzleState(initial_board, empty_pos)

    print("Generated 8-Puzzle Instance:")
    print(initial_state.board)

    path, depth = iterative_deepening_search(initial_state)

if __name__ == "__main__":
    main()