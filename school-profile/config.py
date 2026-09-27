"""Konfigurasi aplikasi.

Semua pengaturan database ada di sini supaya mudah diubah.
Nilai default mengikuti XAMPP standar (user root, password kosong, port 3306).
"""

import os

# Folder tempat file app.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    # --- Keamanan session -------------------------------------------------
    # Ganti string ini bila aplikasi dipakai di server publik.
    SECRET_KEY = os.environ.get("SECRET_KEY", "ganti-secret-key-ini-untuk-produksi")

    # --- Database MySQL / MariaDB (XAMPP) ---------------------------------
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")  # XAMPP: password root kosong
    DB_NAME = os.environ.get("DB_NAME", "sekolah_profile")

    # --- Upload gambar ----------------------------------------------------
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # maksimal 5 MB per file
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

    # --- Tampilan ---------------------------------------------------------
    ITEMS_PER_PAGE = 6  # jumlah item per halaman di website public
    ADMIN_ITEMS_PER_PAGE = 8  # jumlah baris per halaman di dashboard admin
