
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



if __name__ == '__main__':

    #Leggere i parametri di analisi - fin_analysis
    parser = argparse.ArgumentParser(description="Script di analisi riconoscitore di nodi rumorosi")
    parser.add_argument("fin", type=int, default=0, help="Dimensione della finestra di analisi")

    args = parser.parse_args()
    print(f"fin_analysis = {args.fin}\n")

    #Leggere da input motore, per avere n_steps
    n_steps = get_Nsteps()
    print(f"steps tr = {n_steps}\n")

    #Leggere le traiettorie del motore - lista traiettoria per ogni cond init
    traiettorie = get_traiettorie(n_steps + 1)

    #TO DO - AGGIUNGERE FASE DI ANALISI
