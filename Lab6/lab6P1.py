import numpy as np

class HopfieldNetwork:
    def _init_(self, size):
        self.size = size
        self.weights = np.zeros((size, size))
    
    def train(self, patterns):
        for pattern in patterns:
            self.weights += np.outer(pattern, pattern)
        np.fill_diagonal(self.weights, 0)
    
    def recall(self, pattern, steps=10):
        state = np.copy(pattern)
        for _ in range(steps):
            for i in range(self.size):
                state[i] = 1 if np.dot(self.weights[i], state) > 0 else -1
        return state

network_size = 100
patterns = [
    np.random.choice([-1, 1], size=network_size),
    np.random.choice([-1, 1], size=network_size)
]

hn = HopfieldNetwork(size=network_size)
hn.train(patterns)
retrieved_pattern = hn.recall(patterns[0])

print("Original Pattern:")
print(patterns[0])

print("\nRecalled Pattern:")
print(retrieved_pattern)

is_match = np.array_equal(patterns[0], retrieved_pattern)
print("\nPattern successfully recalled:", is_match)