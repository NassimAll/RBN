'''
NW1
- per ogni rete (k=2, bias=0.5, N=20)
    --- trovare gli stati degli attrattori
    --- introdurre un basso rumore in ogni nodo
    --- per ogni stato di ogni traiettoria, identificare l'attrattore più vicino e la distanza minima
    --- alzare la frequenza del rumore, e rifare
  -- farlo per N reti

  1. Lanciaree motore mode 3 senza rumore e salvare gli attrattori in un file temporaneo
  2. aggiungere rumore in ogni nodo partendo da 1/20, poi aumentarlo progessivamente fino a notare una variazione sostanziale
  3. Data una traiettoria rumorosa, vogliamo vedere come si muove rispetto a come si muove se avrebbe rumore.
    Etichettiamo ogni stato. Tag per ogni attrattore, controllo la traiettoria e verifico la distanza tra lo stato e il possibile attratto.
    Cerchiamo la distanza di hamming più piccola da ogni stato dell’attrattore e la associo. 

'''

import random
import os
import numpy as np
import shutil
import statistics
import itertools
from generatore import main_for_sim
from generatore_initcond import main_initcond
from motore import NW1_find_attractor
import RBN_rapporto
import espandi_attrattori 
from motore_rumors import main_for_MG1


#current directory
dir =  os.getcwd()
#path for result
path = os.path.join(dir, f"dati") 
reti = 50


# Funzione per calcolare la distanza di Hamming tra due stati
def distanza_hamming(stato1, stato2):
    return np.sum(stato1 != stato2)


def get_attrattori():
    attrattori = []
    traiettoria_corrente = []
    
    with open(os.path.join(dir, f"attrattori_espansi.txt") , 'r') as file:
        # Salta la prima riga (header)
        next(file)
        
        for line in file:
            # Rimuovi eventuali spazi bianchi all'inizio e alla fine
            line = line.strip()
            if line:
                # Converti la riga in un array numpy di interi
                riga = np.array(list(map(int, line.split())))
                # Aggiungi la riga alla traiettoria corrente
                traiettoria_corrente.append(riga)
            else:
                # Se trovi una linea vuota, salva la traiettoria e resetta la lista corrente
                if traiettoria_corrente:
                    attrattori.append(traiettoria_corrente)
                    traiettoria_corrente = []

        # Aggiungi l'ultima traiettoria se il file non termina con una linea vuota
        if traiettoria_corrente:
            attrattori.append(traiettoria_corrente)

    return attrattori


def analisi(traiettorie):

    attrattori = get_attrattori()

    risultati = []

    for x, stato in enumerate(traiettorie):
        distanze_minime = set()
        distanza_minima = float('inf')
        
        # Confronta con ogni traiettoria degli attrattori
        for i, traiettoria_attrattore in enumerate(attrattori):
            for stato_attrattore in traiettoria_attrattore:
                distanza = distanza_hamming(stato, stato_attrattore)
                
                # Se troviamo una distanza minore, aggiorniamo la lista delle distanze minime
                if distanza < distanza_minima:
                    distanza_minima = distanza
                    distanze_minime = {i}  # Salva l'indice dell'attrattore
                # Se la distanza è uguale alla distanza minima, aggiungi l'indice dell'attrattore
                elif distanza == distanza_minima:
                    distanze_minime.add(i)
        
        # Aggiungi l'indice dell'attrattore (o attrattori) più simile/i e la distanza minima al risultato
        risultati.append((stato, distanze_minime, distanza_minima))

    return risultati

def print_results(res_analisi, name):
    # Print the results
    with open(name, 'w') as file:
        for (stato, attrattori, dist) in res_analisi:
            file.write(f"{' '.join(str(x) for x in stato)} \t {dist} \t {' '.join(str(x) for x in list(attrattori))}\n")

           #file.write("\n")

