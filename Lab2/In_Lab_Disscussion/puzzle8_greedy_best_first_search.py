import heapq
import time
import sys
from typing import List, Tuple, Optional

PuzzleState = List[List[int]]

def print_puzzle(state: PuzzleState) -> None:
    for row in state:
        print(' '.join(str(tile) if tile != 0 else ' ' for tile in row))
    print()

def get_possible_moves(state: PuzzleState) -> List[PuzzleState]:
    x, y = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    moves = []
    
    def swap_and_copy(x1, y1, x2, y2):
        new_state = [row[:] for row in state]
        new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
        return new_state

    if x > 0:
        moves.append(swap_and_copy(x, y, x-1, y))
    if x < 2:
        moves.append(swap_and_copy(x, y, x+1, y))
    if y > 0:
        moves.append(swap_and_copy(x, y, x, y-1))
    if y < 2:
        moves.append(swap_and_copy(x, y, x, y+1))
    return moves

def manhattan_distance(state: PuzzleState, goal_state: PuzzleState) -> int:
    total_distance = 0
    for i, row in enumerate(state):
        for j, tile in enumerate(row):
            if tile != 0:
                goal_index = [(r, row.index(tile)) for r, row in enumerate(goal_state) if tile in row][0]
                goal_row, goal_col = goal_index
                total_distance += abs(i - goal_row) + abs(j - goal_col)
    return total_distance

def greedy_best_first_search(initial_state: PuzzleState, goal_state: PuzzleState) -> Tuple[Optional[List[Tuple[Tuple[int]]]], int, int, float]:
    frontier = []
    heapq.heappush(frontier, (manhattan_distance(initial_state, goal_state), initial_state))
    came_from = {}
    visited = set()
    state_count = 0  
    initial_state_tuple = tuple(tuple(row) for row in initial_state)
    goal_state_tuple = tuple(tuple(row) for row in goal_state)
    came_from[initial_state_tuple] = None
    visited.add(initial_state_tuple)

    start_time = time.time()
    initial_memory = sys.getsizeof(came_from) + sys.getsizeof(visited)

    while frontier:
        _, current_state = heapq.heappop(frontier)
        current_state_tuple = tuple(tuple(row) for row in current_state)

        state_count += 1

        if current_state == goal_state:
            end_memory = sys.getsizeof(came_from) + sys.getsizeof(visited)
            end_time = time.time()
            return reconstruct_path(came_from, current_state_tuple), state_count, end_memory - initial_memory, end_time - start_time

        for next_state in get_possible_moves(current_state):
            next_state_tuple = tuple(tuple(row) for row in next_state)
            if next_state_tuple not in visited:
                visited.add(next_state_tuple)
                heapq.heappush(frontier, (manhattan_distance(next_state, goal_state), next_state))
                came_from[next_state_tuple] = current_state_tuple

    end_memory = sys.getsizeof(came_from) + sys.getsizeof(visited)
    end_time = time.time()
    return None, state_count, end_memory - initial_memory, end_time - start_time

def reconstruct_path(came_from: dict, current_state: Tuple[Tuple[int]]) -> List[Tuple[Tuple[int]]]:
    path = []
    while current_state is not None:
        path.append(current_state)
        current_state = came_from[current_state]
    path.reverse()
    return path

initial_state = [
    [4, 3, 1],
    [2, 8, 0],
    [6, 7, 5]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solution_path, states_visited, memory_used, time_taken = greedy_best_first_search(initial_state, goal_state)

if solution_path:
    print(f"Solution found! Path length: {len(solution_path)}")
    print(f"Number of states visited: {states_visited}")
    print(f"Memory used: {memory_used} bytes")
    print(f"Time taken: {time_taken:.6f} seconds")
else:
    print("No solution found.")