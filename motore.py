import numpy as np
import json
import os

#Definizione file con dati in input
input_motore =  os.getcwd() + "/input/input_motore.txt"
input_grafo =  os.getcwd() + "/output/rete.json"
input_condInit =  os.getcwd() + "/output/condizioni_iniziali.txt"
output_dir = os.getcwd() + "/output/"

#Oggetto che rappresenta la rete
class RandomBooleanNetwork:
    def __init__(self, N, adjacency_matrix, functions):
        self.N = N  # Number of nodes
        self.adjacency_matrix = adjacency_matrix  # Adjacency matrix
        self.functions = functions  # List of boolean functions for each node
        self.state = np.zeros(N, dtype=int)  # Initial state (to be set later)
    
    def set_initial_state(self, initial_state): # Set initial state to the network
        self.state = np.array(initial_state)
    
    def _update_node(self, node):
        inputs = self.adjacency_matrix[node]
        input_states = self.state[np.where(inputs == 1)]
        input_index = int("".join(map(str, input_states)), 2)
        return self.functions[node][input_index]
    
    def step(self):
        new_state = np.zeros_like(self.state)
        for i in range(self.N):
            new_state[i] = self._update_node(i)
        self.state = new_state
    
    def run(self, steps):
        history = [self.state.copy()]
        for _ in range(steps):
            self.step()
            history.append(self.state.copy())
        return history
    
    def print_network(self):    # print network info
        print("Adjacency Matrix:")
        print(self.adjacency_matrix)
        print("\nBoolean Functions:")
        for i, func in enumerate(self.functions):
            print(f"Node {i}: {func}")

#Reading from file motore parameters, n_step - mode - finamx
def read_param():
    parametri = {}
    with open(input_motore, 'r') as file:
        for line in file:
            if line.strip():
                key, value = line.split(':')
                parametri[key.strip()] = value.strip()
    return parametri

#Reading graph from json 
def read_graph():
    with open(input_grafo, 'r') as file:
        data = json.load(file)
    
    n_genes = len(data)
    adjacency_matrix = np.zeros((n_genes, n_genes), dtype=int)
    functions = [None] * n_genes
    
    for gene, details in data.items():
        gene_index = int(gene)
        inputs = details["ingressi"]
        outputs = details["uscite"]
        
        adjacency_matrix[gene_index, inputs] = 1
        functions[gene_index] = outputs
    
    return n_genes, adjacency_matrix, functions

#Reading the set of initial conditions
def read_init_conditions():
    with open(input_condInit, 'r') as file:
        lines = file.readlines()
    
    n_genes, n_cond = map(int, lines[0].strip().split()[1::2])
    initial_conditions = [list(map(int, line.split())) for line in lines[1:]]
    
    return initial_conditions


if __name__ == '__main__':
    
    # read param of motore
    parametri = read_param()

    # Conversione dei parametri letti dal file al tipo corretto
    n_steps = int(parametri['n_steps'])
    mode = int(parametri['mode'])
    print(mode)
    fin_max = int(parametri['finmax'])

    n_genes, adjacency_matrix, functions = read_graph()
    rbn = RandomBooleanNetwork(n_genes, adjacency_matrix, functions)

    # Print the network structure
    print("Generated Random Boolean Network:")
    rbn.print_network()

    initial_conditions = read_init_conditions()

    # Run simulation for each initial condition
    results = []
    for initial_state in initial_conditions:
        rbn.set_initial_state(initial_state)
        if mode == 1:
            break
        elif mode == 2:
            history = rbn.run(n_steps)
            results.append(history)
        elif mode == 3:
            break

    # Print results
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        for i, (initial_state, history) in enumerate(zip(initial_conditions, results)):
            print(f"\nInitial condition {i + 1}: {initial_state}")
            file.write(f"\nInitial condition {i + 1}: {initial_state}\n")
            for step, state in enumerate(history):
                print(f" Step {step}: {state}")
                file.write(f"\nStep {step}: {state}")


