import os
import matplotlib.pyplot as plt
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
    #for filename in os.listdir(input_folder):
    #    if filename.endswith('.in'):
    #        full_path = os.path.join(input_folder, filename)
    #        dataset_paths.append(full_path)

    full_path = os.path.join(input_folder, 'small.in')
    dataset_paths.append(full_path)
    full_path = os.path.join(input_folder, 'medium.in')
    dataset_paths.append(full_path)
    full_path = os.path.join(input_folder, 'big.in')
    dataset_paths.append(full_path) 
    full_path = os.path.join(input_folder, 'extra.in')
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

    # --- Grafici ---
    plt.figure(figsize=(12, 8))     # imposta le dimensioni della figura

    plt.scatter(results["pli_times"], results["pli_scores"],
                color='blue', marker='o', s=100, label='PLI Solution')
    for i, dataset_name in enumerate(results["dataset_names"]):
        plt.text(results["pli_times"][i], results["pli_scores"][i], f' {dataset_name}',
                fontsize=9, ha='left', va='bottom', color='blue')

    # Grafico Algoritmo Genetico
    plt.scatter(results["genetic_times"], results["genetic_scores"],
                color='red', marker='x', s=100, label='Algoritmo Genetico')
    for i, dataset_name in enumerate(results["dataset_names"]):
        plt.text(results["genetic_times"][i], results["genetic_scores"][i], f' {dataset_name}',
                fontsize=9, ha='left', va='bottom', color='red')


    plt.title('Comparazione Score vs. Tempo per Dataset')
    plt.xlabel('Tempo (secondi)')
    plt.ylabel('Score')
    plt.grid(True)
    plt.legend() # Mostra la legenda per i tipi di soluzione
    plt.tight_layout() # Adatta automaticamente i parametri della trama per un layout stretto
    plt.show()

