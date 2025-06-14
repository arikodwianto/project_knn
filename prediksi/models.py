# prediksi/models.py
from django.db import models

class DataLatih(models.Model):
    HARI_CHOICES = [
        (1, 'Senin'),
        (2, 'Selasa'),
        (3, 'Rabu'),
        (4, 'Kamis'),
        (5, 'Jumat'),
        (6, 'Sabtu'),
        (7, 'Minggu'),
    ]

    WAKTU_CHOICES = [
        (1, 'Pagi'),
        (2, 'Siang'),
        (3, 'Sore'),
        (4, 'Malam'),
    ]

    PAKET_CHOICES = [
        (0, 'Reguler'),
        (1, 'Intensif'),
        (2, 'Private'),
        (3, 'VIP'),
    ]

    STATUS_CHOICES = [
        ('Bisa', 'Bisa'),
        ('Tidak Bisa', 'Tidak Bisa'),
    ]

    nama = models.CharField(max_length=100)
    hari = models.IntegerField(choices=HARI_CHOICES)
    waktu = models.IntegerField(choices=WAKTU_CHOICES)
    durasi = models.IntegerField()
    paket = models.IntegerField(choices=PAKET_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.nama} - {self.status}"

class DataUji(models.Model):
    HARI_CHOICES = DataLatih.HARI_CHOICES
    WAKTU_CHOICES = DataLatih.WAKTU_CHOICES
    PAKET_CHOICES = DataLatih.PAKET_CHOICES

    nama = models.CharField(max_length=100)
    hari = models.IntegerField(choices=HARI_CHOICES)
    waktu = models.IntegerField(choices=WAKTU_CHOICES)
    durasi = models.IntegerField()
    paket = models.IntegerField(choices=PAKET_CHOICES)
    hasil_prediksi = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nama} - {self.hasil_prediksi or 'Belum Diprediksi'}"
