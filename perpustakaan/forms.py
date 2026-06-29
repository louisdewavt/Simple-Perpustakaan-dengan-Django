from django import forms
from .models import Kategori, Buku, Anggota, Peminjaman
from django.contrib.auth.models import User


class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama_kategori']

class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ['judul_buku', 'penulis_buku', 'penerbit_buku', 'tahun_terbit', 'kategori', 'stok']

class AnggotaForm(forms.ModelForm):
    class Meta:
        model = Anggota
        fields = ['nama_anggota', 'email_anggota', 'alamat_anggota']

class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        fields = ['anggota', 'buku', 'tanggal_pinjam', 'tanggal_kembali', 'status']
        widgets = {
            'tanggal_pinjam': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_kembali': forms.DateInput(attrs={'type': 'date'}),
        }

class EditUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Username baru',
        }