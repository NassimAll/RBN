# RBN - Random boolean network 

Progetto composto da 3 file: 

- generatore.py: questo file genera la rete booleana leggendo le caratteristiche dal file input nella sua apposita cartella. Lo script genera il grafo su due file differenti, uno in formato json e uno in formato testuale
- generatore_initcond.py: leggendo sempre da input i suoi parametri genera una lista di condizioni iniziali 
- motore.py: il motore effettua la simulazione su 3 modalità differenti e genera a seconda di essi un output. 
- RBN_rapporto
- espandi_attrattori.py: dati gli attrattori trovati li espande trovando la traiettoria di ciascuno 

Simulatore che tiene conto del rumore, è stata eseguita una modifica su determinati file per tenere conto di possibili perturbazioni nella simulazione:
- motore_rumors.py: modificando gli input inserendo una lista di soglie di rumore per ogni nodo 
- analizza_nodi.py: passando da linea di comando il valore della finestra lo script preleva per ogni traiettoria una finestra (a partire dal fondo). Di questa finestra vengono analizzati i singoli nodi in modo da dedurre il loro comportamento. 

I file di input per ogni script sono contenuti nella relatica cartella input, e gli output invece sono nella relativa cartella output. 

Per ogni script i percorsi dei file di sono definiti all'inizio e sono inseriti in modo da funzionare su ogni macchina