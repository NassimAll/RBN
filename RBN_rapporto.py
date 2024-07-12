# -*- coding: utf-8 -*-
#import shutil
import os

out_motore = os.path.join(os.getcwd() + "/output_motore.txt")
out_rapporto = os.path.join(os.getcwd() + "/output_motore_rapporto.txt")


"""File per trovare attrattori"""

def leggi_output_motore_mod3():
    try:
        f = open(out_motore, 'r')
    except Exception as e:
        print(e)
     
    line = f.readline().split()
    nnodi=eval(line[1])
    ncond=eval(line[3])
    #print(nnodi,ncond)

    line = f.readline()

    per=[]
    mat=[]
    while line != "":
        tmp=[]
        #print(line.split())
        for el in line.split():
            tmp+=[eval(el)]
        #print(tmp)
        linetmp1 = tmp[:nnodi]
        linetmp2 = tmp[nnodi:]
        mat+=[linetmp1]
        per+=[linetmp2[0]]
        line = f.readline()
        
    f.close()

    return nnodi, ncond, mat, per


"""
def leggi_output_motore_mod3():
    try:
        f = open("output_motore.txt", 'r')
    except Exception as e:
        print(e)

    line = f.readline()
    nodicond = [int(s) for s in line.split() if s.isdigit()]
    del line
    nnodi = nodicond[0]
    ncond = nodicond[1]
    del nodicond
    mat = [[0 for x in range(nnodi)] for y in range(ncond)]
    per = []
    for i in range(ncond):
        #linetmp = f.readline().strip()
        linetmp = f.readline().split()
        print(linetmp)
        linetmp1 = linetmp[:nnodi*2]
        linetmp2 = linetmp[nnodi*2:]
        print("ORA")
        print(linetmp1)
        print(linetmp2)
        del linetmp
        bitlist = [int(s) for s in linetmp1.split()]# if s.isdigit()]
        perlist = [int(s) for s in linetmp2.split()]# if s.isdigit()]
        print(len(bitlist),len(perlist))
        print(bitlist)
        print(perlist)
        del linetmp1
        del linetmp2
        per.append(perlist[0])
        for j in range(nnodi):
            mat[i][j] = bitlist[j]

    del bitlist
    del perlist
    f.close()

    return nnodi, ncond, mat, per
"""

def confronta_vettori_int(v1, v2, n):
    for i in range(n):
        if v1[i] != v2[i]:
            return 0
    return 1

def stampa_file_vettore_int(f, v, n):
    for i in range(n):
        f.write(str(v[i]) + " ")

def stampa_rapporto(n_attr, nnodi, ncond, elenco, mat, per, bacini):
    try:
        f = open(out_rapporto, 'w')
    except Exception:
        print("File output_motore_rapporto.txt non aperto\n")

    f.write("Attrattori: " + str(n_attr) + "   geni: " + str(nnodi) + "\n")

    j = 0
    for i in range(ncond):
        if elenco[i]:
            stampa_file_vettore_int(f, mat[i], nnodi)
            calc = bacini[j]/float(ncond)
            calc2 = "{:.6f}".format(calc)
            del calc
            f.write(" " + str(per[i]) + " " + str(calc2) + "\n")
            j += 1
    f.close()

def main():
    nnodi, ncond, mat, per = leggi_output_motore_mod3()

    
    # Alloco elenco
    elenco = []
    for i in range(ncond):
        elenco.append(1)

    # Elimino doppioni
    for i in range(ncond):
        if elenco[i]:
            for j in range(i+1, ncond, 1):
                if elenco[j]:
                    if confronta_vettori_int(mat[i], mat[j], nnodi):
                        elenco[j] = 0

    # Calcolo numero attrattori
    n_attr = 0
    for i in range(ncond):
        if elenco[i]:
            n_attr += 1

    print("Numero Attrattori: " + str(n_attr))

    k = 0
    # Alloco bacini
    bacini = []
    for i in range(n_attr):
        bacini.append(0)

    for i in range(ncond):
        if k < n_attr:
            bacini[k] = 1
        if elenco[i]:
            # Conto il numero di vettori uguali al vettore modello
            for j in range(i+1, ncond, 1):
                if confronta_vettori_int(mat[i], mat[j], nnodi):
                    bacini[k] += 1
            k += 1

    if k > n_attr:
        print("ALLARME n_attrattori: " + str(n_attr) + " j: " + str(k) + "\n")

    print("bacini attrazione:\n")
    for i in range(n_attr):
        print(bacini[i])
    print("\n")

    stampa_rapporto(n_attr, nnodi, ncond, elenco, mat, per, bacini)


if __name__=="__main__":
    main()
