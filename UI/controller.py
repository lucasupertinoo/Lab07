import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
    - Riceve gli eventi dalla View (click, selezioni), chiede i dati al Model
      e dice alla View cosa mostrare
'''

class Controller:
    def __init__(self, view: View, model: Model):
        # Riferimenti al Model e alla View, passati da main.py
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        # None = l'utente non ha ancora scelto nulla -> il Model lo tratta come "nessun filtro"
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    def popola_dropdown(self):
        """Popola i dropdown di biblioteche e generi nella View.
        Viene chiamato da view.load_interface(), dopo che i dropdown sono stati creati."""

        # --- Dropdown biblioteche ---
        # Option("Nessun filtro") -> key e testo visualizzato coincidono: "Nessun filtro"
        self._view.dd_biblioteca.options.append(ft.dropdown.Option("Nessun filtro"))
        # Appendo singolarmente il nessun filtro

        # Chiedo al Model la lista delle biblioteche (oggetti Biblioteca)
        biblioteche = self._model.get_biblioteche()

        for b in biblioteche:   # Appendo tutto il resto con un ciclo
            # Usiamo l'ID come chiave e il nome come visualizzazione:
            # l'utente vede il nome, ma in e.control.value arriverà l'id (come stringa)
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(key=str(b.id), text=b.nome))

        # --- Dropdown generi ---
        self._view.dd_genere.options.append(ft.dropdown.Option("Nessun filtro"))
        generi = self._model.get_generi()   # Lista di stringhe, già senza duplicati e ordinata
        for g in generi:
            # Per i generi key e testo sono uguali: il nome del genere
            self._view.dd_genere.options.append(ft.dropdown.Option(key=g, text=g))

        self._view.update()

    # CALLBACKS DROPDOWN
    # L'obiettivo di queste funzioni è salvare la scelta dell'utente all'interno delle variabili del controller (righe 21-22)
    # Flet le chiama automaticamente quando l'utente sceglie un'opzione (evento on_select impostato nella View).
    # e è l'evento: e.control è il controllo che lo ha generato (il dropdown)
    # e con .value leggo la KEY dell'opzione scelta (id della biblioteca, nome del genere o "Nessun filtro")

    def seleziona_biblioteca(self, e):
        """Callback per la selezione della biblioteca."""
        self.biblioteca_selezionata = e.control.value

    def seleziona_genere(self, e):
        """Callback per la selezione del genere."""
        self.genere_selezionato = e.control.value

    # AZIONE: MOSTRA LIBRI
    def mostra_libri(self,e):
        """Callback del pulsante "Mostra Libri"."""
        # Chiedo al Model i libri che rispettano le selezioni correnti
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)

        # Svuoto la ListView, così non si accumulano i risultati delle ricerche precedenti
        self._view.lv_risultati.controls.clear()    # Prima di mostrarli pulisco la view

        if not libri:
            # Lista vuota -> nessun libro soddisfa i criteri, il sistema risponderà con un alert
            self._view.show_alert("Nessun libro trovato con i filtri selezionati.")
        else:
            # Mostro quanti libri ho trovato e poi un ft.Text per ogni libro.
            self._view.lv_risultati.controls.append(ft.Text(f"Trovati {len(libri)} libri:"))
            for libro in libri:
                self._view.lv_risultati.controls.append(ft.Text(str(libro)))

        self._view.update()