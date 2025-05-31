import os
#import pli_solution
import genetic_solution

def read_dataset(dataset_path):
    with open(dataset_path, 'r') as file:
        # Legge la prima riga: M = max fette, N = numero di tipi di pizza
        first_line = file.readline()
        M, N = map(int, first_line.strip().split())

        # Legge la seconda riga: lista delle fette per tipo di pizza
        slices = list(map(int, file.readline().strip().split()))

        return M, N, slices
    
def list_datasets():
    input_folder = 'Datasets'
    dataset_paths = []

    # Verifica se la cartella esiste
    if not os.path.isdir(input_folder):
        print(f"La cartella '{input_folder}' non esiste.")
        return

    # Itera sui file nella cartella
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

        print("\t[] Risoluzione con PLI in corso...")
        best_score_pli = pli_solution.solve(M, N, slices)  

        print("\t[] Risoluzione con algoritmo genetico in corso...")
        best_score_genetic = genetic_solution.solve(M, N, slices)

        print("\tMiglior punteggio con PLI:", best_score_pli)
        print("\tMiglior punteggio con algoritmo genetico:", best_score_genetic)

        print("-"*100)

