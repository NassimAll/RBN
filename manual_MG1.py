import random
import os
import numpy as np
import shutil
import statistics
from generatore import main_for_sim
from generatore_initcond import main_initcond
from motore_rumors import main_for_MG1
#from motore_rumors import simulate_rbn, load_rete_from_text
from analizza_nodi import main_analisi_for_MG1

'''
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
output_dir = dir + "/resultMG1/G11/"
res_file = os.path.join(output_dir,"MG1_res")
analisi_path = os.path.join(dir, "analisi_nodi.txt")
n = 20
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
     with open(f_name, 'w') as file:
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
    print(max_nuclei)
    print(nuclei_per_cond)
    media_nuclei = statistics.mean(nuclei_per_cond)
    mediana_nuclei = statistics.median(nuclei_per_cond)

    # print("Nuclei per riga:", nuclei_per_cond)
    # print("Nucleo totale:", nucleo_totale)
        
    return nucleo_totale, min_nuclei, max_nuclei, media_nuclei, mediana_nuclei

#esegue le simulazioni con rumore minimo 0.02
def simulate_with_noise(file_name, val):

    rumore = [0] * n
    rumore[10] = val
    
    #Start motore
    main_for_MG1(mode, rumore, n_steps) #esegue la simulazione e stampa i risultati
    #Analisi simulazione
    main_analisi_for_MG1(fin, n_steps) # analizza la simulazione e stampa i risultati

    shutil.copy(os.path.join(dir,'analisi_nodi.txt'), os.path.join(output_dir,f'analisi_nodi_{val}.txt'))
    statistiche = check_stat_analisi()

    write_stats(file_name, statistiche)

    with open(file_name, 'a') as file:
        file.write("\n")
    return

if __name__ == '__main__':
    
    #generare il grafo per la simulazione - Input fisso nel file
    # if not main_for_sim():
    #     raise ValueError('Si è verificato un errore con la generazione del grafo')

    # print("GRAFO OK")
    # shutil.copy(os.path.join(dir,'grafo.txt'), output_dir)

    # #GENERARE LE CONDIZIONI INIZIALI - Input fisso nel file
    # if not main_initcond():
    #     raise ValueError('Si è verificato un errore con la generazione delle condizioni iniziali')

    # print("CONDIZIONI INIZIALI OK")
    # shutil.copy(os.path.join(dir,'condizioni_iniziali.txt'), output_dir)

    #INIZIO SIMULAZIONI
    # file_name = res_file + f"_R1_min_noise.txt"
    # write_intestazione(file_name, "RETE 1 - rumore = 0.02 \n")
    # simulate_with_noise(file_name, 0.02)

    # file_name = res_file + f"_R1_01_noise.txt"
    # write_intestazione(file_name, "RETE 1 - rumore = 0.1 \n")
    # simulate_with_noise(file_name, 0.1)

    # file_name = res_file + f"_R1_02_noise.txt"
    # write_intestazione(file_name, "RETE 1 - rumore = 0.1 \n")
    # simulate_with_noise(file_name, 0.2)

    file_name = res_file + f"_R1_05_noise.txt"
    write_intestazione(file_name, "RETE 1 - rumore = 0.5 \n")
    simulate_with_noise(file_name, 0.5)


