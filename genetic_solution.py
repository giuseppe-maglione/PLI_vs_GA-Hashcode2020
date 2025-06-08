import random
import time

# parameters
POPULATION_SIZE = 50
NUM_GENERATIONS = 500
MUTATION_RATE = 0.05
TOURNAMENT_SIZE = 3
TIME_LIMIT = 60

def fitness(bitstring, slices, M):
    total = sum(s for i, s in enumerate(slices) if bitstring[i])
    if total <= M:
        return total
    else:
        return M - (total - M)  # penalità lineare

def tournament_selection(population, slices, M, k=TOURNAMENT_SIZE):
    selected = random.sample(population, k)
    selected.sort(key=lambda x: fitness(x, slices, M), reverse=True)
    return selected[0]

def crossover_2point(parent1, parent2):
    point1, point2 = sorted(random.sample(range(len(parent1)), 2))
    return parent1[:point1] + parent2[point1:point2] + parent1[point2:]


def mutate(bitstring):
    mutated_bitstring = []
    for bit in bitstring:
        if random.random() < MUTATION_RATE:
            mutated_bitstring.append(bit ^ 1)   # inverte il bit
        else:
            mutated_bitstring.append(bit)   # lascia il bit inalterato
    return mutated_bitstring

def generate_first_population(M, N, slices):
    population = []

    for _ in range(POPULATION_SIZE):
        strategy = random.choice(['desc', 'asc', 'shuffle'])    # scegliamo casualmente in che modo generare la prima popolazione
        indices = list(range(N))
        
        if strategy == 'desc':  
            indices.sort(key=lambda i: -slices[i])      # greedy
        elif strategy == 'asc': 
            indices.sort(key=lambda i: slices[i])       # greedy inverso
        elif strategy == 'shuffle':
            random.shuffle(indices)                     # casuale

        total = 0
        bitstring = [0] * N

        for i in indices:
            if total + slices[i] <= M:
                total += slices[i]
                bitstring[i] = 1

        population.append(bitstring)

    return population

def solve(M, N, slices):
    start_time = time.perf_counter()
    population = generate_first_population(M, N, slices)
    best_individual = max(population, key=lambda x: fitness(x, slices, M))
    best_score = fitness(best_individual, slices, M)

    for gen in range(NUM_GENERATIONS):
        elapsed = time.perf_counter() - start_time
        if elapsed >= TIME_LIMIT:
            print(f"\t\t[Geneneration {gen+1}] Early stop, time limit reached ({elapsed:.2f}s)")
            break

        new_population = []

        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, slices, M)
            parent2 = tournament_selection(population, slices, M)

            child1 = crossover_2point(parent1, parent2)
            child2 = child1[:]  # copia diretta

            child1 = mutate(child1)  # solo il primo figlio mutato

            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

        # salva il miglior individuo
        current_best = max(population, key=lambda x: fitness(x, slices, M))
        current_score = fitness(current_best, slices, M)
        if current_score > best_score:
            best_individual = current_best
            best_score = current_score

        if gen == 0 or (gen + 1) % 50 == 0:
            print(f"\t\t[Geneneration {gen+1}] Current best fitness = {best_score}")

        if best_score == M:
            print(f"\t\t[Geneneration {gen+1}] Early stop, fitness reached max score ({M})")
            break

    elapsed_time = time.perf_counter() - start_time
    return best_score, elapsed

"""
OLD FITNESS FUNC
def fitness(bitstring, slices, M):
    total = sum(s for i, s in enumerate(slices) if bitstring[i])
    return total if total <= M else 0  # penalizza se invalido
"""

"""
OLD REPAIR FUNC
def repair(bitstring, slices, M):
    total = sum(s for i, s in enumerate(slices) if bitstring[i])
    if total <= M:
        return bitstring

    # rimuove pizze finché rientra in M
    indices = [i for i, bit in enumerate(bitstring) if bit == 1]
    random.shuffle(indices)
    for i in indices:
        bitstring[i] = 0
        total -= slices[i]
        if total <= M:
            break
    return bitstring
"""
