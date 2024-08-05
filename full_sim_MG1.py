import random
import os
import numpy as np
import shutil
import statistics
from generatore import main_for_sim, read_param
from generatore_initcond import main_initcond
from motore_rumors import main_for_MG1
#from motore_rumors import simulate_rbn, load_rete_from_text
from analizza_nodi import main_analisi_for_MG1

'''
ESEGUE SU N RETI CON N = 50
INFO SIMULAZIONE
RETI - input generatore: n=20, k=2, bias=0.5
CONDIZIONI INIZIALI : input cond iniziali ?
MOTORE(rumore): 500 step di simulazione, rumori da provare: 0.02, 0.1, 0.2, 0.5
ANALISI FINESTRE: dim_fin = 100

infine per ogni finestra negli insiemi di simulazione stampa: 
NucleoT 	NucleoMin	NucleoMedio	    NucleoMediano	NucleoMax
per ogni nodo diverso in cui viene posto il rumore
'''

dir =  os.getcwd()
path = os.path.join(dir, f"RISULTATI_MG1_50") 
#output_dir = dir + "/resultMG1/"
res_file = os.path.join(path,"MG1_")
analisi_path = os.path.join(dir, "analisi_nodi.txt")
N_reti = 50
n = 50
#PARAMETRI MOTORE
n_steps = 500
mode = 2
#rumore = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
#PARAMETRI ANALISI
fin = 100

def read_analisi_results():
    tab = []
    with open(analisi_path, 'r') as file:
        for line in file:
            riga = list(map(int, line.split()))
            tab.append(riga)
    return tab

def write_intestazione(f_name, message):
     with open(f_name, 'a') as file:
        file.write(message)

def write_stats(f_name, stats):
    with open(f_name, 'a') as file:
        file.write(f"{stats[0]}\t{stats[1]}\t{stats[2]}\t{stats[3]}\t{stats[4]}\n")
        #file.write("\n")

#Per ogni condizione valore nucleo (situazioni fisse) della rete, dati gli n nuclei si calcola media, mediana, max, min
def check_stat_analisi():
    
    #leggiamo la tabella che contiene i risulatati dell'analisi
    res_analysis = read_analisi_results()

    # Calcolo dei nuclei per ogni riga
    nuclei_per_cond = [sum(1 for val in riga if val == fin) for riga in res_analysis]

    # Calcolo del nucleo totale
    nucleo_totale = 0
    for colonna in range(len(res_analysis[0])):
        if all(riga[colonna] == fin for riga in res_analysis):
            nucleo_totale += 1

    # Calcolare min, max, media e mediana dei nuclei per riga
    min_nuclei = min(nuclei_per_cond)
    max_nuclei = max(nuclei_per_cond)
    media_nuclei = statistics.mean(nuclei_per_cond)
    mediana_nuclei = statistics.median(nuclei_per_cond)

        
    return nucleo_totale, min_nuclei, max_nuclei, media_nuclei, mediana_nuclei

#esegue le simulazioni con rumore minimo 0.02
def simulate_with_noise(file_name, val):

    for i in range(n):
        rumore = [0] * n
        rumore[i] = val
        
        #Start motore
        main_for_MG1(mode, rumore, n_steps) #esegue la simulazione e stampa i risultati
        #print(f"SIM GENE {i} OK")
        #Analisi simulazione
        main_analisi_for_MG1(fin, n_steps) # analizza la simulazione e stampa i risultati
        #print(f"ANALISI GENE {i} OK")
        statistiche = check_stat_analisi()

        write_stats(file_name, statistiche)
        #print(f"GENE {i} OK")
    
    with open(file_name, 'a') as file:
        file.write("\n\n")
    return

if __name__ == '__main__':

    #DEFINIAMO QUI I PARAMETRI PER EVITARE UNA CONTINUA LETTURA DEL FILE
    n_nodi = n
    k_minimo = 2
    k_massimo = 2
    probabilita_k = [1.0]
    bias = [0.5]
    n_cond = 1000
    mask = [2] * n_nodi

    #CREAIAMO LA CARTELLA DELLA RETE RELATIVA
    if not os.path.exists(path): 
        os.mkdir(path) 
    
    #generare il grafo per la simulazione - Input fisso nel file
    for i in range(N_reti):
        
        if not main_for_sim(n_nodi, k_minimo, k_massimo, probabilita_k, bias):
            raise ValueError('Si è verificato un errore con la generazione del grafo')

        print("GRAFO OK")
        shutil.copy(os.path.join(dir,'grafo.txt'), os.path.join(path,f'grafo_{i}.txt')) #salvo il grafo

        #GENERARE LE CONDIZIONI INIZIALI - Input fisso nel file
        if not main_initcond(n_nodi, n_cond, 0.5, mask):
            raise ValueError('Si è verificato un errore con la generazione delle condizioni iniziali')

        print("CONDIZIONI INIZIALI OK")
        shutil.copy(os.path.join(dir,'condizioni_iniziali.txt'), os.path.join(path,f'condizioni_iniziali_{i}.txt'))

       #INIZIO SIMULAZIONI
        file_name = res_file + f"_R{i}_res.txt"
        write_intestazione(file_name, f"RETE {i} - rumore = 0.02 \n")
        simulate_with_noise(file_name, 0.02)
        print(f"FINE 0.02")
        write_intestazione(file_name, f"RETE {i} - rumore = 0.1 \n")
        simulate_with_noise(file_name, 0.1)
        print(f"FINE 0.1")
        write_intestazione(file_name, f"RETE {i} - rumore = 0.2 \n")
        simulate_with_noise(file_name, 0.2)
        print(f"FINE  0.2")
        write_intestazione(file_name, f"RETE {i} - rumore = 0.5 \n")
        simulate_with_noise(file_name, 0.5)

        print(f"FINE RETE {i}")

