
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

MAX_CARS = 20
GAMMA = 0.9
CREDIT_REWARD = 10
MOVING_REWARD = -2

class poisson_:
    def __init__(self, _lambda):
        self._lambda = _lambda
        epsilon = 0.01
        self.alpha = 0
        state = 1
        self.vals = {}
        summer = 0
        while True:
            if state == 1:
                temp = poisson.pmf(self.alpha, self._lambda) 
                if temp <= epsilon:
                    self.alpha += 1
                else:
                    self.vals[self.alpha] = temp
                    summer += temp
                    self.beta = self.alpha + 1
                    state = 2
            elif state == 2:
                temp = poisson.pmf(self.beta, self._lambda)
                if temp > epsilon:
                    self.vals[self.beta] = temp
                    summer += temp
                    self.beta += 1
                else:
                    break    
        added_val = (1 - summer) / (self.beta - self.alpha)
        for key in self.vals:
            self.vals[key] += added_val
        
    def f(self, n):
        return self.vals.get(n, 0)

class location:
    def __init__(self, req, ret):
        self.alpha = req
        self.beta = ret
        self.poisson_alpha = poisson_(self.alpha)
        self.poisson_beta = poisson_(self.beta)

A = location(3, 3)
B = location(4, 2)
value = np.zeros((MAX_CARS + 1, MAX_CARS + 1))
policy = value.copy().astype(int)
