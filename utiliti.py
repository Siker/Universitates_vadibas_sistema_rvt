"""
utiliti.py — visas biznesa loģikas funkcijas.
Dati tiek glabāti MySQL datubāzē (caur db.py).
In-memory saraksti un JSON fails vairs netiek izmantoti.
"""

from db import connect_db
from student import Student
from pasniedzejs import Pasniedzejs
from kurss import Kurss
from atzime import Atzime
from grafiks import Grafiks


# ──────────────────────────────────────────────
# Palīgfunkcija: datuma konvertēšana
# ──────────────────────────────────────────────

def _parse_date(datums_str):
    """Konvertē 'DD.MM.GGGG' uz 'GGGG-MM-DD' MySQL formātam."""
    try:
        parts = datums_str.strip().split(".")
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
    except Exception:
        pass
    return datums_str  # ja jau pareizs formāts vai kļūda


def _format_date(mysql_date):
    """Konvertē MySQL datumu atpakaļ uz 'DD.MM.GGGG' attēlošanai."""
    if mysql_date is None:
        return ""
    s = str(mysql_date)  # '2025-05-14' vai datetime.date objekts
    parts = s.split("-")
    if len(parts) == 3:
        return f"{parts[2]}.{parts[1]}.{parts[0]}"
    return s


# ──────────────────────────────────────────────
# Validācija (prasību dok. 3.1.1)
# ──────────────────────────────────────────────

def validate_student(vards, uzvards, personas_kods, epasts, talrunis):
    if not vards:
        print("Kļūda: vārds nav ievadīts"); return False
    if len(vards) > 30:
        print("Kļūda: vārds pārsniedz 30 rakstzīmes"); return False
    if not uzvards:
        print("Kļūda: uzvārds nav ievadīts"); return False
    if len(uzvards) > 30:
        print("Kļūda: uzvārds pārsniedz 30 rakstzīmes"); return False
    if len(personas_kods) != 12:
        print("Kļūda: personas kodam jābūt tieši 12 rakstzīmēm (piem. 140507-39522)"); return False
    if len(epasts) > 50:
        print("Kļūda: e-pasts pārsniedz 50 rakstzīmes"); return False
    if len(talrunis) != 12:
        print("Kļūda: tālrunim jābūt tieši 12 rakstzīmēm (piem. +37120454239)"); return False
    return True


def validate_pasniedzejs(vards, uzvards, epasts):
    if not vards:
        print("Kļūda: vārds nav ievadīts"); return False
    if len(vards) > 30:
        print("Kļūda: vārds pārsniedz 30 rakstzīmes"); return False
    if not uzvards:
        print("Kļūda: uzvārds nav ievadīts"); return False
    if len(uzvards) > 30:
        print("Kļūda: uzvārds pārsniedz 30 rakstzīmes"); return False
    if len(epasts) > 50:
        print("Kļūda: e-pasts pārsniedz 50 rakstzīmes"); return False
    return True


def validate_kurss(nosaukums):
    if not nosaukums:
        print("Kļūda: nosaukums nav ievadīts"); return False
    if len(nosaukums) > 50:
        print("Kļūda: nosaukums pārsniedz 50 rakstzīmes"); return False
    return True


# ──────────────────────────────────────────────
# save_data / load_data — saglabāti saderībai ar main.py
# (ar MySQL dati tiek saglabāti automātiski katrā operācijā)
# ──────────────────────────────────────────────

def save_data():
    print("Dati tiek glabāti datubāzē automātiski.")


def load_data():
    from db import init_db
    init_db()
    print("Savienojums ar datubāzi izveidots.")


# ──────────────────────────────────────────────
# Studenti
# ──────────────────────────────────────────────

