from django.db import models

# Create your models here.

#class Kategori dengan parameter models.Model yang digunakan untuk membuat model Kategori. 
class Kategori(models.Model):
    # Model ini memiliki satu field yaitu nama_kategori yang merupakan CharField dengan panjang maksimum 100 karakter. 

    nama_kategori = models.CharField(max_length=100)

    # Metode __str__ digunakan untuk mengembalikan representasi string dari objek Kategori, yaitu nama_kategori itu sendiri.

    def __str__(self):
        return self.nama_kategori
    

class Buku(models.Model):
    # Model ini memiliki beberapa field, yaitu:
    # - judul_buku: CharField dengan panjang maksimum 200 karakter.
    # - penulis_buku: CharField dengan panjang maksimum 100 karakter.
    # - penerbit_buku: CharField dengan panjang maksimum 100 karakter.
    # - tahun_terbit: IntegerField untuk menyimpan tahun terbit buku.
    # - kategori: ForeignKey yang menghubungkan model Buku dengan model Kategori. 
    #   Jika kategori dihapus, maka semua buku yang terkait juga akan dihapus (on_delete=models.CASCADE).

    judul_buku = models.CharField(max_length=200)
    penulis_buku = models.CharField(max_length=100)
    penerbit_buku = models.CharField(max_length=100)
    tahun_terbit = models.IntegerField()
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    stok = models.PositiveIntegerField(default=0)  # Field untuk menyimpan jumlah stok buku, dengan nilai default 0.

    # Metode __str__ digunakan untuk mengembalikan representasi string dari objek Buku, yaitu judul buku itu sendiri.

    def __str__(self):
        return self.judul_buku
    
class Anggota(models.Model):
    # Model ini memiliki beberapa field, yaitu:
    # - nama: CharField dengan panjang maksimum 100 karakter.
    # - alamat: TextField untuk menyimpan alamat anggota.
    # - no_telepon: CharField dengan panjang maksimum 15 karakter untuk menyimpan nomor telepon anggota.
    # - tanggal_daftar: DateField yang secara otomatis diisi dengan tanggal saat anggota dibuat (auto_now_add=True).

    nama_anggota = models.CharField(max_length=150)
    email_anggota = models.CharField(unique=True, max_length=100)
    alamat_anggota = models.TextField()
    tanggal_daftar = models.DateField(auto_now_add=True)

    # Metode __str__ digunakan untuk mengembalikan representasi string dari objek Anggota, yaitu nama anggota itu sendiri.

    def __str__(self):
        return self.nama_anggota

class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('dipinjam', 'Dipinjam'),
        ('dikembalikan', 'Dikembalikan'),
    ]

    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dipinjam')

    def __str__(self):
        return f"{self.buku.judul_buku} - {self.anggota.nama_anggota} ({self.status})"
 