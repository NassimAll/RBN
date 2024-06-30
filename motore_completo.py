import json
import os
import numpy as np

#Definizione file con dati in input
input_motore =  os.getcwd() + "/input/input_motore.txt"
input_grafo =  os.getcwd() + "/output/rete.json"
input_condInit =  os.getcwd() + "/output/condizioni_iniziali.txt"
output_dir = os.getcwd() + "/output/"


def load_network_from_json():
    with open(input_grafo, 'r') as f:
        network = json.load(f)
    return network

def boolean_function_output(inputs, outputs):
    index = int(''.join(map(str, inputs)), 2)
    return outputs[index]

def simulate_rbn(network, initial_conditions, steps):
    n_genes = len(network)
    results = []
    
    for initial in initial_conditions:
        state = np.array(initial)
        trajectory = [state.copy()]
        
        for _ in range(steps):
            new_state = state.copy()
            for node, info in network.items():
                node = int(node)
                ingressi = info['ingressi']
                uscite = info['uscite']
                inputs = [state[i] for i in ingressi]
                new_state[node] = boolean_function_output(inputs, uscite)
            state = new_state
            trajectory.append(state.copy())
        results.append(trajectory)
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

if __name__ == "__main__":

    # Carichiamo i parametri del motore
    parametri = read_parametri()

    # Conversione dei parametri letti dal file al tipo corretto
    n_steps = int(parametri['n_steps'])
    mode = int(parametri['mode'])
    print(mode)
    fin_max = int(parametri['finmax'])
    
    # Carichiamo la rete e la sequenza di ocndizioni iniziali
    network = load_network_from_json()
    initial_conditions, n_cond = read_init_conditions()

    # Simulate the network for each initial condition for a given number of steps
    steps = 10
    results = simulate_rbn(network, initial_conditions, steps)
    
    # Print the results
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        for i, result in enumerate(results):
            print(f"Initial condition {i+1}: {initial_conditions[i]}")
            file.write(f"Initial condition {i+1}: {initial_conditions[i]}\n")
            for step, state in enumerate(result):
                print(f" Step {step}: {state}")
                file.write(f" Step {step}: {state}\n")
            print()

