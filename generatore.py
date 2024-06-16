import random
import json
import os
import numpy as np

input_file =  os.getcwd() + "/input/input_generatore.txt"
output_dir = os.getcwd() + "/output/"

#Leggiamo i parametri in input dal file
def read_param():
    parametri = {}
    with open(input_file, 'r') as file:
        for line in file:
            if line.strip():
                key, value = line.split(':')
                parametri[key.strip()] = value.strip()
    return parametri

def generate_RBN(n_nodi, k_minimo, k_massimo, probabilita_k, bias, seme):
    random.seed(seme)
    rete = {}
    
    if len(probabilita_k) != (k_massimo - k_minimo + 1):
        raise ValueError("Il numero di probabilità di k deve essere uguale al numero di valori possibili di k")
    
    if len(bias) != (k_massimo - k_minimo + 1):
        raise ValueError("Il numero di bias deve essere uguale al numero di valori possibili di k")
    
    if not np.isclose(sum(probabilita_k), 1.0):
        raise ValueError("La somma delle probabilità di k deve essere uguale a 1")
    
    if any(b < 0 or b > 1 for b in bias):
        raise ValueError("I bias devono essere compresi tra 0 e 1")
    
    for nodo in range(n_nodi):
        k = random.choices(range(k_minimo, k_massimo + 1), probabilita_k)[0]
        ingressi = random.sample(range(n_nodi), k)
        num_uscite = 2 ** k
        #uscite = [int(random.random() < bias[k - k_minimo]) for _ in range(num_uscite)]
        uscite = [random.choices([0, 1], [(1.0 - bias[k - k_minimo]), bias[k - k_minimo]])[0] for _ in range(num_uscite)]
        rete[nodo] = {
            "ingressi": ingressi,
            "uscite": uscite
        }
    return rete


def write_on_json(rete, file_output):
    with open(file_output, 'w') as file:
        json.dump(rete, file, indent=4)

def write_output(rete, file_output):
    with open(file_output, 'w') as file:
        for nodo in rete:
            print(f"gene: {nodo}")
            file.write(f"gene: {nodo}\n")
            print(f"lista_ingressi({len(rete[nodo]["ingressi"])}): {' '.join(map(str, rete[nodo]["ingressi"]))}")
            file.write(f"lista_ingressi({len(rete[nodo]["ingressi"])}): {' '.join(map(str, rete[nodo]["ingressi"]))}\n")
            print(f"uscite({len(rete[nodo]["uscite"])}): {' '.join(map(str, rete[nodo]["uscite"]))}")
            file.write(f"uscite({len(rete[nodo]["uscite"])}): {' '.join(map(str, rete[nodo]["uscite"]))}\n")


if __name__ == '__main__':
    
    # Lettura dei parametri dal file
    parametri = read_param()

   # Conversione dei parametri letti dal file al tipo corretto
    n_nodi = int(parametri['n_nodi'])
    k_minimo = int(parametri['k_minimo'])
    k_massimo = int(parametri['k_massimo'])
    probabilita_k = list(map(float, parametri['probabilità_k'].split()))
    bias = list(map(float, parametri['bias per ogni k'].split()))
    seme = int(parametri['seme'])

    # Generazione della rete casuale
    rete = generate_RBN(n_nodi, k_minimo, k_massimo, probabilita_k, bias, seme)

    # Scrittura della rete su json
    write_on_json(rete, output_dir+'rete.json')

    # Scrittura della rete su stdout e text
    write_output(rete, output_dir+'grafo.txt')