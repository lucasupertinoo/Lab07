from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        self.database_connect = DBConnect

    def get_libro(self):
        """Legge TUTTI i libri dal DB e li restituisce come lista di oggetti Libro.
        I filtri per biblioteca e genere vengono applicati dopo, in Python, nel Model"""

        cnx = self.database_connect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Query senza WHERE e senza %s -> restituisce tutti i libri della tabella
        query = """ SELECT id, titolo, autore, genere, anno_pubblicazione, id_biblioteca
                    FROM libro"""

        cursor.execute(query)

        # Per ogni riga creo un oggetto Libro, passando i campi nello stesso ordine in cui sono dichiarati nella dataclass Libro
        result = []
        for row in cursor:
            result.append(Libro(row["id"], row["titolo"], row["autore"], row["genere"], row["anno_pubblicazione"], row["id_biblioteca"]))

        cursor.close()
        cnx.close()
        return result