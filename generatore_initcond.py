import random
import os

input_file =  os.getcwd() + "/input/input_initcond.txt"
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

def gen_condizioni_iniziali(n_genes, n_cond, bias, seme):
    random.seed(seme)
    condizioni = []
    
    for _ in range(n_cond):
        condizione = [random.choices([0, 1], [(1.0 - bias), bias])[0] for _ in range(n_genes)]
        condizioni.append(condizione)
    
    return condizioni

def write_out(condizioni, out_file, n_genes, n_cond):
    with open(out_file, 'w') as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond}\n")
        for condizione in condizioni:
            file.write(' '.join(map(str, condizione)) + '\n')


if __name__ == '__main__':
    
    # Lettura dei parametri dal file
    parametri_iniziali = read_param()

    # Conversione dei parametri letti dal file al tipo corretto
    n_genes = int(parametri_iniziali['n_genes'])
    n_cond = int(parametri_iniziali['n_cond'])
    bias = float(parametri_iniziali['bias'])
    seme = int(parametri_iniziali['seme'])
    maschera = int(parametri_iniziali['maschera'])


    # Generazione delle condizioni iniziali
    condizioni_iniziali = gen_condizioni_iniziali(n_genes, n_cond, bias, seme)

    # Scrittura delle condizioni su file
    write_out(condizioni_iniziali, (output_dir+'condizioni_iniziali.txt'), n_genes, n_cond)
