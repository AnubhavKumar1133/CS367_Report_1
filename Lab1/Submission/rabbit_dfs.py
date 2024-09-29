from collections import deque

def is_goal(state):
    return state == ['W', 'W', 'W', '_', 'E', 'E', 'E']

def swap(state, i, j):
    """Swaps the elements at indices i and j in the state."""
    new_state = state[:]
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

def generate_successors(state):
    successors = []
    index_of_blank = state.index('_')
    
    # Possible moves: -2 (two steps left), -1 (one step left), 1 (one step right), 2 (two steps right)
    moves = [-2, -1, 1, 2]
    
    for move in moves:
        new_index = index_of_blank + move
        if 0 <= new_index < len(state):
            new_state = swap(state, index_of_blank, new_index)
            successors.append(new_state)
    
    return successors

def dfs(initial_state):
    stack = [(initial_state, [])]
    visited = set()
    visited.add(tuple(initial_state))
    
    while stack:
        current_state, path = stack.pop()
        
        if is_goal(current_state):
            print(f"Length of path to reach the final state: {len(path) + 1}")
            return path + [current_state]
        
        for successor in generate_successors(current_state):
            if tuple(successor) not in visited:
                visited.add(tuple(successor))
                stack.append((successor, path + [current_state]))
    
    return None

def print_solution(solution):
    for step in solution:
        print(step)

# Initial state
initial_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']
solution = dfs(initial_state)

if solution:
    print("Solution found:")
    print_solution(solution)
else:
    print("No solution found.")
