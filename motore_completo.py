import json
import os
import numpy as np

#Definizione file con dati in input
input_motore =  os.getcwd() + "/input/input_motore.txt"
input_grafo =  os.getcwd() + "/output/rete.json"
input_condInit =  os.getcwd() + "/output/condizioni_iniziali.txt"
output_dir = os.getcwd() + "/output/"


def load_rete():
    with open(input_grafo, 'r') as f:
        network = json.load(f)
    return network

#Costruisco il binario dagli input e lo trasformo nell'indice che mi rappresenta il suo out
# inputs --> 0 1 --> 01 --> index = 1 --> outputs[1]
# inputs --> 1 1 --> 11 --> index = 3 --> outputs[3]

def boolean_function_output(inputs, outputs):
    index = int(''.join(map(str, inputs)), 2)
    return outputs[index]

def simulate_rbn(network, initial_conditions, steps):
    n_genes = len(network)
    results = []
    
    for initial in initial_conditions:
        state = np.array(initial) #Carico lo stato iniziale
        traiettoria = [state.copy()] #inizializzo la traiettoria al primo stato
        
        for _ in range(steps):
            new_state = state.copy() # stato successivo
            for node, info in network.items(): # Calcolo lo stato per ogni singolo nodo
                node = int(node)
                ingressi = info['ingressi'] # nodi in ingresso
                uscite = info['uscite'] # tabella delle uscite
                inputs = [state[i] for i in ingressi] # carico il valore degli ingressi nel nodo, in ordine
                new_state[node] = boolean_function_output(inputs, uscite) # funzione per calcolare il valore dell'uscita
            state = new_state # salvo il nuovo stato 
            traiettoria.append(state.copy())
        results.append(traiettoria)
    return results


#Reading from file motore parameters, n_step - mode - finamx
def read_parametri():
    parametri = {}
    with open(input_motore, 'r') as file:
        for line in file:
            if line.strip():
                key, value = line.split(':')
                parametri[key.strip()] = value.strip()
    return parametri

#Reading the set of initial conditions
def read_init_conditions():
    with open(input_condInit, 'r') as file:
        lines = file.readlines()
    
    n_genes, n_cond = map(int, lines[0].strip().split()[1::2])
    initial_conditions = [list(map(int, line.split())) for line in lines[1:]]
    
    return initial_conditions, n_cond

def print_result_mode_1(results, initial_conditions):
     # Print the results
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        for i, result in enumerate(results):
            file.write(f"Initial condition {i+1}: {initial_conditions[i]}\n")
            file.write(f" Last step : {result[-1]}\n")
            #print()

def print_result_mode_2(results, initial_conditions):
     # Print the results
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        for i, result in enumerate(results):
            #print(f"Initial condition {i+1}: {initial_conditions[i]}")
            file.write(f"Initial condition {i+1}: {initial_conditions[i]}\n")
            for step, state in enumerate(result):
                #print(f" Step {step}: {state}")
                file.write(f" Step {step}: {state}\n")
            #print()


def print_result_mode_3(results, initial_conditions):
    #TO DO
    return

if __name__ == "__main__":

    # Carichiamo i parametri del motore
    parametri = read_parametri()

    # Conversione dei parametri letti dal file al tipo corretto
    n_steps = int(parametri['n_steps'])
    mode = int(parametri['mode'])
    print(mode)
    fin_max = int(parametri['finmax'])
    
    # Carichiamo la rete e la sequenza di ocndizioni iniziali
    network = load_rete()
    initial_conditions, n_cond = read_init_conditions()

    # Eseguo la simulazione
    #steps = 10
    results = simulate_rbn(network, initial_conditions, n_steps)
    
    if mode == 1:
        print_result_mode_1(results, initial_conditions)
    elif mode == 2:
        print_result_mode_2(results, initial_conditions)
    elif mode == 3:
        print_result_mode_3(results)

    # # Print the results
    # with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
    #     for i, result in enumerate(results):
    #         print(f"Initial condition {i+1}: {initial_conditions[i]}")
    #         file.write(f"Initial condition {i+1}: {initial_conditions[i]}\n")
    #         for step, state in enumerate(result):
    #             print(f" Step {step}: {state}")
    #             file.write(f" Step {step}: {state}\n")
    #         print()

