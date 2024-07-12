import os
import numpy as np
from motore import simulate_rbn, load_rete_from_text

#Definizione file con dati in input
input_attrattori =  os.getcwd() + "/output_motore_rapporto.txt"
input_grafo_txt =  os.getcwd() + "/grafo.txt"
output_file = os.getcwd() + "/attrattori_espansi.txt"


#Reading the set of initial conditions
def read_attrattori():
    with open(input_attrattori, 'r') as file:
        lines = file.readlines()
    
    n_cond, n_genes = map(int, lines[0].strip().split()[1::2])

    # Inizializzazione attrattori e periodi
    attractors = []


    for line in lines[1:]:
        tmp = line.split()
        attractor = list(map(int, tmp[:n_genes]))
        period = int(tmp[n_genes])
        #step = float(tmp[n_genes + 1])
        attractors.append((attractor, period))
    
    return attractors, n_genes, len(attractors)

def expand_attractors(attractors):
    results = []
    network, n_genes = load_rete_from_text()

    for a in attractors:
        attractor = a[0]
        period = a[1]
        results.append(simulate_rbn(network, attractor, period))
    
    return results

def write_results(results, n_genes, n_cond):
     # Print the results
    with open(output_file, 'w') as file:
        file.write(f'n_genes: {n_genes} n_cond: {n_cond}\n')
        for result in results:
            #print(result)
            for state in result:
                #print(f"{' '.join(str(x) for x in state)}\n")
                file.write(f"{' '.join(str(x) for x in state)}\n")
            file.write("\n")


if __name__ == "__main__":

    # Carichiamo i parametri del motore
    # n_cond --> sono il numero di attrattori che in questo caso sono le condizioni di simulazione
    attractors, n_genes, n_cond = read_attrattori()

    results = expand_attractors(attractors)

    write_results(results, n_genes, n_cond)