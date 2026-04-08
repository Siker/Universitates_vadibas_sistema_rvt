class Student:
    # funkcija init pieņem int tipa vērtību id, str tipa vērtību vards, str tipa vērtību uzvards,
    # str tipa vērtību personas_kods, str tipa vērtību epasts, str tipa vērtību talrunis
    # un atgriež None tipa vērtību rezultāts
    def __init__(self, id, vards, uzvards, personas_kods, epasts, talrunis):
        self.id = id
        self.vards = vards
        self.uzvards = uzvards
        self.personas_kods = personas_kods
        self.epasts = epasts
        self.talrunis = talrunis
        self.kursi = []
