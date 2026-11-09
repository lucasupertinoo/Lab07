import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    def popola_dropdown(self):
        """Popola i dropdown di biblioteche e generi nella View."""
        # Opzione "Nessun filtro" come richiesto dal README
        self._view.dd_biblioteca.options.append(ft.dropdown.Option("Nessun filtro"))    # Appendo singolarmente il nessun filtro
        biblioteche = self._model.get_biblioteche()

        for b in biblioteche:   # Appendo tutto il resto con un ciclo
            # Usiamo l'ID come chiave e il nome come visualizzazione
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(key=str(b.id), text=b.nome))

        self._view.dd_genere.options.append(ft.dropdown.Option("Nessun filtro"))
        generi = self._model.get_generi()
        for g in generi:
            self._view.dd_genere.options.append(ft.dropdown.Option(key=g, text=g))

        self._view.update()

    # CALLBACKS DROPDOWN
    # L'obiettivo di queste funzioni è salvare la scelta dell'utente all'interno delle variabili del controller (righe 17-18)
    # e.control.value parte dall'evento di click: flet individua grazie a e.control che c'è stato un click
    # e con .value va a leggere la chiave del controllo cliccato (il dropdown in questo caso che viene riconosciuto)

    def seleziona_biblioteca(self, e):
        """Callback per la selezione della biblioteca."""
        self.biblioteca_selezionata = e.control.value

    def seleziona_genere(self, e):
        """Callback per la selezione del genere."""
        self.genere_selezionato = e.control.value

    # AZIONE: MOSTRA LIBRI
    def mostra_libri(self,e):
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)
        self._view.lv_risultati.controls.clear()    # Prima di mostrarli pulisco la view

        if not libri:
            # Se nessun libro soddisfa i criteri, il sistema risponderà con un alert
            self._view.show_alert("Nessun libro trovato con i filtri selezionati.")
        else:
            self._view.lv_risultati.controls.append(ft.Text(f"Trovati {len(libri)} libri:"))
            for libro in libri:
                self._view.lv_risultati.controls.append(ft.Text(str(libro)))

        self._view.update()
