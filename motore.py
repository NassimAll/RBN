import json
import os
import numpy as np

#Definizione file con dati in input
input_motore =  os.getcwd() + "/input/input_motore.txt"
input_grafo =  os.getcwd() + "/output/rete.json"
input_grafo_txt =  os.getcwd() + "/output/grafo.txt"
input_condInit =  os.getcwd() + "/output/condizioni_iniziali.txt"
output_dir = os.getcwd() + "/output/"

#load da file di testo
def load_rete_from_text():
    network = {}
    
    with open(input_grafo_txt, 'r') as file:
        lines = file.readlines()
    
    n_genes = int(lines[0].strip().split(": ")[1])
    
    for i in range(1, len(lines), 3):
        gene_info = lines[i].strip().split(": ")
        gene_id = int(gene_info[1])
        
        inputs_info = lines[i + 1].strip().split(": ")[1].split()
        input_nodes = list(map(int, inputs_info))
        
        outputs_info = lines[i + 2].strip().split(": ")[1].split()
        output_values = list(map(int, outputs_info))
        
        network[gene_id] = {
            'ingressi': input_nodes,
            'uscite': output_values
        }
    
    return network

#Load da json, più veloce
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

# Funzione per convertire un array numpy in una stringa binaria
def array_to_binary_string(arr):
    return ''.join(str(x) for x in arr)

#Rilevamento dell'attrattore
def detect_attractor(traiettoria, fin_max):
    stati_to_index = {}
    trai_len = len(traiettoria)
    # Iniziamo a risalire la traiettoria dall'ultimo stato
    for index in range(trai_len - 1, max(trai_len - fin_max - 1, -1), -1):
        stato = tuple(traiettoria[index]) #trasformo in tupla perche non posso lavorare con array
        
        if stato in stati_to_index:
            first_occurrence = stati_to_index[stato]
            periodo = index - first_occurrence

             # Calcoliamo il nome dell'attrattore trovando lo stato con il valore decimale massimo
            period_states = traiettoria[index:(first_occurrence + index)]
            #print("sus")
            #print(period_states)
            # Convertiamo ogni array in una stringa binaria
            lista_stringhe_binarie = [array_to_binary_string(arr) for arr in period_states]
            max_state = max(lista_stringhe_binarie)

            return tuple(max_state), abs(periodo), (first_occurrence - abs(periodo))
        
        stati_to_index[stato] = index
        
    return None, None, None

#Avvia la simulazione per ogni cond init
def simulate_rbn(network, initial_conditions, steps, mode, fin_max):
    #n_genes = len(network)
    results = []
    attrattori = []


    for initial in initial_conditions:
        state = np.array(initial) #Carico lo stato iniziale
        traiettoria = [state.copy()] #inizializzo la traiettoria al primo stato
        trovato = False

        for step in range(steps):
            new_state = state.copy() # stato successivo
            for node, info in network.items(): # Calcolo lo stato per ogni singolo nodo
                node = int(node)
                ingressi = info['ingressi'] # nodi in ingresso
                uscite = info['uscite'] # tabella delle uscite
                inputs = [state[i] for i in ingressi] # carico il valore degli ingressi nel nodo, in ordine
                new_state[node] = boolean_function_output(inputs, uscite) # funzione per calcolare il valore dell'uscita
            state = new_state # salvo il nuovo stato 
            traiettoria.append(state.copy())

            if mode == 3:
                if np.array_equal(state, traiettoria[-2]): #prima controllo che non sia gia presente prima 
                    attrattori.append((state.copy(), 1, step))
                    trovato = True
                else: # poi controllo l'attrattore ciclico
                    attractor, period, passo = detect_attractor(traiettoria, fin_max)
                    if attractor:
                        attrattori.append((attractor, period, passo))
                        trovato = True
            
            if trovato:
                results.append(traiettoria)
                break
        results.append(traiettoria)
    
    return results, attrattori


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


def print_result_mode_3(attrattori):

    print("Detected attractors:")
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        for attractor, period, step in attrattori:
            file.write(f"Attrattore: {' '.join(str(x) for x in attractor)}, Periodo: {period}, Step: {step}\n")
            print(f"Attractor: {' '.join(str(x) for x in attractor)}, Period: {period}, Step: {step}")



if __name__ == "__main__":

    # Carichiamo i parametri del motore
    parametri = read_parametri()

    # Conversione dei parametri letti dal file al tipo corretto
    n_steps = int(parametri['n_steps'])
    mode = int(parametri['mode'])
    print(mode)
    fin_max = int(parametri['finmax'])
    
    # Carichiamo la rete e la sequenza di ocndizioni iniziali
    #network = load_rete()
    network = load_rete_from_text()
    initial_conditions, n_cond = read_init_conditions()

    results, attrattori = simulate_rbn(network, initial_conditions, n_steps, mode, fin_max)
    
    if mode == 1:
        print_result_mode_1(results, initial_conditions)
    elif mode == 2:
        print_result_mode_2(results, initial_conditions)
    elif mode == 3:
        print_result_mode_3(attrattori)


