import mysql.connector

# funkcija connect_db pieņem None tipa vērtību ievade un atgriež connection tipa vērtību savienojums
def connect_db():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_brat_andrej",
        password="Uv5YN&e223Km4ay",
        database="freedb_Universitates_vadibas_sistema"
    )