def main():

    #DEFINIAMO QUI I PARAMETRI PER EVITARE UNA CONTINUA LETTURA DEL FILE
    n_nodi = 20
    k_minimo = 2
    k_massimo = 2
    probabilita_k = [1.0]
    bias = [0.5]
    n_cond = 1000
    mask = [2] * n_nodi

    #result folder
    if not os.path.exists(path): 
        os.mkdir(path) 
    
    for i in range(reti):
        #create rbn 
        if not main_for_sim(n_nodi, k_minimo, k_massimo, probabilita_k, bias):
            raise ValueError('Si è verificato un errore con la generazione del grafo')
        
        shutil.copy(os.path.join(dir,'grafo.txt'), os.path.join(path,f'grafo{i}.txt')) #salvo il grafo

        #Generate init conditions
        if not main_initcond(n_nodi, n_cond, 0.5, mask):
            raise ValueError('Si è verificato un errore con la generazione delle condizioni iniziali')

        #PARAMETRI MOTORE
        n_steps = 500
        mode = 3 
        finmax = 100

        #get attractors
        NW1_find_attractor(mode, n_steps, finmax)
        RBN_rapporto.main()
        espandi_attrattori.main()

        shutil.copy(os.path.join(dir,'attrattori_espansi.txt'), os.path.join(path,f'attrattori{i}.txt'))

        #Ottenuti glli attrattori e la loro traiettoria simuliamo aggiungendo rumore in ogni nodo 

        #Primo tentativo rumore = 1/20 = 0.05
        rumore = [0.05] * n_nodi
        mode = 2
        #simulate with noise
        traiettorie = main_for_MG1(mode, rumore, n_steps)
        # Unire tutte le sottoliste in una sola lista
        traiettorie = list(itertools.chain(*traiettorie))

        shutil.copy(os.path.join(dir,'output_motore_rumore.txt'), os.path.join(path,f'traiettorie_min{i}.txt'))

        print('INIZIO ANALISI')

        result = analisi(traiettorie)

        out_dir = os.path.join(os.getcwd(), 'res_min')
         #result folder
        if not os.path.exists(out_dir): 
            os.mkdir(out_dir) 

        file_res = os.path.join(out_dir, f"distanza_attrattori{i}.txt") 

        print_results(result, file_res)

        #Secondo tentativo rumore = 1/20 = 0.1
        rumore = [0.1] * n_nodi
        mode = 2
        #simulate with noise
        traiettorie = main_for_MG1(mode, rumore, n_steps)
        # Unire tutte le sottoliste in una sola lista
        traiettorie = list(itertools.chain(*traiettorie))

        shutil.copy(os.path.join(dir,'output_motore_rumore.txt'), os.path.join(path,f'traiettorie_01_{i}.txt'))

        print('INIZIO ANALISI')

        result = analisi(traiettorie)

        out_dir =  os.path.join(os.getcwd(), 'res_01')
         #result folder
        if not os.path.exists(out_dir): 
            os.mkdir(out_dir) 

        file_res = os.path.join(out_dir, f"distanza_attrattori{i}.txt") 

        print_results(result, file_res)

    #Secondo tentativo rumore = 1/20 = 0.1
        rumore = [0.2] * n_nodi
        mode = 2
        #simulate with noise
        traiettorie = main_for_MG1(mode, rumore, n_steps)
        # Unire tutte le sottoliste in una sola lista
        traiettorie = list(itertools.chain(*traiettorie))

        shutil.copy(os.path.join(dir,'output_motore_rumore.txt'), os.path.join(path,f'traiettorie_02_{i}.txt'))

        print('INIZIO ANALISI')

        result = analisi(traiettorie)

        out_dir =  os.path.join(os.getcwd(), 'res_02')
         #result folder
        if not os.path.exists(out_dir): 
            os.mkdir(out_dir) 

        file_res = os.path.join(out_dir, f"distanza_attrattori{i}.txt") 

        print_results(result, file_res)

        #quarto tentativo rumore = 1/20 = 0.5
        rumore = [0.5] * n_nodi
        mode = 2
        #simulate with noise
        traiettorie = main_for_MG1(mode, rumore, n_steps)
        # Unire tutte le sottoliste in una sola lista
        traiettorie = list(itertools.chain(*traiettorie))

        shutil.copy(os.path.join(dir,'output_motore_rumore.txt'), os.path.join(path,f'traiettorie_05_{i}.txt'))

        print('INIZIO ANALISI')

        result = analisi(traiettorie)

        out_dir =  os.path.join(os.getcwd(), 'res_05')
         #result folder
        if not os.path.exists(out_dir): 
            os.mkdir(out_dir) 

        file_res = os.path.join(out_dir, f"distanza_attrattori{i}.txt") 

        print_results(result, file_res)

        #Secondo tentativo rumore = 1/20 = 0.1
        rumore = [0.7] * n_nodi
        mode = 2
        #simulate with noise
        traiettorie = main_for_MG1(mode, rumore, n_steps)
        # Unire tutte le sottoliste in una sola lista
        traiettorie = list(itertools.chain(*traiettorie))

        shutil.copy(os.path.join(dir,'output_motore_rumore.txt'), os.path.join(path,f'traiettorie_07_{i}.txt'))

        print('INIZIO ANALISI')

        result = analisi(traiettorie)

        out_dir =  os.path.join(os.getcwd(), 'res_07')
         #result folder
        if not os.path.exists(out_dir): 
            os.mkdir(out_dir) 

        file_res = os.path.join(out_dir, f"distanza_attrattori{i}.txt") 

        print_results(result, file_res)



if __name__ == '__main__':

    main()

    




