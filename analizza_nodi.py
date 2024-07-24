
'''
Script di analisi:
Lo scopo di questo script è analizzare la traiettoria che assume ogni singolo nodo in una determinata finestra massima, con lo'obiettibo
di rilevare determinate caratteristiche. 
possiamo rilevare se un nodo:
- è regolare
- è irregolare
- è periodico
- è costante
Queste caratteristiche sono deducibili dai pattern che vengono rilevati nella finestra di osservazione definita.
'''

import os
import numpy as np
import argparse
#from motore_rumors import 

input_motore =  os.getcwd() + "/input_motore_rumors.txt"
input_traiettorie =  os.getcwd() + "/output_motore_rumore.txt"
out_res =  os.getcwd() + "/analisi_nodi.txt"
out_fin =  os.getcwd() + "/fin_di_analisi.txt"


#Reading from file motore parameters, n_step
def get_Nsteps():
    with open(input_motore, 'r') as file:
        lines = file.readlines()
    
    # Estrae i valori delle variabili
    n_steps = int(lines[0].split(":")[1].strip())

    return n_steps

#Reading from file motore parameters, n_step
def get_traiettorie(len_trj):
    with open(input_traiettorie, 'r') as file:
        # Leggi la prima riga per ottenere n_genes e n_cond
        first_line = file.readline().strip()
        n_genes, n_cond = map(int, first_line.split()[1::2])
        
        # Inizializza una lista per memorizzare tutte le traiettorie, e una temporanea per la corrente
        result = []
        tr_corrente = []
        
        # Leggi le righe successive per ottenere le stringhe binarie
        for line in file:
            state = list(map(int, line.strip().split()))
            tr_corrente.append(state)
            
            # Se la lunghezza corrente della traiettoria raggiunge len_trj la salva
            if len(tr_corrente) == len_trj:
                result.append(tr_corrente.copy())
                # Rimuovi il primo stato per far spazio al prossimo
                tr_corrente.clear()
    
    return result

#Funzione di analisi del singolo nodo, restituisce il periodo del pattern e il numero di passi in cui si ripete 
def analyze_node(node):
    lunghezza = len(node)
    max_ripetizioni = 0 #numero di passi 
    pattern_migliore = None

    # Scorre i possibili pattern dal basso verso l'alto e ci si ferma a metà
    for n in range(1, lunghezza // 2 + 1):
        ripetizioni = 1 #numero di passi 
        pattern_corrente = node[-n:]  # Pattern di lunghezza n caratteri partendo dal fondo
        #print(pattern_corrente)
        i = lunghezza - n

        # Risali la colonna per trovare ripetizioni consecutive
        while i >= n and np.array_equal(node[i-n:i], pattern_corrente):
            #print(node[i-n:i])
            ripetizioni += 1
            i -= n

        #print(ripetizioni)

        # Verifica se è il pattern con la ripetizione maggiore
        if ripetizioni > max_ripetizioni:
            max_ripetizioni = ripetizioni
            pattern_migliore = pattern_corrente
        
        #print(max_ripetizioni)
        
        #Se ho trovato un pattern valido per tutta la finestra di analisi posso interrompere l'analisi
        if max_ripetizioni == lunghezza or max_ripetizioni*len(pattern_migliore) == lunghezza:
            break
    
    #trasformare il le ripetiizoni nel numero di passi per l'output successivo
    if len(pattern_migliore) != 1:
        max_ripetizioni *= len(pattern_migliore)

    if len(pattern_migliore) == 1:
        stato = "COSTANTE "
    else:
        stato = "PERIODICO "
    
    if max_ripetizioni == lunghezza:
        stato += "REGOLARE"
    else: stato += "IRREGOLARE"


    res = {
        "pattern": pattern_migliore,
        "passi": max_ripetizioni,
        "periodo": len(pattern_migliore),
        "stato": stato
    }

    return res

def analyze_fin(fin_to_analyze):
    # Converto la finestra (lista di liste) in una matrice NumPy per faciilità di utilizzo
    fin = np.array(fin_to_analyze)

    write_fin(fin)

    result = [] # lista dei risultati per ogni nodo 
    
    for n in range(fin.shape[1]):
        node = fin[:, n] # Prelevo la lista degli stati del singolo nodo
        # Esegui l'analisi desiderata su ogni colonna
        #print(f"Nodo {n}: {node}")
        result.append(analyze_node(node))

    return result

#Analisi delle traiettorie
def analyze_all(traiettorie, fin):
    results = [] # lista che contiene i risultati per ogni traiettoria 

    for t in traiettorie:
        fin_to_analyze = t[len(t)-fin:len(t)] #Prelevo la finestra da ogni traiettoria
        #[print(x) for x in fin_to_analyze]

        results.append(analyze_fin(fin_to_analyze))

        #print("\n")
    return results

#Scrive i risultati dell'analisi su analisi_nodi.txt
def write_results(results):
    with open(out_res, 'w') as file:
        for tr in results: # Per ogni traiettoria
            for i, node in enumerate(tr): # Per ogni nodo della traiettoria
                file.write(f"gene: {i} \t Periodo: {node["periodo"]} \t Passi: {node["passi"]} \t Pattern: {node["pattern"]}\t Stato: {node["stato"]}.\n")
            file.write("\n")

#Scrive la finestra di analisi di ogni traiettoria in fin_di_analisi.txt
def write_fin(fin):
    with open(out_fin, 'a') as file:
        for line in range(fin.shape[0]):
            file.write(f"{" ".join(str(x) for x in fin[line, :])}\n")
        file.write("\n")

if __name__ == '__main__':

    #Remove dei file per stampare i nuovi risultati
    if os.path.exists(out_fin) and os.path.exists(out_res): 
        os.remove(out_fin) 
        os.remove(out_res) 

    #Leggere i parametri di analisi - fin_analysis
    parser = argparse.ArgumentParser(description="Script di analisi riconoscitore di nodi rumorosi")
    parser.add_argument("fin", type=int, default=0, help="Dimensione della finestra di analisi")

    args = parser.parse_args()
    print(f"Finestra di analisi = {args.fin}\n")

    #Leggere da input motore, per avere n_steps
    n_steps = get_Nsteps()
    print(f"Lunghezza singola traiettoria = {n_steps}\n")

    #Leggere le traiettorie del motore - lista traiettoria per ogni cond init
    traiettorie = get_traiettorie(n_steps + 1) # n_steps + 1 perche per ogni condizinone si deve considerare la prima cond iniziale

    #FASE DI ANALISI
    results = analyze_all(traiettorie, args.fin)
    
    #Stampa risultati su file
    write_results(results)