import random
import matplotlib.pyplot as plt
from pysat.solvers import Solver
import numpy as np
import time

def generate_sat_instance(n, m, k):
    clauses = set()
    while len(clauses) < m:
        clause = set()
        while len(clause) < k:
            literal = random.randint(1, n)
            if random.random() < 0.5:
                literal = -literal
            if -literal not in clause:
                clause.add(literal)
        clauses.add(tuple(clause))
    return list(clauses)

def is_satisfiable(clauses):
    solver = Solver(name='glucose3')
    for clause in clauses:
        solver.add_clause(clause)
    result = solver.solve()
    solver.delete()
    return result

n = 50 #Mude caso precise.
k_values = [3, 5]
num_instances = 30 #Mude caso precise.

alpha_ranges = {
    3: np.arange(1.0, 10.1, 0.1),
    5: np.arange(1.0, 30.1, 0.1)
}

results = {}
plt.figure(figsize=(8, 6))

for k in k_values:
    alpha_values = alpha_ranges[k]
    probabilities = []
    times = []

    for alpha in alpha_values:
        m = int(alpha * n)
        satisfiable_count = 0
        start_time = time.time()

        for _ in range(num_instances):
            if is_satisfiable(generate_sat_instance(n, m, k)):
                satisfiable_count += 1

        probability = satisfiable_count / num_instances
        elapsed_time = (time.time() - start_time) / num_instances
        probabilities.append(probability)
        times.append(elapsed_time)

    results[k] = (alpha_values, probabilities, times)

    plt.figure(figsize=(8, 6))
    plt.plot(alpha_values, probabilities, marker='o', label=f'{k}-SAT')
    plt.xlabel('Razão α = m/n')
    plt.ylabel('Probabilidade de SAT')
    plt.title(f'Probabilidade de SAT para {k}-SAT')
    plt.legend()
    plt.grid(True)
    plt.show()

critical_points = {}
for k in k_values:
    alpha_values, probabilities, _ = results[k]
    critical_alpha = alpha_values[np.argmax(np.diff(probabilities) < -0.5)]
    critical_points[k] = critical_alpha
    plt.axvline(x=critical_alpha, linestyle='--', color='r', alpha=0.7, label=f'αc {k}-SAT')
    plt.plot(alpha_values, probabilities, marker='o', label=f'{k}-SAT')

plt.xlabel('Razão α = m/n')
plt.ylabel('Probabilidade de SAT')
plt.title('Ponto Crítico da Transição de Fase')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
for k in k_values:
    alpha_values, _, times = results[k]
    plt.plot(alpha_values, times, marker='s', label=f'Tempo médio {k}-SAT')

plt.xlabel('Razão α = m/n')
plt.ylabel('Tempo médio de execução (s)')
plt.title('Tempo Médio de Execução por α')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
for k in k_values:
    alpha_values, probabilities, _ = results[k]
    plt.plot(alpha_values, probabilities, marker='o', label=f'{k}-SAT')

plt.xlabel('Razão α = m/n')
plt.ylabel('Probabilidade de SAT')
plt.title('Comparação entre 3-SAT e 5-SAT')
plt.legend()
plt.grid(True)
plt.show()

print("Pontos críticos αc para cada k-SAT:", critical_points)
