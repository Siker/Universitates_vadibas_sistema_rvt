import mysql.connector
from mysql.connector import Error


# 🔹 Подключение к базе (ОДНА база!)
def connect_db():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_brat_andrej",
        password="Uv5YN&e223Km4ay",
        database="freedb_Universitates_vadibas_sistema"
    )


# 🔹 Инициализация таблиц (БЕЗ создания базы!)
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            StudentID   INT PRIMARY KEY,
            Vards       VARCHAR(30)  NOT NULL,
            Uzvards     VARCHAR(30)  NOT NULL,
            Personas_Kods CHAR(12)   NOT NULL,
            Epasts      VARCHAR(50),
            Talrunis    CHAR(12)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasniedzejs (
            PasniedzejsID INT PRIMARY KEY,
            Vards         VARCHAR(30) NOT NULL,
            Uzvards       VARCHAR(30) NOT NULL,
            Epasts        VARCHAR(50)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kurss (
            KurssID       INT PRIMARY KEY,
            Nosaukums     VARCHAR(50) NOT NULL,
            PasniedzejsID INT,
            FOREIGN KEY (PasniedzejsID) REFERENCES pasniedzejs(PasniedzejsID)
                ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kurss_studenti (
            KurssID    INT NOT NULL,
            StudentID  INT NOT NULL,
            PRIMARY KEY (KurssID, StudentID),
            FOREIGN KEY (KurssID)   REFERENCES kurss(KurssID)    ON DELETE CASCADE,
            FOREIGN KEY (StudentID) REFERENCES students(StudentID) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atzime (
            AtzimeID   INT PRIMARY KEY,
            StudentID  INT NOT NULL,
            KurssID    INT NOT NULL,
            Atzime     INT NOT NULL,
            FOREIGN KEY (StudentID) REFERENCES students(StudentID) ON DELETE CASCADE,
            FOREIGN KEY (KurssID)   REFERENCES kurss(KurssID)      ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grafiks (
            GrafiksID  INT PRIMARY KEY,
            Datums     DATE NOT NULL,
            Laiks      CHAR(5) NOT NULL,
            Kabinets   INT,
            KurssID    INT,
            FOREIGN KEY (KurssID) REFERENCES kurss(KurssID) ON DELETE SET NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Tabulas gatavas!")


# 🔹 Пример: добавление студента
def add_student(student_id, vards, uzvards, personas_kods, epasts, talrunis):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
        INSERT INTO students (StudentID, Vards, Uzvards, Personas_Kods, Epasts, Talrunis)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (student_id, vards, uzvards, personas_kods, epasts, talrunis)

    try:
        cursor.execute(query, values)
        conn.commit()  # 🔴 ВАЖНО!
        print("✅ Students pievienots!")
    except Error as e:
        print("❌ Kļūda:", e)

    cursor.close()
    conn.close()


# 🔹 Пример: получить всех студентов
def get_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()


# 🔹 Запуск
if __name__ == "__main__":
    init_db()

    # Добавляем тестового студента
    add_student(1, "Andrej", "Ivanov", "123456-12345", "test@mail.com", "12345678")

    print("\n📋 Studentu saraksts:")
    get_students()