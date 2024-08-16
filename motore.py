import json
import os
import numpy as np

#Definizione file con dati in input
input_motore =  os.getcwd() + "/input_motore.txt"
input_grafo =  os.getcwd() + "/rete.json"
input_grafo_txt =  os.getcwd() + "/grafo.txt"
input_condInit =  os.getcwd() + "/condizioni_iniziali.txt"
output_dir = os.getcwd() + "/"

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
    
    return network, n_genes

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
def simulate_rbn(network, initial_cond, steps):
    state = np.array(initial_cond) #Carico lo stato iniziale
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
    
    return traiettoria #Restituisce la traiettoria ottenuta

#Effettua la simulazione in modalità 3, rilevando gli attrattori per ogni traiettoria
def simulate_mode_3(network, initial_cond, steps, fin_max):
    
    state = np.array(initial_cond) #Carico lo stato iniziale
    traiettoria = [state.copy()] #inizializzo la traiettoria al primo stato

    for step in range(steps): # Inizio la simulazione
        new_state = state.copy() # stato successivo
        for node, info in network.items(): # Calcolo lo stato per ogni singolo nodo
            node = int(node)
            ingressi = info['ingressi'] # nodi in ingresso
            uscite = info['uscite'] # tabella delle uscite
            inputs = [state[i] for i in ingressi] # carico il valore degli ingressi nel nodo, in ordine
            new_state[node] = boolean_function_output(inputs, uscite) # funzione per calcolare il valore dell'uscita
        state = new_state # salvo il nuovo stato 
        traiettoria.append(state.copy())

        if np.array_equal(state, traiettoria[-2]): #Controllo che non sia un attrattore continuo 
            attrattore = (state.copy(), 1, step)
            return attrattore
        else: # poi controllo l'attrattore ciclico
            attractor, period, passo = detect_attractor(traiettoria, fin_max)
            if attractor:
                attrattore = (attractor, period, passo)
                return attrattore
        
    return None

#Inizia la simulazione in mode 3 e chiama la funzione di simulazione per ogni init cond
#Return @listaAttrattori
def start_simulation_mode_3(network, initial_conditions, steps, fin_max):
    attrattori = []
    for initial in initial_conditions:
        attrattori.append(simulate_mode_3(network, initial, steps, fin_max))
    
    return attrattori

#Inizia la simulazione e chiama la funzione di simulazione per ogni init cond
#Return @Lista traiettorie
def start_simulation_normal(network, initial_conditions, steps):
    results = []
    for initial in initial_conditions:
        results.append(simulate_rbn(network, initial, steps))
    
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

def print_result_mode_1(results, n_genes, n_cond):
     # Print the results
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond} \n")
        for i, result in enumerate(results):
            #file.write(f"Initial condition {i+1}: {' '.join(str(x) for x in initial_conditions[i])}\n")
            #file.write(f" Last step : {' '.join(str(x) for x in result[-1])}\n")
            file.write(f"{' '.join(str(x) for x in result[-1])}\n")
            #print()

def print_result_mode_2(results, n_genes, n_cond):
     # Print the results
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond} \n")
        for i, result in enumerate(results):
            for step, state in enumerate(result):
                #print(f" Step {step}: {state}")
                file.write(f"{' '.join(str(x) for x in state)}\n")
            #print()


def print_result_mode_3(attrattori, n_genes, n_cond):
    print("Detected attractors:")
    with open(os.path.join(output_dir, "output_motore.txt"), 'w') as file:
        file.write(f'n_genes: {n_genes} n_cond: {n_cond}\n')
        for attractor, period, step in attrattori:
            file.write(f"{' '.join(str(x) for x in attractor)} \t{period} \t{step}\n")
            print(f"Attractor: {' '.join(str(x) for x in attractor)}, Period: {period}, Step: {step}")


def NW1_find_attractor(mode, n_steps, fin_max):
    # Carichiamo la rete e la sequenza di ocndizioni iniziali
    network, n_genes = load_rete_from_text()
    initial_conditions, n_cond = read_init_conditions()
  
    if mode == 3:
        attrattori = start_simulation_mode_3(network, initial_conditions, n_steps, fin_max)
        print_result_mode_3(attrattori, n_genes, n_cond)




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
    network, n_genes = load_rete_from_text()
    initial_conditions, n_cond = read_init_conditions()
    
    if mode == 1:
        results = start_simulation_normal(network, initial_conditions, n_steps)
        print_result_mode_1(results, n_genes, (n_steps*n_cond))
    elif mode == 2:
        results = start_simulation_normal(network, initial_conditions, n_steps)
        print_result_mode_2(results, n_genes, (n_steps*n_cond))
    elif mode == 3:
        attrattori = start_simulation_mode_3(network, initial_conditions, n_steps, fin_max)
        print_result_mode_3(attrattori, n_genes, n_cond)


