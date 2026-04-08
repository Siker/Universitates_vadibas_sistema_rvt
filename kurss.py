class Kurss:
    # funkcija init pieņem int tipa vērtību id, str tipa vērtību nosaukums,
    # int tipa vērtību pasniedzejs_id
    # un atgriež None tipa vērtību rezultāts
    def __init__(self, id, nosaukums, pasniedzejs_id):
        self.id = id
        self.nosaukums = nosaukums
        self.pasniedzejs_id = pasniedzejs_id
        self.studenti = []
