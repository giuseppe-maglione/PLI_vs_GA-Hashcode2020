import os
import pli_solution
import genetic_solution

def read_dataset(dataset_path):
    with open(dataset_path, 'r') as file:
        first_line = file.readline()
        M, N = map(int, first_line.strip().split())
        slices = list(map(int, file.readline().strip().split()))
        return M, N, slices
    
def list_datasets(input_folder='Datasets'):
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

    dataset_paths = list_datasets('Datasets')

    results = {                 # struttura per memorizzare i risultati
        "dataset_names": [],
        "pli_scores": [],
        "pli_times": [],
        "genetic_scores": [],
        "genetic_times": []
    }

    print("-"*80)

    for path in dataset_paths:
        results["dataset_names"].append(path)

        print(f"== RISOLUZIONE ==")
        M, N, slices = read_dataset(path)
        print(f"\tDataset: {path}")
        print("\tMax fette:", M)
        print("\tNumero tipi di pizza:", N)
        if len(slices) < 20:
            print("\tLista fette per pizza:", slices)
        else:
            print("\tLista fette per pizza: [...]")

        # --- PLI ---
        print("\t[] Risoluzione con PLI in corso...")
        pli_score, pli_time = pli_solution.solve(M, N, slices)
        results["pli_scores"].append(pli_score)
        results["pli_times"].append(pli_time)

        # --- Algoritmo Genetico ---
        print("\t[] Risoluzione con algoritmo genetico in corso...")
        genetic_score, genetic_time = genetic_solution.solve(M, N, slices) 
        results["genetic_scores"].append(genetic_score)
        results["genetic_times"].append(genetic_time)

        # --- Risultati ---
        print("== RISULTATI ==")
        print(f"\tPLI -> Score: {pli_score}, Tempo: {pli_time:.4f}s")
        print(f"\tGenetico -> Score: {genetic_score}, Tempo: {genetic_time:.4f}s")

        print("-"*80)