def add_student(student):
    """Pievieno studentu datubāzē (prasības 1.1–1.5)."""
    if not validate_student(student.vards, student.uzvards,
                            student.personas_kods, student.epasts, student.talrunis):
        return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (StudentID, Vards, Uzvards, Personas_Kods, Epasts, Talrunis) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (student.id, student.vards, student.uzvards,
             student.personas_kods, student.epasts, student.talrunis)
        )
        conn.commit()
        print("Students veiksmīgi pievienots")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Kļūda: students ar šādu ID jau eksistē")
        else:
            print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def find_student(student_id):
    """Atrod studentu pēc ID. Atgriež Student objektu vai None."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT StudentID, Vards, Uzvards, Personas_Kods, Epasts, Talrunis "
            "FROM students WHERE StudentID = %s", (student_id,)
        )
        row = cursor.fetchone()
        if row:
            return Student(row[0], row[1], row[2], row[3], row[4], row[5])
        return None
    finally:
        cursor.close()
        conn.close()


def show_all_students():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT StudentID, Vards, Uzvards, Epasts, Talrunis FROM students ORDER BY StudentID"
        )
        rows = cursor.fetchall()
        if not rows:
            print("Nav neviena studenta."); return
        print("\n--- Studenti ---")
        for r in rows:
            print(f"  [{r[0]}] {r[1]} {r[2]} | {r[3]} | {r[4]}")
    finally:
        cursor.close()
        conn.close()


def show_student_info(student_id):
    """Parāda studenta kursus un vērtējumus (prasība 5.1–5.3)."""
    student = find_student(student_id)
    if not student:
        print("Kļūda: students nav atrasts"); return

    print(f"\n--- {student.vards} {student.uzvards} ---")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Studenta kursi
        cursor.execute("""
            SELECT k.KurssID, k.Nosaukums, p.Vards, p.Uzvards
            FROM kurss_studenti ks
            JOIN kurss k ON ks.KurssID = k.KurssID
            LEFT JOIN pasniedzejs p ON k.PasniedzejsID = p.PasniedzejsID
            WHERE ks.StudentID = %s
        """, (student_id,))
        kursi_rows = cursor.fetchall()
        print("\nStudenta kursi:")
        if kursi_rows:
            for r in kursi_rows:
                p_info = f"{r[2]} {r[3]}" if r[2] else f"ID {r[0]}"
                print(f"  [{r[0]}] {r[1]} | Pasniedzējs: {p_info}")
        else:
            print("  Nav reģistrēts nevienā kursā.")

        # Vērtējumi
        cursor.execute("""
            SELECT k.Nosaukums, a.Atzime
            FROM atzime a
            JOIN kurss k ON a.KurssID = k.KurssID
            WHERE a.StudentID = %s
        """, (student_id,))
        atzime_rows = cursor.fetchall()
        print("\nVērtējumu saraksts:")
        if atzime_rows:
            for r in atzime_rows:
                print(f"  {r[0]}: {r[1]}")
            videjais = sum(r[1] for r in atzime_rows) / len(atzime_rows)
            print(f"\nVidējais vērtējums: {videjais:.2f}")
        else:
            print("  Nav vērtējumu.")
    finally:
        cursor.close()
        conn.close()


def edit_student(student_id):
    """Rediģē studenta kontaktdatus."""
    student = find_student(student_id)
    if not student:
        print("Kļūda: students nav atrasts"); return
    print(f"Rediģē: {student.vards} {student.uzvards}")
    epasts = input(f"Jauns e-pasts (pašreiz: {student.epasts}, Enter = atstāt): ").strip()
    talrunis = input(f"Jauns tālrunis (pašreiz: {student.talrunis}, Enter = atstāt): ").strip()
    if epasts and len(epasts) > 50:
        print("Kļūda: e-pasts pārsniedz 50 rakstzīmes"); return
    if talrunis and len(talrunis) != 12:
        print("Kļūda: tālrunim jābūt tieši 12 rakstzīmēm"); return

    conn = connect_db()
    cursor = conn.cursor()
    try:
        if epasts:
            cursor.execute("UPDATE students SET Epasts = %s WHERE StudentID = %s",
                           (epasts, student_id))
        if talrunis:
            cursor.execute("UPDATE students SET Talrunis = %s WHERE StudentID = %s",
                           (talrunis, student_id))
        conn.commit()
        print("Studenta dati atjaunināti")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_student(student_id):
    if not find_student(student_id):
        print("Kļūda: students nav atrasts"); return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE StudentID = %s", (student_id,))
        conn.commit()
        print("Students dzēsts")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# Pasniedzēji
# ──────────────────────────────────────────────

def add_pasniedzejs(pasniedzejs):
    if not validate_pasniedzejs(pasniedzejs.vards, pasniedzejs.uzvards, pasniedzejs.epasts):
        return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pasniedzejs (PasniedzejsID, Vards, Uzvards, Epasts) "
            "VALUES (%s, %s, %s, %s)",
            (pasniedzejs.id, pasniedzejs.vards, pasniedzejs.uzvards, pasniedzejs.epasts)
        )
        conn.commit()
        print("Pasniedzējs veiksmīgi pievienots")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Kļūda: pasniedzējs ar šādu ID jau eksistē")
        else:
            print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def find_pasniedzejs(pasniedzejs_id):
    """Atrod pasniedzēju pēc ID. Atgriež Pasniedzejs objektu vai None."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT PasniedzejsID, Vards, Uzvards, Epasts "
            "FROM pasniedzejs WHERE PasniedzejsID = %s", (pasniedzejs_id,)
        )
        row = cursor.fetchone()
        if row:
            return Pasniedzejs(row[0], row[1], row[2], row[3])
        return None
    finally:
        cursor.close()
        conn.close()


