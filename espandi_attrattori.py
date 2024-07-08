import os
import numpy as np

#Definizione file con dati in input
input_attrattori =  os.getcwd() + "/output/output_motore.txt"
input_grafo_txt =  os.getcwd() + "/output/grafo.txt"
output_dir = os.getcwd() + "/output/"


#Reading the set of initial conditions
def read_attrattori():
    with open(input_attrattori, 'r') as file:
        lines = file.readlines()
    
    n_genes, n_cond = map(int, lines[0].strip().split()[1::2])
    initial_conditions = [list(map(int, line.split())) for line in lines[1:]]
    
    return initial_conditions, n_cond


if __name__ == "__main__":

    # Carichiamo i parametri del motore
    parametri = read_attrattori()