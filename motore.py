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


if __name__ == '__main__':
    
    # Lettura dei parametri dal file
    parametri = read_param()

   # Conversione dei parametri letti dal file al tipo corretto
    n_steps = int(parametri['n_steps'])
    mode = int(parametri['mode'])
    fin_max = int(parametri['fin_max'])
