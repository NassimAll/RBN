# RBN - Random Boolean Network

Python tool per la creazione e simulazione di modelli di Reti Booleane Casuali (RBN).

## Descrizione del Progetto

Questo progetto contiene una serie di script per generare, simulare e analizzare modelli di RBN. Ogni script ha uno scopo specifico e produce un output utilizzato dagli script successivi. Esegui gli script nell'ordine elencato per ottenere i risultati desiderati.

---

## Struttura del Progetto

### 1. Generazione della Rete e delle Condizioni Iniziali

- **`generatore.py`**  
  Crea la rete booleana basandosi sui parametri definiti in un file di configurazione. Genera il grafo in formato `.txt`.

- **`generatore_initcond.py`**  
  Genera una lista di condizioni iniziali secondo i parametri specificati nel file di configurazione.

### 2. Simulazione della Rete

- **`motore.py`**  
  Esegue la simulazione della rete utilizzando i parametri iniziali e offre diverse modalità di output:
  - **mode = 1**: Esegue la simulazione per ogni condizione iniziale e restituisce solo lo stato finale.
  - **mode = 2**: Esegue la simulazione per ogni condizione iniziale e restituisce l'intera traiettoria.
  - **mode = 3**: Esegue la simulazione per ogni condizione iniziale e restituisce i nomi degli attrattori rilevati.

- **`RBN_rapporto`**  
  Genera un rapporto dettagliato degli attrattori identificati nelle simulazioni.

- **`espandi_attrattori.py`**  
  Prende in input gli attrattori trovati e ne espande la traiettoria completa per ciascuno.

---

## Versione con Rumore

Questa versione del simulatore include modifiche per tenere conto delle perturbazioni (rumore) sui nodi durante la simulazione.

- **`motore_rumors.py`**  
  Una versione del motore che accetta una lista di soglie di rumore, specificata per ogni nodo.

- **`analizza_nodi.py`**  
  Analizza il comportamento dei nodi in una finestra di tempo specificata. Da eseguire con il comando:
  ```
  bash
  python analizza_nodi.py <finestra>
  ```


---

## Utilizzo

Per l'utilizzo scaricare il progetto e tenere in cosiderazione che:

- I file di input per ciascuno script devono trovarsi nella stessa directory degli script.
- I file di output vengono generati nella stessa directory.