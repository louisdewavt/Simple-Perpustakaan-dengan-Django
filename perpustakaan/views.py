from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Kategori, Buku, Anggota, Peminjaman
from .forms import KategoriForm, BukuForm, AnggotaForm, PeminjamanForm

from django.utils import timezone
from django.db import transaction


@login_required
def dashboard(request):
    context = {
        'jumlah_kategori': Kategori.objects.count(),
        'jumlah_buku': Buku.objects.count(),
        'jumlah_anggota': Anggota.objects.count(),
        'jumlah_peminjaman': Peminjaman.objects.count(),
    }
    return render(request, 'perpustakaan/dashboard.html', context)


@login_required
def daftar_buku(request):
    keyword = request.GET.get('q')

    if keyword:
        buku = Buku.objects.filter(judul__icontains=keyword)
    else:
        buku = Buku.objects.all()

    return render(request, 'perpustakaan/daftar_buku.html', {
        'buku': buku,
        'keyword': keyword
    })


@login_required
def tambah_buku(request):
    if request.method == 'POST':
        form = BukuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data buku berhasil ditambahkan.')
            return redirect('daftar_buku')
    else:
        form = BukuForm()

    return render(request, 'perpustakaan/form_buku.html', {
        'form': form,
        'judul': 'Tambah Buku'
    })


@login_required
def edit_buku(request, id):
    buku = get_object_or_404(Buku, id=id)

    if request.method == 'POST':
        form = BukuForm(request.POST, instance=buku)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data buku berhasil diperbarui.')
            return redirect('daftar_buku')
    else:
        form = BukuForm(instance=buku)

    return render(request, 'perpustakaan/form_buku.html', {
        'form': form,
        'judul': 'Edit Buku'
    })


@login_required
def hapus_buku(request, id):
    buku = get_object_or_404(Buku, id=id)

    if request.method == 'POST':
        buku.delete()
        messages.success(request, 'Data buku berhasil dihapus.')
        return redirect('daftar_buku')

    return render(request, 'perpustakaan/konfirmasi_hapus.html', {
        'objek': buku,
        'jenis': 'Buku'
    })


@login_required
def daftar_anggota(request):
    anggota = Anggota.objects.all()
    return render(request, 'perpustakaan/daftar_anggota.html', {
        'anggota': anggota
    })


@login_required
def tambah_anggota(request):
    if request.method == 'POST':
        form = AnggotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data anggota berhasil ditambahkan.')
            return redirect('daftar_anggota')
    else:
        form = AnggotaForm()

    return render(request, 'perpustakaan/form_anggota.html', {
        'form': form,
        'judul': 'Tambah Anggota'
    })


@login_required
def edit_anggota(request, id):
    anggota = get_object_or_404(Anggota, id=id)

    if request.method == 'POST':
        form = AnggotaForm(request.POST, instance=anggota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data anggota berhasil diperbarui.')
            return redirect('daftar_anggota')
    else:
        form = AnggotaForm(instance=anggota)

    return render(request, 'perpustakaan/form_anggota.html', {
        'form': form,
        'judul': 'Edit Anggota'
    })


@login_required
def hapus_anggota(request, id):
    anggota = get_object_or_404(Anggota, id=id)

    if request.method == 'POST':
        anggota.delete()
        messages.success(request, 'Data anggota berhasil dihapus.')
        return redirect('daftar_anggota')

    return render(request, 'perpustakaan/konfirmasi_hapus.html', {
        'objek': anggota,
        'jenis': 'Anggota'
    })


@login_required
def daftar_peminjaman(request):
    peminjaman = Peminjaman.objects.select_related('buku', 'anggota').all()
    return render(request, 'perpustakaan/daftar_peminjaman.html', {
        'peminjaman': peminjaman
    })


@login_required
def tambah_peminjaman(request):
    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                peminjaman = form.save(commit=False)

                buku = Buku.objects.select_for_update().get(id=peminjaman.buku.id)
                if buku.stok <= 0:
                    form.add_error(
                        'buku',
                        'Stok buku ini sudah habis.'
                    )
                else:
                    peminjaman.status = 'dipinjam'
                    peminjaman.tanggal_kembali = None
                    peminjaman.save()

                    buku.stok -= 1
                    buku.save(update_fields=['stok'])

                    return redirect('daftar_peminjaman')
            
    else:
        form = PeminjamanForm()

    return render(request, 'perpustakaan/form_peminjaman.html', {
        'form': form,
        'judul': 'Tambah Peminjaman'
    })

@login_required
def kembalikan_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if request.method == 'POST':
        with transaction.atomic():
            peminjaman = Peminjaman.objects.select_for_update().get(
                id=id
            )

            if peminjaman.status == 'dipinjam':
                buku = Buku.objects.select_for_update().get(
                    id=peminjaman.buku_id
                )

                peminjaman.status = 'dikembalikan'
                peminjaman.tanggal_kembali = timezone.localdate()
                peminjaman.save(
                    update_fields=['status', 'tanggal_kembali']
                )

                buku.stok += 1
                buku.save(update_fields=['stok'])

        return redirect('daftar_peminjaman')

    return redirect('daftar_peminjaman')

@login_required
def edit_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if request.method == 'POST':
        form = PeminjamanForm(request.POST, instance=peminjaman)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data peminjaman berhasil diperbarui.')
            return redirect('daftar_peminjaman')
    else:
        form = PeminjamanForm(instance=peminjaman)

    return render(request, 'perpustakaan/form_peminjaman.html', {
        'form': form,
        'judul': 'Edit Peminjaman'
    })


@login_required
def hapus_peminjaman(request, id):
    peminjaman = get_object_or_404(Peminjaman, id=id)

    if request.method == 'POST':
        peminjaman.delete()
        messages.success(request, 'Data peminjaman berhasil dihapus.')
        return redirect('daftar_peminjaman')

    return render(request, 'perpustakaan/konfirmasi_hapus.html', {
        'objek': peminjaman,
        'jenis': 'Peminjaman'
    })


@login_required
def daftar_kategori(request):
    kategori = Kategori.objects.all().order_by('nama_kategori')
    return render(
        request,
        'perpustakaan/daftar_kategori.html',
        {'kategori': kategori}
    )


@login_required
def tambah_kategori(request):
    if request.method == 'POST':
        form = KategoriForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('daftar_kategori')
    else:
        form = KategoriForm()

    return render(
        request,
        'perpustakaan/form_kategori.html',
        {'form': form}
    )

@login_required
def edit_kategori(request, id):
    kategori = get_object_or_404(Kategori, id=id)

    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)

        if form.is_valid():
            form.save()
            return redirect('daftar_kategori')
    else:
        form = KategoriForm(instance=kategori)

    return render(
        request,
        'perpustakaan/form_kategori.html',
        {
            'form': form,
            'judul': 'Edit Kategori',
        }
    )


@login_required
def hapus_kategori(request, id):
    kategori = get_object_or_404(Kategori, id=id)

    if request.method == 'POST':
        kategori.delete()
        return redirect('daftar_kategori')

    return render(
        request,
        'perpustakaan/konfirmasi_hapus.html',
        {'objek': kategori, 'jenis': 'Kategori'}
    )