from utils import cognome_to_cf, nome_to_cf, anno_to_cf, mese_to_cf, giorno_to_cf, comune_to_cf, carattere_controllo_to_cf

cognome = input("Inserisci il cognome: ")
nome = input("Inserisci il nome: ")
anno = input("Inserisci l'anno di nascita: ")
mese = input("Inserisci il mese di nascita: ")
giorno = input("Inserisci il giorno di nascita: ")
comune = input("Inserisci il comune di nascita: ")
sesso = input("Inserisci il sesso (M/F): ")

cf = (
    cognome_to_cf(cognome)
    + nome_to_cf(nome)
    + anno_to_cf(anno)
    + mese_to_cf(mese)
    + giorno_to_cf(giorno, sesso)
    + comune_to_cf(comune)
)
cf = cf + carattere_controllo_to_cf(cf)
print("Codice Fiscale completo:", cf)