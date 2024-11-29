import numpy as np

# Grid World dimensions
ROWS, COLS = 4, 3
TERMINAL_STATES = {(4, 3): 1, (4, 2): -1}

# Actions and their probabilities
ACTIONS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
ACTION_PROBS = {"intended": 0.8, "right-angle": 0.1}

# Parameters
DISCOUNT = 0.9  # Gamma
THRESHOLD = 1e-3  # Convergence threshold

def is_valid_state(state):
    """Check if a state is within grid bounds."""
    r, c = state
    return 1 <= r <= ROWS and 1 <= c <= COLS

def get_next_states(state, action):
    """Returns possible next states and their probabilities."""
    if state in TERMINAL_STATES:
        return [(state, 1.0)]  # Terminal state remains the same
    
    intended = (state[0] + action[0], state[1] + action[1])
    right_angle_1 = (state[0] + action[1], state[1] - action[0])  # Perpendicular
    right_angle_2 = (state[0] - action[1], state[1] + action[0])  # Perpendicular
    
    next_states = [(intended, ACTION_PROBS["intended"]),
                   (right_angle_1, ACTION_PROBS["right-angle"]),
                   (right_angle_2, ACTION_PROBS["right-angle"])]
    
    # Stay in place if hitting a wall
    return [(s if is_valid_state(s) else state, p) for s, p in next_states]

def value_iteration_explicit(reward, max_iterations=1000):
    """Performs value iteration explicitly as per the handwritten notes."""
    V = np.zeros((ROWS + 1, COLS + 1))  # Initialize values to 0
    policy = np.full((ROWS + 1, COLS + 1), None)  # Policy map
    
    # Set rewards for terminal states
    for state, r in TERMINAL_STATES.items():
        V[state] = r
    
    iteration = 0
    while True:
        delta = 0  # Track convergence
        new_V = V.copy()
        
        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                state = (r, c)
                
                # Skip terminal states
                if state in TERMINAL_STATES:
                    continue
                
                # Initialize Bellman equation variables
                max_action_value = float('-inf')
                best_action = None
                
                for action_name, action in ACTIONS.items():
                    # Calculate the sum of probabilities × value for the next states
                    next_states = get_next_states(state, action)
                    expected_value = sum(prob * V[s] for s, prob in next_states)
                    
                    # Bellman update for this action
                    action_value = reward + DISCOUNT * expected_value
                    
                    # Store the best action and value
                    if action_value > max_action_value:
                        max_action_value = action_value
                        best_action = action_name
                
                # Update value and policy for this state
                new_V[state] = max_action_value
                policy[state] = best_action
                
                # Compute maximum change in value for convergence
                delta = max(delta, abs(new_V[state] - V[state]))
        
        V = new_V
        iteration += 1
        
        # Check for convergence
        if delta < THRESHOLD or iteration >= max_iterations:
            break
    
    return V, policy

def print_results(V, policy):
    """Displays the value function and policy in a readable format."""
    print("Value Function:")
    for r in range(1, ROWS + 1):
        print(["{:.2f}".format(V[(r, c)]) for c in range(1, COLS + 1)])
    
    print("\nPolicy:")
    for r in range(1, ROWS + 1):
        print([policy[(r, c)] if (r, c) not in TERMINAL_STATES else "T" for c in range(1, COLS + 1)])

# Example usage for r(s) = -0.04
reward1 = -0.04
V1, policy1 = value_iteration_explicit(reward1)
print_results(V1, policy1)

# a) r(s) = -2
reward2 = -2
V2, policy2 = value_iteration_explicit(reward2)
print_results(V2, policy2)

# b) r(s) = 0.1
reward3 = 0.1
V3, policy3 = value_iteration_explicit(reward3)
print_results(V3, policy3)

# c) r(s) = 0.02
reward4 = 0.02
V4, policy4 = value_iteration_explicit(reward4)
print_results(V4, policy4)

# d) r(s) = 1
reward5 = 1
V5, policy5 = value_iteration_explicit(reward5)
print_results(V5, policy5)