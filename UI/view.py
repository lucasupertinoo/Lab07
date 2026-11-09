import flet as ft
from UI.alert import AlertManager

'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
    - Non contiene logica: quando l'utente interagisce, passa l'evento al Controller
'''

class View:
    def __init__(self, page: ft.Page):
        # Page: la finestra dell'applicazione, fornita da Flet in main.py
        self.page = page
        self.page.title = "Lab07"                     # Titolo della finestra
        self.page.horizontal_alignment = "center"     # Centra orizzontalmente i controlli
        self.page.theme_mode = ft.ThemeMode.DARK      # Tema scuro di default

        # Alert: oggetto che mostra le finestre di avviso
        self.alert = AlertManager(page)

        # Controller: per ora None, viene impostato da main.py con set_controller()
        self.controller = None

    def show_alert(self, messaggio):
        """Mostra un alert con il messaggio indicato (usato dal Controller)."""
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        """Collega il Controller alla View (chiamato da main.py prima di load_interface)."""
        self.controller = controller

    def update(self):
        """Ridisegna la pagina: va chiamato dopo ogni modifica ai controlli."""
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # --- Sezione 1: Intestazione ---
        self.txt_titolo = ft.Text(value="Biblioteche di Torino", size=38, weight=ft.FontWeight.BOLD)

        # --- Sezione 2: Filtraggio ---
        # Dropdown delle biblioteche.
        self.dd_biblioteca = ft.Dropdown(label="Biblioteca",
                                         hint_text="Seleziona una biblioteca...",
                                         width=300,
                                         on_select=self.controller.seleziona_biblioteca)
        # Il dropdown lo popolo dal controller e non nella view

        # Dropdown dei generi: stessa struttura del precedente
        self.dd_genere = ft.Dropdown(label="Genere",
                                         hint_text="Seleziona un genere...",
                                         width=300,
                                         on_select=self.controller.seleziona_genere)

        # Sezione 3: Libri
        # Pulsante "Mostra Libri": al click Flet chiama controller.mostra_libri.
        self.btn_mostra_libri = ft.Button(content="Mostra Libri",
                                          on_click=self.controller.mostra_libri,
                                          width=150)

        # lv_risultati mostra la listview scrollabile con tutti i risultati.
        self.lv_risultati = ft.ListView(height=400, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        # Switch per passare da tema scuro a chiaro: al cambio chiama self.cambia_tema
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        # page.add aggiunge i controlli alla pagina, dall'alto verso il basso
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),   # Linea orizzontale di separazione

            # Sezione 2: Filtraggio con i due dropdown affiancati in una riga centrata
            ft.Row([self.dd_biblioteca, self.dd_genere], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),

            # Sezione 3: Libri bottone che mostra i libri e listview con elenco di libri
            self.btn_mostra_libri,
            self.lv_risultati
        )

        # Ora che i dropdown esistono e sono nella pagina, il Controller li riempie con i dati del DB
        self.controller.popola_dropdown()

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        # Se lo switch è attivo (value=True) -> tema scuro, altrimenti tema chiaro
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
