from django.contrib import admin
from .models import Kategori, Buku, Anggota, Peminjaman

# Register your models here.


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_kategori')
    search_fields = ('nama_kategori',)


@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('id', 'judul_buku', 'penulis_buku', 'penerbit_buku', 'tahun_terbit', 'kategori', 'stok')
    search_fields = ('judul_buku', 'penulis_buku', 'penerbit_buku')
    list_filter = ('kategori','tahun_terbit')


@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_anggota', 'email_anggota', 'alamat_anggota', 'tanggal_daftar')
    search_fields = ('nama_anggota', 'email_anggota')

@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ('id', 'anggota', 'buku', 'tanggal_pinjam', 'tanggal_kembali', 'status')
    search_fields = ('anggota__nama_anggota', 'buku__judul_buku')
    list_filter = ('status',)
