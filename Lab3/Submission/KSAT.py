import random

def generate_kSAT_instance(n, k, m):
    if n < k:
        raise ValueError("Error: n must be greater than or equal to k")
    
    variables = [f"v{i+1}" for i in range(n)]
    problem = []
    
    for i in range(m):
        clause = []
        selected_vars = random.sample(variables, k) 

        for var in selected_vars:
            if random.random() < 0.5:
                clause.append(f"~{var}")
            else:
                clause.append(f"{var}")

        problem.append(f"({' or '.join(clause)})")
    
    return " and ".join(problem)

n = int(input("Enter the number of variables (n): "))
k = int(input("Enter the number of literals per clause (k): "))
m = int(input("Enter the number of clauses (m): "))

random_kSAT_problem = generate_kSAT_instance(n, k, m)
print(f"\nGenerated {k}-SAT problem with {n} variables and {m} clauses:")
print(f"\n{random_kSAT_problem}")