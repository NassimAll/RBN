#Leggiamo i parametri in input dal file
def read_param():
    with open(input_file, 'r') as file:
        # Legge tutte le righe del file
        lines = file.readlines()

    # Estrae i valori delle variabili
    n_genes = int(lines[0].split(":")[1].strip())
    n_cond = int(lines[1].split(":")[1].strip())
