class Atzime:
    # funkcija init pieņem int tipa vērtību student_id,
    # int tipa vērtību kurss_id, int tipa vērtību atzime
    # un atgriež None tipa vērtību rezultāts
    def __init__(self, id, student_id, kurss_id, atzime):
        self.id = id
        self.student_id = student_id
        self.kurss_id = kurss_id
        self.atzime = atzime
