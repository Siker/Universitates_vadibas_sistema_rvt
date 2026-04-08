import json
import os
from database import studenti, kursi, pasniedzeji, atzimes, grafiki

DATA_FILE = "data.json"


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
# Saglabāšana / ielāde (JSON)
# ──────────────────────────────────────────────

def save_data():
    data = {
        "studenti": [
            {"id": s.id, "vards": s.vards, "uzvards": s.uzvards,
             "personas_kods": s.personas_kods, "epasts": s.epasts,
             "talrunis": s.talrunis}
            for s in studenti
        ],
        "pasniedzeji": [
            {"id": p.id, "vards": p.vards, "uzvards": p.uzvards, "epasts": p.epasts}
            for p in pasniedzeji
        ],
        "kursi": [
            {"id": k.id, "nosaukums": k.nosaukums,
             "pasniedzejs_id": k.pasniedzejs_id, "studenti": k.studenti}
            for k in kursi
        ],
        "atzimes": [
            {"id": a.id, "student_id": a.student_id,
             "kurss_id": a.kurss_id, "atzime": a.atzime}
            for a in atzimes
        ],
        "grafiki": [
            {"id": g.id, "datums": g.datums, "laiks": g.laiks,
             "kabinets": g.kabinets, "kurss_id": g.kurss_id}
            for g in grafiki
        ],
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Dati saglabāti.")


def load_data():
    from student import Student
    from pasniedzejs import Pasniedzejs
    from kurss import Kurss
    from atzime import Atzime
    from grafiks import Grafiks

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for s in data.get("studenti", []):
        obj = Student(s["id"], s["vards"], s["uzvards"],
                      s["personas_kods"], s["epasts"], s["talrunis"])
        studenti.append(obj)
    for p in data.get("pasniedzeji", []):
        obj = Pasniedzejs(p["id"], p["vards"], p["uzvards"], p["epasts"])
        pasniedzeji.append(obj)
    for k in data.get("kursi", []):
        from kurss import Kurss
        obj = Kurss(k["id"], k["nosaukums"], k["pasniedzejs_id"])
        obj.studenti = k["studenti"]
        kursi.append(obj)
    for a in data.get("atzimes", []):
        obj = Atzime(a["id"], a["student_id"], a["kurss_id"], a["atzime"])
        atzimes.append(obj)
    for g in data.get("grafiki", []):
        obj = Grafiks(g["id"], g["datums"], g["laiks"], g["kabinets"], g["kurss_id"])
        grafiki.append(obj)

    print("Dati ielādēti no faila.")


# ──────────────────────────────────────────────
# Studenti
# ──────────────────────────────────────────────

def add_student(student):
    """Pievieno studentu; validē laukus un pārbauda unikālo ID (prasības 1.1–1.5)."""
    if not validate_student(student.vards, student.uzvards,
                            student.personas_kods, student.epasts, student.talrunis):
        return
    if find_student(student.id):
        print("Kļūda: students ar šādu ID jau eksistē"); return
    studenti.append(student)
    print("Students veiksmīgi pievienots")


def find_student(student_id):
    for s in studenti:
        if s.id == student_id:
            return s
    return None


def show_all_students():
    if not studenti:
        print("Nav neviena studenta."); return
    print("\n--- Studenti ---")
    for s in studenti:
        print(f"  [{s.id}] {s.vards} {s.uzvards} | {s.epasts} | {s.talrunis}")


def show_student_info(student_id):
    """Parāda studenta kursus un vērtējumus (prasība 5.1–5.3)."""
    student = find_student(student_id)
    if not student:
        print("Kļūda: students nav atrasts"); return
    print(f"\n--- {student.vards} {student.uzvards} ---")

    print("\nStudenta kursi:")
    enrolled = [k for k in kursi if student_id in k.studenti]
    if enrolled:
        for k in enrolled:
            p = find_pasniedzejs(k.pasniedzejs_id)
            p_info = f"{p.vards} {p.uzvards}" if p else f"ID {k.pasniedzejs_id}"
            print(f"  [{k.id}] {k.nosaukums} | Pasniedzējs: {p_info}")
    else:
        print("  Nav reģistrēts nevienā kursā.")

    print("\nVērtējumu saraksts:")
    student_grades = [a for a in atzimes if a.student_id == student_id]
    if student_grades:
        for a in student_grades:
            kurss_nos = next((k.nosaukums for k in kursi if k.id == a.kurss_id), "?")
            print(f"  {kurss_nos}: {a.atzime}")
        videjais = sum(a.atzime for a in student_grades) / len(student_grades)
        print(f"\nVidējais vērtējums: {videjais:.2f}")
    else:
        print("  Nav vērtējumu.")


def edit_student(student_id):
    """Rediģē studenta kontaktdatus."""
    student = find_student(student_id)
    if not student:
        print("Kļūda: students nav atrasts"); return
    print(f"Rediģē: {student.vards} {student.uzvards}")
    epasts = input(f"Jauns e-pasts (pašreiz: {student.epasts}, Enter = atstāt): ").strip()
    talrunis = input(f"Jauns tālrunis (pašreiz: {student.talrunis}, Enter = atstāt): ").strip()
    if epasts:
        if len(epasts) > 50:
            print("Kļūda: e-pasts pārsniedz 50 rakstzīmes"); return
        student.epasts = epasts
    if talrunis:
        if len(talrunis) != 12:
            print("Kļūda: tālrunim jābūt tieši 12 rakstzīmēm"); return
        student.talrunis = talrunis
    print("Studenta dati atjaunināti")


def delete_student(student_id):
    student = find_student(student_id)
    if not student:
        print("Kļūda: students nav atrasts"); return
    studenti.remove(student)
    print("Students dzēsts")


# ──────────────────────────────────────────────
# Pasniedzēji
# ──────────────────────────────────────────────

def add_pasniedzejs(pasniedzejs):
    if not validate_pasniedzejs(pasniedzejs.vards, pasniedzejs.uzvards, pasniedzejs.epasts):
        return
    if find_pasniedzejs(pasniedzejs.id):
        print("Kļūda: pasniedzējs ar šādu ID jau eksistē"); return
    pasniedzeji.append(pasniedzejs)
    print("Pasniedzējs veiksmīgi pievienots")


def find_pasniedzejs(pasniedzejs_id):
    for p in pasniedzeji:
        if p.id == pasniedzejs_id:
            return p
    return None


def show_all_pasniedzejs():
    if not pasniedzeji:
        print("Nav neviena pasniedzēja."); return
    print("\n--- Pasniedzēji ---")
    for p in pasniedzeji:
        print(f"  [{p.id}] {p.vards} {p.uzvards} | {p.epasts}")


def delete_pasniedzejs(pasniedzejs_id):
    p = find_pasniedzejs(pasniedzejs_id)
    if not p:
        print("Kļūda: pasniedzējs nav atrasts"); return
    pasniedzeji.remove(p)
    print("Pasniedzējs dzēsts")


# ──────────────────────────────────────────────
# Kursi
# ──────────────────────────────────────────────

def add_kurss(kurss):
    """Pievieno kursu; pārbauda pasniedzēja eksistenci (prasības 2.1–2.4)."""
    if not validate_kurss(kurss.nosaukums):
        return
    for k in kursi:
        if k.id == kurss.id:
            print("Kļūda: kurss ar šādu ID jau eksistē"); return
    # Prasība 2.2–2.3: pasniedzējam jāeksistē
    if not find_pasniedzejs(kurss.pasniedzejs_id):
        print(f"Kļūda: pasniedzējs ar ID {kurss.pasniedzejs_id} neeksistē sistēmā"); return
    kursi.append(kurss)
    print("Kurss veiksmīgi pievienots")


def edit_kurss(kurss_id):
    """Rediģē kursa nosaukumu."""
    for k in kursi:
        if k.id == kurss_id:
            nosaukums = input(f"Jauns nosaukums (pašreiz: {k.nosaukums}, Enter = atstāt): ").strip()
            if nosaukums:
                if len(nosaukums) > 50:
                    print("Kļūda: nosaukums pārsniedz 50 rakstzīmes"); return
                k.nosaukums = nosaukums
            print("Kurss atjaunināts"); return
    print("Kļūda: kurss nav atrasts")


def show_all_kursi():
    if not kursi:
        print("Nav neviena kursa."); return
    print("\n--- Kursi ---")
    for k in kursi:
        p = find_pasniedzejs(k.pasniedzejs_id)
        p_info = f"{p.vards} {p.uzvards}" if p else f"ID {k.pasniedzejs_id}"
        print(f"  [{k.id}] {k.nosaukums} | Pasniedzējs: {p_info} | Studenti: {len(k.studenti)}")


def find_course_by_name(name):
    """Meklē kursus pēc nosaukuma — daļēja sakritība."""
    results = [k for k in kursi if name.lower() in k.nosaukums.lower()]
    if not results:
        print("Kursi nav atrasti."); return
    print("\n--- Meklēšanas rezultāti ---")
    for k in results:
        print(f"  [{k.id}] {k.nosaukums}")


def delete_course(course_id):
    for k in kursi:
        if k.id == course_id:
            kursi.remove(k)
            print("Kurss dzēsts"); return
    print("Kļūda: kurss nav atrasts")


def enroll_student(student_id, kurss_id):
    """Reģistrē studentu kursā (prasības 3.1–3.5)."""
    if not find_student(student_id):
        print("Kļūda: students nav atrasts"); return
    for k in kursi:
        if k.id == kurss_id:
            if student_id in k.studenti:
                print("Kļūda: students jau ir reģistrēts šajā kursā"); return
            k.studenti.append(student_id)
            print("Students veiksmīgi pievienots kursam"); return
    print("Kļūda: kurss nav atrasts")


# ──────────────────────────────────────────────
# Atzīmes
# ──────────────────────────────────────────────

def add_atzime(atzime):
    """Pievieno atzīmi (prasības 4.1–4.5)."""
    if not find_student(atzime.student_id):
        print("Kļūda: students nav atrasts"); return
    if not any(k.id == atzime.kurss_id for k in kursi):
        print("Kļūda: kurss nav atrasts"); return
    if not (1 <= atzime.atzime <= 10):
        print("Kļūda: nepareiza atzīme (jābūt no 1 līdz 10)"); return
    if any(a.id == atzime.id for a in atzimes):
        print("Kļūda: atzīme ar šādu ID jau eksistē"); return
    atzimes.append(atzime)
    print("Vērtējums pievienots")


def edit_atzime(atzime_id):
    """Rediģē atzīmes vērtību."""
    for a in atzimes:
        if a.id == atzime_id:
            try:
                jauna = int(input(f"Jaunā atzīme (pašreiz: {a.atzime}): "))
            except ValueError:
                print("Kļūda: ievadi skaitli"); return
            if not (1 <= jauna <= 10):
                print("Kļūda: atzīmei jābūt no 1 līdz 10"); return
            a.atzime = jauna
            print("Atzīme atjaunināta"); return
    print("Kļūda: atzīme nav atrasta")


def average_grade(student_id):
    """Aprēķina studenta vidējo atzīmi."""
    grades = [a.atzime for a in atzimes if a.student_id == student_id]
    if grades:
        print(f"Vidējais vērtējums: {sum(grades) / len(grades):.2f}")
    else:
        print("Nav atzīmju vidējā aprēķinam.")


# ──────────────────────────────────────────────
# Grafiks
# ──────────────────────────────────────────────

def add_grafiks(grafiks):
    if not grafiks.datums or not grafiks.laiks:
        print("Kļūda: datums vai laiks nav ievadīts"); return
    if any(g.id == grafiks.id for g in grafiki):
        print("Kļūda: grafiks ar šādu ID jau eksistē"); return
    if not any(k.id == grafiks.kurss_id for k in kursi):
        print("Kļūda: kurss nav atrasts"); return
    grafiki.append(grafiks)
    print("Grafiks veiksmīgi pievienots")


def show_grafiks():
    if not grafiki:
        print("Nav neviena grafika."); return
    print("\n--- Grafiks ---")
    for g in grafiki:
        kurss_nos = next((k.nosaukums for k in kursi if k.id == g.kurss_id), "?")
        print(f"  [{g.id}] {g.datums} {g.laiks} | Kabinets: {g.kabinets} | Kurss: {kurss_nos}")
