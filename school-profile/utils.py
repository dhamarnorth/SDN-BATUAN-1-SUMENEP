"""Helper kecil: upload gambar & format tanggal.

Aturan upload:
- hanya extension JPG, JPEG, PNG, WEBP
- nama file dibersihkan (secure_filename) lalu diberi kode acak
- database hanya menyimpan NAMA FILE, bukan isi gambar
"""

import os
import uuid
from datetime import date, datetime

from flask import current_app, url_for
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """True jika extension file ada di daftar yang diizinkan."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_image(file_storage, prefix="img"):
    """Simpan file gambar ke static/uploads/.

    Mengembalikan NAMA FILE (contoh: berita_1a2b3c4d.jpg) atau None
    kalau tidak ada file yang dipilih. Mengafaalkan ValueError bila
    extension tidak diizinkan.
    """
    if file_storage is None or not file_storage.filename:
        return None

    if not allowed_file(file_storage.filename):
        raise ValueError("Format gambar harus JPG, JPEG, PNG, atau WEBP.")

    # secure_filename membersihkan nama file dari karakter berbahaya
    nama_aman = secure_filename(file_storage.filename)
    ext = nama_aman.rsplit(".", 1)[1].lower()
    nama_file = f"{prefix}_{uuid.uuid4().hex[:8]}.{ext}"

    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)
    file_storage.save(os.path.join(folder, nama_file))
    return nama_file


def delete_image(nama_file):
    """Hapus file gambar dari folder upload (dipakai saat data dihapus)."""
    if not nama_file:
        return
    folder = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(folder, os.path.basename(nama_file))
    if os.path.isfile(path):
        try:
            os.remove(path)
        except OSError:
            pass


def image_url(nama_file, fallback="images/placeholder.svg"):
    """URL gambar dari nama file di database, dengan gambar cadangan.

    Data gambar bisa berasal dari dua sumber:
    - file hasil upload admin  -> static/uploads/<nama_file>
    - gambar contoh bawaan    -> static/images/<nama_file>
    """
    if not nama_file:
        return url_for("static", filename=fallback)

    nama_file = str(nama_file)
    if nama_file.startswith("images/") or nama_file.lower().endswith(".svg"):
        return url_for("static", filename=nama_file)
    return url_for("static", filename="uploads/" + nama_file)


BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def format_tanggal(tgl, dengan_waktu=False):
    """Ubah tanggal dari database menjadi '12 Agustus 2024'."""
    if not tgl:
        return "-"
    if isinstance(tgl, (datetime, date)):
        teks = f"{tgl.day:02d} {BULAN[tgl.month - 1]} {tgl.year}"
        if dengan_waktu and isinstance(tgl, datetime):
            teks += f" {tgl:%H:%M}"
        return teks
    return str(tgl)


def bersihkan_teks(nilai, panjang_maks=5000):
    """Rapikan input teks: buang spasi berlebih, potong panjang maksimal."""
    if nilai is None:
        return ""
    teks = " ".join(str(nilai).split())
    return teks[:panjang_maks]
