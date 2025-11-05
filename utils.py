import csv





def cognome_to_cf(nome):
    array = []
    nome = nome.upper()
    cons = 0
    if len(nome) >= 3:
        for char in nome:
            if char not in "AEIOU":
                cons += 1
        if cons >= 3:
            for char in nome:
                if char not in "AEIOU":
                    array.append(char)
            nome_cf = array[0] + array[1] + array[2]
        elif cons == 2 or cons == 1:
            for char in nome:
                if char not in "AEIOU":
                        array.append(char)
            for char in nome:
                if char in "AEIOU" and len(array) < 3:
                    array.append(char)
            nome_cf = array[0] + array[1] + array[2]
        else:
            for char in nome:
                array.append(char)
            nome_cf = array[0] + array[1] + array[2]
    match len(nome):
        case 2:
            nome_cf = nome[0] + nome[1] + "X"
        case 1:
            nome_cf = nome[0] + "XX"
    return nome_cf


def nome_to_cf(nome):
    array = []
    nome = nome.upper()
    cons = 0
    vocali = []
    for char in nome:
        if char not in "AEIOU":
            cons += 1
            array.append(char)
    if cons > 3:
        nome_cf = array[0] + array[2] + array[3]
    for char in nome:
        if char in "AEIOU":
            vocali.append(char)
    match cons:
        case 3:
            nome_cf = array[0] + array[1] + array[2]
        case 2:
            if len(vocali) >= 1:
                nome_cf = array[0] + array[1] + vocali[0]
            else:
                nome_cf = array[0] + array[1] + "X"
        case 1:
            if len(vocali) >= 2:
                nome_cf = array[0] + vocali[0] + vocali[1]
            else:
                if len(vocali) == 1:
                    nome_cf = array[0] + vocali[0] + "X"
                else:
                    nome_cf = array[0] + "XX"
        case 0:
            if len(vocali) >= 3:
                nome_cf = vocali[0] + vocali[1] + vocali[2]
            elif len(vocali) == 2:
                nome_cf = vocali[0] + vocali[1] + "X"
            elif len(vocali) == 1:
                nome_cf = vocali[0] + "XX"
    return nome_cf

def anno_to_cf(anno):
    anno_to_str = str(anno)[2:4]
    return anno_to_str


# --- Funzioni gestione mesi per codice fiscale ---
def carica_mesi(file_csv: str) -> dict[str, str]:
    """
    Legge il CSV dei mesi con intestazioni 'Mese,lettera' e restituisce un dict {NomeMese: Lettera}.
    Esempio riga: Gennaio,A
    """
    mappa: dict[str, str] = {}
    with open(file_csv, mode="r", encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        for riga in lettore:
            mese = riga["Mese"].strip()
            lettera = riga["lettera"].strip()
            mappa[mese] = lettera
    return mappa

def _nome_mese_da_numero(n: int) -> str:
    """Converte un numero 1-12 nel corrispondente nome del mese in italiano con iniziale maiuscola."""
    if not (1 <= n <= 12):
        raise ValueError(f"Mese numerico fuori range: {n}")
    nomi = [
        "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
    ]
    return nomi[n - 1]

def mese_to_cf(mese, percorso_csv: str = "mese.csv") -> str:
    """
    Restituisce la lettera del codice fiscale per il mese.
    - 'mese' può essere un int 1-12, uno stringa numerica '1'..'12', o il nome del mese ('gennaio', 'Gennaio', etc.).
    - 'percorso_csv' è il file CSV con intestazioni 'Mese,lettera'.
    Il CSV viene caricato una sola volta e poi riutilizzato (cache interna).
    """
    # cache della mappa mesi->lettera
    if not hasattr(mese_to_cf, "_mappa"):
        mese_to_cf._mappa = carica_mesi(percorso_csv)

    # Normalizza l'input
    if isinstance(mese, int):
        nome = _nome_mese_da_numero(mese)
    else:
        s = str(mese).strip()
        if s.isdigit():
            nome = _nome_mese_da_numero(int(s))
        else:
            nome = s.capitalize()

    try:
        return mese_to_cf._mappa[nome]
    except KeyError:
        raise KeyError(f"Mese '{nome}' non trovato nel CSV '{percorso_csv}'. Assicurati che il file contenga una riga come 'Gennaio,A'.")



def giorno_to_cf(giorno,sesso):
    sesso = sesso.upper()
    match sesso:
        case "M":
            if (giorno) < '10':
                return "0" + str(giorno)
            else:
                return str(giorno)
        case "F":
            (giorno) += 40
            return str(giorno)
        
def _norma_nome(s: str) -> str:
    # normalizza: spazi doppi, apostrofi tipografici, maiuscole/minuscole
    return " ".join(s.strip().replace("’", "'").split()).casefold()



def carica_codici_comuni(percorso_txt: str) -> dict:
    mappa = {}
    with open(percorso_txt, encoding="utf-8") as f:
        for riga in f:
            r = riga.strip()
            if not r:
                continue
            if "\t" in r:
                nome, codice = r.split("\t", 1)
            else:
                nome, codice = r.rsplit(maxsplit=1)
            mappa[_norma_nome(nome)] = codice.strip()
    return mappa



def comune_to_cf(nome_comune: str, percorso_txt: str = "comuni.txt") -> str | None:
    # Carica la mappa solo la prima volta che la funzione viene chiamata
    if not hasattr(comune_to_cf, "_mappa"):
        comune_to_cf._mappa = carica_codici_comuni(percorso_txt)
    return comune_to_cf._mappa.get(_norma_nome(nome_comune))

def lista_codici(percorso_txt: str) -> list[str]:
    codici = []
    with open(percorso_txt, encoding="utf-8") as f:
        for riga in f:
            r = riga.strip()
            if not r:
                continue
            if "\t" in r:
                _, codice = r.split("\t", 1)
            else:
                _, codice = r.rsplit(maxsplit=1)
            codici.append(codice.strip())
    return codici

def carattere_controllo_to_cf(cf: str) -> str:
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