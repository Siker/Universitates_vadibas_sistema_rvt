# main.py — konsoles saskarne un izvēlne universitātes vadības sistēmai.
from student import Student
from pasniedzejs import Pasniedzejs
from kurss import Kurss
from atzime import Atzime
from grafiks import Grafiks
from utiliti import (
    add_student, find_student, show_all_students, show_student_info,
    edit_student, delete_student,
    add_pasniedzejs, show_all_pasniedzejs, delete_pasniedzejs,
    add_kurss, edit_kurss, show_all_kursi, find_course_by_name,
    delete_course, enroll_student,
    add_atzime, edit_atzime, average_grade,
    add_grafiks, show_grafiks,
    save_data, load_data
)


def safe_int(prompt):
    """Nolasa veselu skaitli ar kļūdu apstrādi (nefunk. prasība 6)."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Kļūda: ievadi skaitli!")


# ──────────────────────────────────────────────
# Apakšizvēlnes
# ──────────────────────────────────────────────

def menu_studenti():
    while True:
        print("\n── Studenti ──")
        print("  1. Pievienot studentu")
        print("  2. Skatīt visus studentus")
        print("  3. Skatīt studenta info (kursi + atzīmes)")
        print("  4. Rediģēt studentu")
        print("  5. Dzēst studentu")
        print("  0. Atpakaļ")
        izvele = input("Izvēle: ")

        if izvele == "1":
            id = safe_int("ID: ")
            vards = input("Vārds: ").strip()
            uzvards = input("Uzvārds: ").strip()
            pk = input("Personas kods (12 zīmes, piem. 140507-39522): ").strip()
            epasts = input("E-pasts: ").strip()
            talr = input("Tālrunis (12 zīmes, piem. +37120454239): ").strip()
            add_student(Student(id, vards, uzvards, pk, epasts, talr))
        elif izvele == "2":
            show_all_students()
        elif izvele == "3":
            show_student_info(safe_int("Studenta ID: "))
        elif izvele == "4":
            edit_student(safe_int("Studenta ID: "))
        elif izvele == "5":
            delete_student(safe_int("Studenta ID: "))
        elif izvele == "0":
            break
        else:
            print("Kļūda: nepareiza izvēle")


def menu_pasniedzeji():
    while True:
        print("\n── Pasniedzēji ──")
        print("  1. Pievienot pasniedzēju")
        print("  2. Skatīt visus pasniedzējus")
        print("  3. Dzēst pasniedzēju")
        print("  0. Atpakaļ")
        izvele = input("Izvēle: ")

        if izvele == "1":
            id = safe_int("ID: ")
            vards = input("Vārds: ").strip()
            uzvards = input("Uzvārds: ").strip()
            epasts = input("E-pasts: ").strip()
            add_pasniedzejs(Pasniedzejs(id, vards, uzvards, epasts))
        elif izvele == "2":
            show_all_pasniedzejs()
        elif izvele == "3":
            delete_pasniedzejs(safe_int("Pasniedzēja ID: "))
        elif izvele == "0":
            break
        else:
            print("Kļūda: nepareiza izvēle")


def menu_kursi():
    while True:
        print("\n── Kursi ──")
        print("  1. Pievienot kursu")
        print("  2. Skatīt visus kursus")
        print("  3. Rediģēt kursu")
        print("  4. Meklēt kursu pēc nosaukuma")
        print("  5. Reģistrēt studentu kursā")
        print("  6. Dzēst kursu")
        print("  0. Atpakaļ")
        izvele = input("Izvēle: ")

        if izvele == "1":
            id = safe_int("Kursa ID: ")
            nosaukums = input("Nosaukums: ").strip()
            pasniedzejs_id = safe_int("Pasniedzēja ID: ")
            add_kurss(Kurss(id, nosaukums, pasniedzejs_id))
        elif izvele == "2":
            show_all_kursi()
        elif izvele == "3":
            edit_kurss(safe_int("Kursa ID: "))
        elif izvele == "4":
            find_course_by_name(input("Ievadi nosaukumu (vai daļu): ").strip())
        elif izvele == "5":
            enroll_student(safe_int("Studenta ID: "), safe_int("Kursa ID: "))
        elif izvele == "6":
            delete_course(safe_int("Kursa ID: "))
        elif izvele == "0":
            break
        else:
            print("Kļūda: nepareiza izvēle")


def menu_atzimes():
    while True:
        print("\n── Atzīmes ──")
        print("  1. Pievienot atzīmi")
        print("  2. Rediģēt atzīmi")
        print("  3. Aprēķināt vidējo atzīmi")
        print("  0. Atpakaļ")
        izvele = input("Izvēle: ")

        if izvele == "1":
            id = safe_int("Atzīmes ID: ")
            student_id = safe_int("Studenta ID: ")
            kurss_id = safe_int("Kursa ID: ")
            atzime_value = safe_int("Atzīme (1-10): ")
            add_atzime(Atzime(id, student_id, kurss_id, atzime_value))
        elif izvele == "2":
            edit_atzime(safe_int("Atzīmes ID: "))
        elif izvele == "3":
            average_grade(safe_int("Studenta ID: "))
        elif izvele == "0":
            break
        else:
            print("Kļūda: nepareiza izvēle")


def menu_grafiks():
    while True:
        print("\n── Grafiks ──")
        print("  1. Pievienot grafiku")
        print("  2. Skatīt grafiku")
        print("  0. Atpakaļ")
        izvele = input("Izvēle: ")

        if izvele == "1":
            id = safe_int("Grafika ID: ")
            datums = input("Datums (DD.MM.GGGG): ").strip()
            laiks = input("Laiks (HH:MM): ").strip()
            kabinets = safe_int("Kabinets: ")
            kurss_id = safe_int("Kursa ID: ")
            add_grafiks(Grafiks(id, datums, laiks, kabinets, kurss_id))
        elif izvele == "2":
            show_grafiks()
        elif izvele == "0":
            break
        else:
            print("Kļūda: nepareiza izvēle")


# ──────────────────────────────────────────────
# Galvenā izvēlne
# ──────────────────────────────────────────────

def menu():
    load_data()
    while True:
        print("\n══════════════════════════════")
        print("   UNIVERSITĀTES VADĪBAS SISTĒMA")
        print("══════════════════════════════")
        print("1. Studenti")
        print("2. Pasniedzēji")
        print("3. Kursi")
        print("4. Atzīmes")
        print("5. Grafiks")
        print("6. Saglabāt datus")
        print("0. Iziet")
        izvele = input("Izvēle: ")

        if izvele == "1":
            menu_studenti()
        elif izvele == "2":
            menu_pasniedzeji()
        elif izvele == "3":
            menu_kursi()
        elif izvele == "4":
            menu_atzimes()
        elif izvele == "5":
            menu_grafiks()
        elif izvele == "6":
            save_data()
        elif izvele == "0":
            save_data()
            print("Uz redzēšanos!")
            break
        else:
            print("Kļūda: nepareiza izvēle")


menu()