def show_all_pasniedzejs():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT PasniedzejsID, Vards, Uzvards, Epasts FROM pasniedzejs ORDER BY PasniedzejsID"
        )
        rows = cursor.fetchall()
        if not rows:
            print("Nav neviena pasniedzēja."); return
        print("\n--- Pasniedzēji ---")
        for r in rows:
            print(f"  [{r[0]}] {r[1]} {r[2]} | {r[3]}")
    finally:
        cursor.close()
        conn.close()


def delete_pasniedzejs(pasniedzejs_id):
    if not find_pasniedzejs(pasniedzejs_id):
        print("Kļūda: pasniedzējs nav atrasts"); return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pasniedzejs WHERE PasniedzejsID = %s", (pasniedzejs_id,))
        conn.commit()
        print("Pasniedzējs dzēsts")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# Kursi
# ──────────────────────────────────────────────

def add_kurss(kurss):
    """Pievieno kursu; pārbauda pasniedzēja eksistenci (prasības 2.1–2.4)."""
    if not validate_kurss(kurss.nosaukums):
        return
    if not find_pasniedzejs(kurss.pasniedzejs_id):
        print(f"Kļūda: pasniedzējs ar ID {kurss.pasniedzejs_id} neeksistē sistēmā"); return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO kurss (KurssID, Nosaukums, PasniedzejsID) VALUES (%s, %s, %s)",
            (kurss.id, kurss.nosaukums, kurss.pasniedzejs_id)
        )
        conn.commit()
        print("Kurss veiksmīgi pievienots")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Kļūda: kurss ar šādu ID jau eksistē")
        else:
            print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def edit_kurss(kurss_id):
    """Rediģē kursa nosaukumu."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Nosaukums FROM kurss WHERE KurssID = %s", (kurss_id,))
        row = cursor.fetchone()
        if not row:
            print("Kļūda: kurss nav atrasts"); return
        nosaukums = input(f"Jauns nosaukums (pašreiz: {row[0]}, Enter = atstāt): ").strip()
        if nosaukums:
            if len(nosaukums) > 50:
                print("Kļūda: nosaukums pārsniedz 50 rakstzīmes"); return
            cursor.execute("UPDATE kurss SET Nosaukums = %s WHERE KurssID = %s",
                           (nosaukums, kurss_id))
            conn.commit()
        print("Kurss atjaunināts")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def show_all_kursi():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT k.KurssID, k.Nosaukums,
                   p.Vards, p.Uzvards,
                   COUNT(ks.StudentID) AS studenti_skaits
            FROM kurss k
            LEFT JOIN pasniedzejs p ON k.PasniedzejsID = p.PasniedzejsID
            LEFT JOIN kurss_studenti ks ON k.KurssID = ks.KurssID
            GROUP BY k.KurssID, k.Nosaukums, p.Vards, p.Uzvards
            ORDER BY k.KurssID
        """)
        rows = cursor.fetchall()
        if not rows:
            print("Nav neviena kursa."); return
        print("\n--- Kursi ---")
        for r in rows:
            p_info = f"{r[2]} {r[3]}" if r[2] else "nav"
            print(f"  [{r[0]}] {r[1]} | Pasniedzējs: {p_info} | Studenti: {r[4]}")
    finally:
        cursor.close()
        conn.close()


