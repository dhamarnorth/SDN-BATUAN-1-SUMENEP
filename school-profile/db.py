"""Koneksi database + fungsi query singkat.

Menggunakan mysql-connector-python. Satu koneksi dibuat per request
(disimpan di flask.g) lalu otomatis ditutup setelah request selesai.
"""

import mysql.connector
from flask import current_app, g


def get_db():
    """Ambil (atau buat) koneksi database untuk request ini."""
    if "db" not in g:
        cfg = current_app.config
        g.db = mysql.connector.connect(
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
            database=cfg["DB_NAME"],
            charset="utf8mb4",
        )
    return g.db


def close_db(exception=None):
    """Tutup koneksi database (dipanggil otomatis Flask)."""
    db = g.pop("db", None)
    if db is not None:
        try:
            if db.is_connected():
                db.close()
        except Exception:
            pass


def fetch_one(sql, params=()):
    """Ambil satu baris data (dictionary) atau None."""
    cur = get_db().cursor(dictionary=True)
    cur.execute(sql, params)
    row = cur.fetchone()
    cur.close()
    return row


def fetch_all(sql, params=()):
    """Ambil banyak baris data (list of dictionary)."""
    cur = get_db().cursor(dictionary=True)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def execute(sql, params=()):
    """Jalankan INSERT / UPDATE / DELETE lalu commit.

    Mengembalikan lastrowid (berguna untuk INSERT).
    """
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    db.commit()
    new_id = cur.lastrowid
    cur.close()
    return new_id


def count(sql, params=()):
    """Hitung jumlah baris hasil query (dipakai untuk pagination)."""
    row = fetch_one(sql, params)
    if not row:
        return 0
    return list(row.values())[0]


def get_sekolah():
    """Data tunggal profil/identitas sekolah (baris id = 1)."""
    return fetch_one("SELECT * FROM sekolah WHERE id = 1")
