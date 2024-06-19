import random
import os

input_file =  os.getcwd() + "/input/input_initcond.txt"
output_dir = os.getcwd() + "/output/"

#Leggiamo i parametri in input dal file
def read_param():
    with open(input_file, 'r') as file:
        # Legge tutte le righe del file
        lines = file.readlines()

    # Estrae i valori delle variabili
    n_genes = int(lines[0].split(":")[1].strip())
    n_cond = int(lines[1].split(":")[1].strip())
    bias = float(lines[2].split(":")[1].strip())
    seme = int(lines[3].split(":")[1].strip())
    
    # Legge la maschera e separa il primo 1 dalla lista rimanente
    maschera = list(map(int, lines[4].split(":")[1].strip().split()))
    flag = maschera[0]
    mask = list(map(int, lines[5].split()))

    return n_genes, n_cond, bias, seme, flag, mask

def gen_condizioni_iniziali(n_genes, n_cond, bias, seme, maschera):
    random.seed(seme)
    condizioni = []
    
    for _ in range(n_cond):
        condizione = []
        for i in range(n_genes):
            if maschera[i] == 0:
                val = 0
            elif maschera[i] == 1:
                val = 1
            elif maschera[i] == 2:
                val = random.choices([0, 1], [(1.0 - bias), bias])[0]
            condizione.append(val)
        condizioni.append(condizione)
    
    return condizioni

def write_out(condizioni, out_file, n_genes, n_cond):
    with open(out_file, 'w') as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")
        for condizione in condizioni:
            file.write(' '.join(map(str, condizione)) + '\n')


if __name__ == '__main__':
    
    # Lettura dei parametri dal file
    n_genes, n_cond, bias, seme, flag, mask = read_param()


    # Generazione delle condizioni iniziali
    condizioni_iniziali = gen_condizioni_iniziali(n_genes, n_cond, bias, seme, mask)

    # Scrittura delle condizioni su file
    write_out(condizioni_iniziali, (output_dir+'condizioni_iniziali.txt'), n_genes, n_cond)
