import numpy as np
from scipy.stats import poisson

# Constants
MAX_BIKES = 20
MAX_MOVE = 5
RENTAL_INCOME = 10
MOVE_COST = 2
DISCOUNT = 0.9

# Poisson distribution means
RENTAL_MEANS = [3, 4]
RETURN_MEANS = [3, 2]

# Initialize value function and policy
states = [(i, j) for i in range(MAX_BIKES + 1) for j in range(MAX_BIKES + 1)]
value_function = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1))
policy = np.zeros((MAX_BIKES + 1, MAX_BIKES + 1), dtype=int)

# Poisson probabilities cache
poisson_cache = {}

def poisson_probability(n, mean):
    """Compute Poisson probability with caching."""
    key = (n, mean)
    if key not in poisson_cache:
        poisson_cache[key] = poisson.pmf(n, mean)
    return poisson_cache[key]

def expected_return(state, action, value_function):
    """Calculate the expected return for a given state and action."""
    s1, s2 = state
    s1 = min(s1 - action, MAX_BIKES)
    s2 = min(s2 + action, MAX_BIKES)

    # Moving cost
    moving_cost = MOVE_COST * abs(action)
    expected_value = -moving_cost

    # Iterate over possible rental requests
    for rentals1 in range(MAX_BIKES + 1):
        for rentals2 in range(MAX_BIKES + 1):
            prob_rentals = poisson_probability(rentals1, RENTAL_MEANS[0]) * \
                           poisson_probability(rentals2, RENTAL_MEANS[1])

            # Rentals
            actual_rentals1 = min(s1, rentals1)
            actual_rentals2 = min(s2, rentals2)
            reward = (actual_rentals1 + actual_rentals2) * RENTAL_INCOME

            # Bikes left after rentals
            bikes1 = s1 - actual_rentals1
            bikes2 = s2 - actual_rentals2

            # Iterate over returns
            for returns1 in range(MAX_BIKES + 1):
                for returns2 in range(MAX_BIKES + 1):
                    prob_returns = poisson_probability(returns1, RETURN_MEANS[0]) * \
                                   poisson_probability(returns2, RETURN_MEANS[1])

                    # Update bike counts
                    new_s1 = min(bikes1 + returns1, MAX_BIKES)
                    new_s2 = min(bikes2 + returns2, MAX_BIKES)

                    # Transition probability
                    prob = prob_rentals * prob_returns
                    expected_value += prob * (reward + DISCOUNT * value_function[new_s1, new_s2])

    return expected_value

def policy_iteration():
    """Perform policy iteration to find the optimal policy."""
    global policy, value_function
    while True:
        # Policy evaluation
        while True:
            delta = 0
            for s1 in range(MAX_BIKES + 1):
                for s2 in range(MAX_BIKES + 1):
                    v = value_function[s1, s2]
                    value_function[s1, s2] = expected_return((s1, s2), policy[s1, s2], value_function)
                    delta = max(delta, abs(v - value_function[s1, s2]))
            if delta < 1e-4:
                break

        # Policy improvement
        policy_stable = True
        for s1 in range(MAX_BIKES + 1):
            for s2 in range(MAX_BIKES + 1):
                old_action = policy[s1, s2]
                action_returns = []
                for action in range(-MAX_MOVE, MAX_MOVE + 1):
                    if 0 <= s1 - action <= MAX_BIKES and 0 <= s2 + action <= MAX_BIKES:
                        action_returns.append(expected_return((s1, s2), action, value_function))
                    else:
                        action_returns.append(float('-inf'))
                best_action = np.argmax(action_returns) - MAX_MOVE
                policy[s1, s2] = best_action
                if best_action != old_action:
                    policy_stable = False

        if policy_stable:
            break

policy_iteration()

# Output optimal policy and value function
print("Optimal Policy:")
print(policy)
print("Optimal Value Function:")
print(value_function)