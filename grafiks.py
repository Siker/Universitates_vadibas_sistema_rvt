class Grafiks:
    # funkcija init pieņem int tipa vērtību id, str tipa vērtību datums,
    # str tipa vērtību laiks, int tipa vērtību kabinets, int tipa vērtību kurss_id
    # un atgriež None tipa vērtību rezultāts
    def __init__(self, id, datums, laiks, kabinets, kurss_id):
        self.id = id
        self.datums = datums
        self.laiks = laiks
        self.kabinets = kabinets
        self.kurss_id = kurss_id
