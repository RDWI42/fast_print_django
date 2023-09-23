from django.db import models

class Product(models.Model):
    nama_produk = models.CharField(max_length=255)
    harga = models.IntegerField()
    kategori = models.ForeignKey('Kategori', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_produk
    
class Status(models.Model):
    nama_status = models.CharField(max_length=255)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_status

class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=255)
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_kategori
