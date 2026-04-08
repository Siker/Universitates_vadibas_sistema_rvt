import mysql.connector
from mysql.connector import Error
 
 
# funkcija connect_db pieņem None tipa vērtību ievade un atgriež connection tipa vērtību savienojums
def connect_db():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_brat_andrej",
        password="Uv5YN&e223Km4ay",
        database="freedb_Universitates_vadibas_sistema"
    )
 
 
# funkcija init_db izveido visas nepieciešamās tabulas, ja tās vēl nepastāv
def init_db():
    """Izveido datubāzi un tabulas, ja tās vēl nepastāv."""
    # Vispirms savienojamies bez datubāzes, lai to izveidotu
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="пароль"
    )
    cursor = conn.cursor()
 
    cursor.execute("CREATE DATABASE IF NOT EXISTS university_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute("USE university_db")
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            StudentID   INT PRIMARY KEY,
            Vards       VARCHAR(30)  NOT NULL,
            Uzvards     VARCHAR(30)  NOT NULL,
            Personas_Kods CHAR(12)   NOT NULL,
            Epasts      VARCHAR(50),
            Talrunis    CHAR(12)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasniedzejs (
            PasniedzejsID INT PRIMARY KEY,
            Vards         VARCHAR(30) NOT NULL,
            Uzvards       VARCHAR(30) NOT NULL,
            Epasts        VARCHAR(50)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kurss (
            KurssID       INT PRIMARY KEY,
            Nosaukums     VARCHAR(50) NOT NULL,
            PasniedzejsID INT,
            FOREIGN KEY (PasniedzejsID) REFERENCES pasniedzejs(PasniedzejsID)
                ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kurss_studenti (
            KurssID    INT NOT NULL,
            StudentID  INT NOT NULL,
            PRIMARY KEY (KurssID, StudentID),
            FOREIGN KEY (KurssID)   REFERENCES kurss(KurssID)    ON DELETE CASCADE,
            FOREIGN KEY (StudentID) REFERENCES students(StudentID) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atzime (
            AtzimeID   INT PRIMARY KEY,
            StudentID  INT NOT NULL,
            KurssID    INT NOT NULL,
            Atzime     INT NOT NULL,
            FOREIGN KEY (StudentID) REFERENCES students(StudentID) ON DELETE CASCADE,
            FOREIGN KEY (KurssID)   REFERENCES kurss(KurssID)      ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grafiks (
            GrafiksID  INT PRIMARY KEY,
            Datums     DATE NOT NULL,
            Laiks      CHAR(5) NOT NULL,
            Kabinets   INT,
            KurssID    INT,
            FOREIGN KEY (KurssID) REFERENCES kurss(KurssID) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
 
    conn.commit()
    cursor.close()
    conn.close()
    print("Datubāze inicializēta.")
