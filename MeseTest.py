cf = "PMPLNZ02L12I921"

def carattere_controllo(cf: str) -> str:
    """
    Calcola il carattere di controllo del codice fiscale.
    Accetta una stringa di 15 (parziale) o 16 caratteri (completo):
    - se 16, usa automaticamente i primi 15 caratteri.
    - se diversa da 15/16, solleva ValueError.
    """
    valori_dispari = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
        'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
        'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
        'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }

    valori_pari = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
        'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
        'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }

    conversione_finale = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = cf.strip().upper()
    if len(s) == 16:
        s = s[:15]
    elif len(s) != 15:
        raise ValueError(f"Lunghezza CF non valida ({len(s)}). Attesi 15 o 16 caratteri.")

    totale = 0
    for i, c in enumerate(s):
        if i % 2 == 0:  # posizioni dispari (1-based)
            totale += valori_dispari[c]
        else:           # posizioni pari (1-based)
            totale += valori_pari[c]

    return conversione_finale[totale % 26]

# Calcola e concatena il codice fiscale completo
cf_completo = cf + carattere_controllo(cf)
print(cf_completo)