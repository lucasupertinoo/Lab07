from database.biblioteca_DAO import BibliotecaDAO
from database.libro_DAO import LibroDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Si occupa di interrogare il DAO (chiama i metodi di BibliotecaDAO e LibroDAO)
    - Non sa nulla dell'interfaccia grafica: riceve valori semplici e restituisce liste di DTO
'''

class Model:
    def __init__(self):
        # Creo un'istanza di ciascun DAO e la tengo come attributo "privato" (underscore iniziale)
        # Qua viene eseguito l'init delle due classi e dunque rimane salvato un riferimento a DB Connect
        self._biblioteca_dao = BibliotecaDAO()
        self._libro_dao = LibroDAO()

    # --- LIBRI ---
    def get_libri_filtrati(self, biblioteca:str, genere:str):   # Vengono passati come argomenti gli input da flet dell'utente
        """Restituisce la lista di tutti i libri filtrati per biblioteca e/o genere (filtri opzionali).
        - biblioteca: la KEY scelta nel dropdown biblioteche, cioè l'id come stringa,
                      oppure "Nessun filtro", oppure None se l'utente non ha ancora scelto nulla
        - genere:     il nome del genere (es. "Giallo"), oppure "Nessun filtro", oppure None
        """

        libri = self._libro_dao.get_libro()
        risultato = []  # Preparo la lista che conterrà solo i libri che superano i filtri


        for libro in libri:
            check_biblioteca = True # Filtro biblioteca: parto dal presupposto che il libro vada bene (True)
            # Il filtro è attivo solo se l'utente ha scelto una biblioteca vera (biblioteca è definito nelle () a riga 19)
            if biblioteca is not None and biblioteca != "Nessun filtro":    # Controlla che ci sia una selezione dell'utente
                # Confronto come stringhe: id_biblioteca nel DTO è int, la key del dropdown è str
                if str(libro.id_biblioteca) != str(biblioteca): # Se il libro non è nella biblioteca lo scarto
                    check_biblioteca = False

            # Stessa logica del filtro biblioteca
            check_genere = True
            if genere is not None and genere != "Nessun filtro":
                if libro.genere != genere:   # Genere diverso da quello scelto -> scarto il libro
                    check_genere = False

            # Il libro entra nel risultato solo se supera ENTRAMBI i controlli.
            if check_biblioteca and check_genere:
                risultato.append(libro)

        return risultato

    def get_generi(self):
        """Restituisce la lista di tutti i generi (senza duplicati, in ordine alfabetico).
        Serve per popolare il dropdown dei generi."""

        libri = self._libro_dao.get_libro()
        generi = []
        for libro in libri:
            if libro.genere and libro.genere not in generi: # Significa "se il genere esiste e non è nella lista"
                generi.append(libro.genere)

        return sorted(generi)

    # --- BIBLIOTECHE ---
    def get_biblioteche(self):
        """ Restituisce la lista di tutte le biblioteche (oggetti Biblioteca), letta tramite il DAO."""
        return self._biblioteca_dao.get_biblioteca()