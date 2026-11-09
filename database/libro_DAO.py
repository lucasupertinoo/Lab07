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
        cnx = self.database_connect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT id, titolo, autore, genere, anno_pubblicazione, id_biblioteca 
                    FROM libro"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Libro(row["id"], row["titolo"], row["autore"], row["genere"], row["anno_pubblicazione"], row["id_biblioteca"]))
        cursor.close()
        cnx.close()
        return result

