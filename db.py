import mysql.connector

# funkcija connect_db pieņem None tipa vērtību ievade un atgriež connection tipa vērtību savienojums
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="пароль",
        database="university_db"
    )
