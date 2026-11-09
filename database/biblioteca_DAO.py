from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        self.database_connect = DBConnect()

    def get_biblioteca(self):
        cnx = self.database_connect.get_connection()

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT id, nome, indirizzo 
                FROM biblioteca
                WHERE nome = COALESCE(%s, nome)"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Biblioteca(row["id"], row["nome"], row["indirizzo"]))
        cursor.close()
        cnx.close()
        return result

