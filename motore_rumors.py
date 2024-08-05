#VERSIONE DEL MOTORE CHE TIENE CONTO DEL RUMORE AL MOMENTO DELLA SIMULAZIONE

import json
import os
import numpy as np
import random

#Definizione file con dati in input
input_motore =  os.getcwd() + "/input_motore_rumors.txt"
input_grafo_txt =  os.getcwd() + "/grafo.txt"
input_condInit =  os.getcwd() + "/condizioni_iniziali.txt"
output_dir = os.getcwd()

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
            # Convertiamo ogni array in una stringa binaria
            lista_stringhe_binarie = [array_to_binary_string(arr) for arr in period_states]
            max_state = max(lista_stringhe_binarie)

            return tuple(max_state), abs(periodo), (first_occurrence - abs(periodo))
        
        stati_to_index[stato] = index
        
    return None, None, None

#Avvia la simulazione per ogni cond init, ed esegue la logica del rumore
#logica rumore: 
# - theshold_noise: lista sogllie di rumore inserite da utente
# Per ogni nodo si genera un valore casuale che aziona l'inversione del risultato se è minore della soglia specificata
def simulate_rbn(network, initial_cond, steps, theshold_noise):
    state = np.array(initial_cond) #Carico lo stato iniziale
    traiettoria = [state.copy()] #inizializzo la traiettoria al primo stato

    for _ in range(steps):
        new_state = state.copy() # Inizializzo stato successivo
        for node, info in network.items(): # Calcolo lo stato per ogni singolo nodo
            node = int(node)
            ingressi = info['ingressi'] # nodi in ingresso
            uscite = info['uscite'] # tabella delle uscite
            inputs = [state[i] for i in ingressi] # carico il valore degli ingressi nel nodo, in ordine
            new_state[node] = boolean_function_output(inputs, uscite) # funzione per calcolare il valore dell'uscita
            #Dopo aver calcolato l'uscita controllo se il rumore ha interferito
            if theshold_noise[node] > 0:
                # Generare un numero casuale reale tra 0 e 1 che identifica il rumore attuale
                noise = random.random()
                #print(f" Controllo nodo {node}, control: {noise} < {theshold_noise[node]}\n")
                #print(f" Stato pre controllo: {new_state[node]} \n")
                if noise < theshold_noise[node]:    #Controllo se supera o meno la soglia 
                    new_state[node] = 1 if new_state[node] == 0 else 0 # Se era 1 diventa 0 se era 0 diventa 1 
                #print(f" Stato post controllo: {new_state[node]} \n")

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
def start_simulation_normal(network, initial_conditions, steps, noise):
    results = []
    for initial in initial_conditions:
        results.append(simulate_rbn(network, initial, steps, noise))
    
    return results


#Reading from file motore parameters, n_step - mode - finamx - ruors_list
def read_parametri():
    parametri = {}
    with open(input_motore, 'r') as file:
        lines = file.readlines()
    
    # Estrae i valori delle variabili
    n_steps = int(lines[0].split(":")[1].strip())
    mode = int(lines[1].split(":")[1].strip())
    finamx = int(lines[2].split(":")[1].strip())
    
    # Legge la lista dei rumori per ogni nodo, sono una lista di reali
    rumors = list(map(float, lines[3].split(":")[1].strip().split()))

    return n_steps, mode, finamx, rumors

#Reading the set of initial conditions
def read_init_conditions():
    with open(input_condInit, 'r') as file:
        lines = file.readlines()
    
    n_genes, n_cond = map(int, lines[0].strip().split()[1::2])
    initial_conditions = [list(map(int, line.split())) for line in lines[1:]]
    
    return initial_conditions, n_cond

def print_result_mode_1(results, n_genes, n_cond):
     # Print the results
    with open(os.path.join(output_dir, "output_motore_rumore.txt"), 'w') as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond} \n")
        for i, result in enumerate(results):
            file.write(f"{' '.join(str(x) for x in result[-1])}\n")

def print_result_mode_2(results, n_genes, n_cond):
     # Print the results
    with open(os.path.join(output_dir, "output_motore_rumore.txt"), 'w') as file:
        file.write(f"n_genes: {n_genes} n_cond: {n_cond} \n")
        for i, result in enumerate(results):
           for step, state in enumerate(result):
                file.write(f"{' '.join(str(x) for x in state)}\n")
           #file.write("\n")


def print_result_mode_3(attrattori, n_genes, n_cond):
    print("Detected attractors:")
    with open(os.path.join(output_dir, "output_motore_rumore.txt"), 'w') as file:
        file.write(f'n_genes: {n_genes} n_cond: {n_cond}\n')
        for attractor, period, step in attrattori:
            file.write(f"{' '.join(str(x) for x in attractor)} \t{period} \t{step}\n")
            print(f"Attractor: {' '.join(str(x) for x in attractor)}, Period: {period}, Step: {step}")

def check_parametri(mode, noise, n_genes): 
    
    rumor = len(noise)
    if rumor != n_genes:
        raise ValueError("Hai inserito una lista di rumori di dimensione differenti dal numero di geni in esame")

    arr = np.array(noise) #trasformo in np array perché più facile da trattare
    if mode == 3:
        # Verificare se tutti gli elementi dell'array sono zero
        is_all_zeros = np.all(arr == 0)
        if not is_all_zeros:
            raise ValueError("Non possiamo avere rumori diversi da 0 se vogliamo trovare degli attrattori")
        
    return True

def main_for_MG1(mode, noise, n_steps):
     # Carichiamo la rete e la sequenza di ocndizioni iniziali
    network, n_genes = load_rete_from_text()
    initial_conditions, n_cond = read_init_conditions()
  
    results = start_simulation_normal(network, initial_conditions, n_steps, noise)
    print_result_mode_2(results, n_genes, (n_steps*n_cond))

if __name__ == "__main__":

    # Carichiamo i parametri del motore
    n_steps, mode, fin_max, noise = read_parametri()

    print(f"mode = {mode}")
    print(f"Lista rumori: {noise}")
    
    # Carichiamo la rete e la sequenza di ocndizioni iniziali
    network, n_genes = load_rete_from_text()
    initial_conditions, n_cond = read_init_conditions()

    if check_parametri(mode, noise, n_genes):
        print("Parametri input OK")
    
    if mode == 1:
        results = start_simulation_normal(network, initial_conditions, n_steps, noise)
        print_result_mode_1(results, n_genes, (n_steps*n_cond))
    elif mode == 2:
        results = start_simulation_normal(network, initial_conditions, n_steps, noise)
        print_result_mode_2(results, n_genes, (n_steps*n_cond))
    elif mode == 3:
        attrattori = start_simulation_mode_3(network, initial_conditions, n_steps, fin_max)
        print_result_mode_3(attrattori, n_genes, n_cond)


