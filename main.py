import os
import tracemalloc
import time
import pli_solution
import genetic_solution

def read_dataset(dataset_path):
    with open(dataset_path, 'r') as file:
        first_line = file.readline()
        M, N = map(int, first_line.strip().split())
        slices = list(map(int, file.readline().strip().split()))
        return M, N, slices
    
def list_datasets():
    input_folder = 'Datasets'
    dataset_paths = []

    # verifica se la cartella esiste
    if not os.path.isdir(input_folder):
        print(f"La cartella '{input_folder}' non esiste.")
        return

    # itera sui file nella cartella
    for filename in os.listdir(input_folder):
        if filename.endswith('.in'):
            full_path = os.path.join(input_folder, filename)
            dataset_paths.append(full_path)

    return dataset_paths
    
if __name__ == '__main__':

    #dataset_paths = list_datasets()
    path = os.path.join('Datasets', 'a_example.in')
    dataset_paths = []
    dataset_paths.append(path)

    best_score_genetic = 0
    best_score_pli = 0

    dataset_type = 'small'

    print("-"*50)

    for path in dataset_paths:

        print('Risolvendo:', path)
        M, N, slices = read_dataset(path)
        print("\tMax fette:", M)
        print("\tNumero tipi di pizza:", N)
        if len(slices) < 20:
            print("\tLista fette per pizza:", slices)
            dataset_type = 'small'
        else:
            print("\tLista fette per pizza: [...]")
            dataset_type = 'big'

        # --- PLI ---
        print("\t[] Risoluzione con PLI in corso...")
        tracemalloc.start()
        start_time = time.perf_counter()

        best_score_pli = pli_solution.solve(M, N, slices)

        pli_time = time.perf_counter() - start_time
        pli_mem_current, pli_mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop() 

        # --- Algoritmo Genetico ---
        print("\t[] Risoluzione con algoritmo genetico in corso...")
        tracemalloc.start()
        start_time = time.perf_counter()

        best_score_genetic = genetic_solution.solve(M, N, slices)

        genetic_time = time.perf_counter() - start_time
        genetic_mem_current, genetic_mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Risultati ---
        print("\n== RISULTATI ==")
        print(f"PLI -> Score: {best_score_pli}, Tempo: {pli_time:.4f}s, Memoria: {pli_mem_peak / 1024:.2f} KB")
        print(f"Genetico -> Score: {best_score_genetic}, Tempo: {genetic_time:.4f}s, Memoria: {genetic_mem_peak / 1024:.2f} KB")

        print("-"*100)

