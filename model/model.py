from database.biblioteca_DAO import BibliotecaDAO
from database.libro_DAO import LibroDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Si occupa di interrogare il DAO (chiama i metodi di BibliotecaDAO e LibroDAO)
'''

class Model:
    def __init__(self):
        self._biblioteca_dao = BibliotecaDAO()
        self._libro_dao = LibroDAO()

    # --- LIBRI ---
    def get_libri_filtrati(self, biblioteca:str, genere:str):   # Vengono passati come argomenti gli input da flet dell'utente
        """Restituisce la lista di tutti i libri filtrati per biblioteca e/o genere (filtri opzionali)."""
        libri = self._libro_dao.get_libro()
        risultato = []
        for libro in libri:
            check_biblioteca = True
            if biblioteca is not None and biblioteca != "Nessun filtro":    # Controlla che ci sia una selezione dell'utente
                if str(libro.id_biblioteca) != str(biblioteca): # Se il libro non è nella biblioteca lo scarto
                    check_biblioteca = False

            check_genere = True
            if genere is not None and genere != "Nessun filtro":
                if libro.genere != genere:
                    check_genere = False

            if check_biblioteca and check_genere:
                risultato.append(libro)

    def get_generi(self):
        """Restituisce la lista di tutti i generi."""
        libri = self._libro_dao.get_libro()
        generi = []
        for libro in libri:
            if libro.genere and libro.genere not in generi: # Significa "se il genere esiste e non è nella lista"
                generi.append(libro.genere)
        return sorted(generi)

    # --- BIBLIOTECHE ---
    def get_biblioteche(self):
        """ Restituisce la lista di tutte le biblioteche."""
        return self._biblioteca_dao.get_biblioteca()
