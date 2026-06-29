from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('buku/', views.daftar_buku, name='daftar_buku'),
    path('buku/tambah/', views.tambah_buku, name='tambah_buku'),
    path('buku/edit/<int:id>/', views.edit_buku, name='edit_buku'),
    path('buku/hapus/<int:id>/', views.hapus_buku, name='hapus_buku'),

    path('anggota/', views.daftar_anggota, name='daftar_anggota'),
    path('anggota/tambah/', views.tambah_anggota, name='tambah_anggota'),
    path('anggota/edit/<int:id>/', views.edit_anggota, name='edit_anggota'),
    path('anggota/hapus/<int:id>/', views.hapus_anggota, name='hapus_anggota'),

    path('peminjaman/', views.daftar_peminjaman, name='daftar_peminjaman'),
    path('peminjaman/tambah/', views.tambah_peminjaman, name='tambah_peminjaman'),
    path('peminjaman/edit/<int:id>/', views.edit_peminjaman, name='edit_peminjaman'),
    path('peminjaman/hapus/<int:id>/', views.hapus_peminjaman, name='hapus_peminjaman'),

    path('kategori/', views.daftar_kategori, name='daftar_kategori'),
    path('kategori/tambah/', views.tambah_kategori, name='tambah_kategori'),
]