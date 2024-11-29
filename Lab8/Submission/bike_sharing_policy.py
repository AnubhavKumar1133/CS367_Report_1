
import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import poisson

class gbr:
    @staticmethod
    def max_bikes():
        return 20
    
    @staticmethod
    def γ():
        return 0.9
    
    @staticmethod
    def credit_reward():
        return 10
    
    @staticmethod
    def moving_reward():
        return -2

class poisson_:
    def __init__(self, λ):
        self.λ = λ
        ε = 0.01
        self.α = 0
        state = 1
        self.vals = {}
        summ = 0
        
        while(1):
            if state == 1:
                temp = poisson.pmf(self.α, self.λ) 
                if temp <= ε:
                    self.α += 1
                else:
                    self.vals[self.α] = temp
                    summ += temp
                    self.β = self.α + 1
                    state = 2
            elif state == 2:
                temp = poisson.pmf(self.β, self.λ)
                if temp > ε:
                    self.vals[self.β] = temp
                    summ += temp
                    self.β += 1
                else:
                    break    
        added_val = (1 - summ) / (self.β - self.α)
        for key in self.vals:
            self.vals[key] += added_val
            
    def f(self, n):
        return self.vals.get(n, 0)

class location: 
    def __init__(self, req, ret):
        self.α = req
        self.β = ret
        self.poissonα = poisson_(self.α)
        self.poissonβ = poisson_(self.β)

def apply_action(state, action):
    return [max(min(state[0] - action, gbr.max_bikes()), 0), 
            max(min(state[1] + action, gbr.max_bikes()), 0)]

def expected_reward(state, action):
    global value
    ψ = gbr.moving_reward() * abs(action)
    new_state = apply_action(state, action)
    for Aα in range(A.poissonα.α, A.poissonα.β):
        for Bα in range(B.poissonα.α, B.poissonα.β):
            for Aβ in range(A.poissonβ.α, A.poissonβ.β):
                for Bβ in range(B.poissonβ.α, B.poissonβ.β):
                    ζ = A.poissonα.vals[Aα] * B.poissonα.vals[Bα] * A.poissonβ.vals[Aβ] * B.poissonβ.vals[Bβ]
                    valid_requests_A = min(new_state[0], Aα)
                    valid_requests_B = min(new_state[1], Bα)
                    rew = (valid_requests_A + valid_requests_B) * gbr.credit_reward()
                    new_s = [
                        max(min(new_state[0] - valid_requests_A + Aβ, gbr.max_bikes()), 0),
                        max(min(new_state[1] - valid_requests_B + Bβ, gbr.max_bikes()), 0)
                    ]
                    ψ += ζ * (rew + gbr.γ() * value[new_s[0]][new_s[1]])
    return ψ

def policy_evaluation():
    global value
    ε = policy_evaluation.ε
    policy_evaluation.ε /= 10 
    while True:
        δ = 0
        for i in range(value.shape[0]):
            for j in range(value.shape[1]):
                old_val = value[i][j]
                value[i][j] = expected_reward([i, j], policy[i][j])
                δ = max(δ, abs(value[i][j] - old_val))
        if δ < ε:
            break

def policy_improvement():
    global policy
    policy_stable = True
    for i in range(value.shape[0]):
        for j in range(value.shape[1]):
            old_action = policy[i][j]
            max_act_val = None
            max_act = None
            τ12 = min(i, 5)
            τ21 = -min(j, 5)
            for act in range(τ21, τ12 + 1):
                σ = expected_reward([i, j], act)
                if max_act_val is None or max_act_val < σ:
                    max_act_val = σ
                    max_act = act
            policy[i][j] = max_act
            if old_action != policy[i][j]:
                policy_stable = False
    return policy_stable

A = location(3, 3)
B = location(4, 2)
value = np.zeros((gbr.max_bikes() + 1, gbr.max_bikes() + 1))
policy = value.copy().astype(int)
policy_evaluation.ε = 50
while True:
    policy_evaluation()
    if policy_improvement():
        break