def find_course_by_name(name):
    """Meklē kursus pēc nosaukuma — daļēja sakritība."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT KurssID, Nosaukums FROM kurss WHERE LOWER(Nosaukums) LIKE %s ORDER BY KurssID",
            (f"%{name.lower()}%",)
        )
        rows = cursor.fetchall()
        if not rows:
            print("Kursi nav atrasti."); return
        print("\n--- Meklēšanas rezultāti ---")
        for r in rows:
            print(f"  [{r[0]}] {r[1]}")
    finally:
        cursor.close()
        conn.close()


def delete_course(course_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT KurssID FROM kurss WHERE KurssID = %s", (course_id,))
        if not cursor.fetchone():
            print("Kļūda: kurss nav atrasts"); return
        cursor.execute("DELETE FROM kurss WHERE KurssID = %s", (course_id,))
        conn.commit()
        print("Kurss dzēsts")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def enroll_student(student_id, kurss_id):
    """Reģistrē studentu kursā (prasības 3.1–3.5)."""
    if not find_student(student_id):
        print("Kļūda: students nav atrasts"); return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT KurssID FROM kurss WHERE KurssID = %s", (kurss_id,))
        if not cursor.fetchone():
            print("Kļūda: kurss nav atrasts"); return
        cursor.execute(
            "SELECT 1 FROM kurss_studenti WHERE KurssID = %s AND StudentID = %s",
            (kurss_id, student_id)
        )
        if cursor.fetchone():
            print("Kļūda: students jau ir reģistrēts šajā kursā"); return
        cursor.execute(
            "INSERT INTO kurss_studenti (KurssID, StudentID) VALUES (%s, %s)",
            (kurss_id, student_id)
        )
        conn.commit()
        print("Students veiksmīgi pievienots kursam")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# Atzīmes
# ──────────────────────────────────────────────

def add_atzime(atzime):
    """Pievieno atzīmi (prasības 4.1–4.5)."""
    if not find_student(atzime.student_id):
        print("Kļūda: students nav atrasts"); return
    if not (1 <= atzime.atzime <= 10):
        print("Kļūda: nepareiza atzīme (jābūt no 1 līdz 10)"); return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT KurssID FROM kurss WHERE KurssID = %s", (atzime.kurss_id,))
        if not cursor.fetchone():
            print("Kļūda: kurss nav atrasts"); return
        cursor.execute(
            "INSERT INTO atzime (AtzimeID, StudentID, KurssID, Atzime) VALUES (%s, %s, %s, %s)",
            (atzime.id, atzime.student_id, atzime.kurss_id, atzime.atzime)
        )
        conn.commit()
        print("Vērtējums pievienots")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Kļūda: atzīme ar šādu ID jau eksistē")
        else:
            print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def edit_atzime(atzime_id):
    """Rediģē atzīmes vērtību."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Atzime FROM atzime WHERE AtzimeID = %s", (atzime_id,))
        row = cursor.fetchone()
        if not row:
            print("Kļūda: atzīme nav atrasta"); return
        try:
            jauna = int(input(f"Jaunā atzīme (pašreiz: {row[0]}): "))
        except ValueError:
            print("Kļūda: ievadi skaitli"); return
        if not (1 <= jauna <= 10):
            print("Kļūda: atzīmei jābūt no 1 līdz 10"); return
        cursor.execute("UPDATE atzime SET Atzime = %s WHERE AtzimeID = %s", (jauna, atzime_id))
        conn.commit()
        print("Atzīme atjaunināta")
    except Exception as e:
        print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def average_grade(student_id):
    """Aprēķina studenta vidējo atzīmi."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT AVG(Atzime) FROM atzime WHERE StudentID = %s", (student_id,)
        )
        row = cursor.fetchone()
        if row and row[0] is not None:
            print(f"Vidējais vērtējums: {row[0]:.2f}")
        else:
            print("Nav atzīmju vidējā aprēķinam.")
    finally:
        cursor.close()
        conn.close()


# ──────────────────────────────────────────────
# Grafiks
# ──────────────────────────────────────────────

def add_grafiks(grafiks):
    if not grafiks.datums or not grafiks.laiks:
        print("Kļūda: datums vai laiks nav ievadīts"); return
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT KurssID FROM kurss WHERE KurssID = %s", (grafiks.kurss_id,))
        if not cursor.fetchone():
            print("Kļūda: kurss nav atrasts"); return
        mysql_date = _parse_date(grafiks.datums)
        cursor.execute(
            "INSERT INTO grafiks (GrafiksID, Datums, Laiks, Kabinets, KurssID) "
            "VALUES (%s, %s, %s, %s, %s)",
            (grafiks.id, mysql_date, grafiks.laiks, grafiks.kabinets, grafiks.kurss_id)
        )
        conn.commit()
        print("Grafiks veiksmīgi pievienots")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("Kļūda: grafiks ar šādu ID jau eksistē")
        else:
            print(f"Datubāzes kļūda: {e}")
    finally:
        cursor.close()
        conn.close()


def show_grafiks():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT g.GrafiksID, g.Datums, g.Laiks, g.Kabinets, k.Nosaukums
            FROM grafiks g
            LEFT JOIN kurss k ON g.KurssID = k.KurssID
            ORDER BY g.Datums, g.Laiks
        """)
        rows = cursor.fetchall()
        if not rows:
            print("Nav neviena grafika."); return
        print("\n--- Grafiks ---")
        for r in rows:
            datums_str = _format_date(r[1])
            kurss_nos = r[4] if r[4] else "?"
            print(f"  [{r[0]}] {datums_str} {r[2]} | Kabinets: {r[3]} | Kurss: {kurss_nos}")
    finally:
        cursor.close()
        conn.close()
