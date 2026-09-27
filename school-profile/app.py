"""SDN BATUAN 1 SUMENEP - Website Profil Sekolah + Admin Dashboard (CMS)

Versi 1: Beranda, Profil Sekolah, Berita, Galeri, Kontak + Dashboard Admin.

Cara menjalankan:
    python app.py
lalu buka http://127.0.0.1:5000
"""

import os

from flask import Flask, render_template

from config import Config
from db import close_db, get_sekolah
from routes.admin import bp as admin_bp
from routes.auth import bp as auth_bp, load_logged_in_user
from routes.public import bp as public_bp
from utils import format_tanggal, image_url


def create_app():
    """Buat objek aplikasi Flask dan daftarkan semua bagian (blueprint)."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Folder upload dibuat otomatis bila belum ada
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Bagian aplikasi
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Session admin dibaca sebelum setiap request
    load_logged_in_user(app)

    # Tutup koneksi database setelah request selesai
    app.teardown_appcontext(close_db)

    # Filter yang dipakai di template:
    #   {{ foto|gambar }}     -> url gambar (dengan gambar cadangan)
    #   {{ tanggal|tanggal }} -> tanggal format Indonesia
    app.add_template_filter(image_url, "gambar")
    app.add_template_filter(format_tanggal, "tanggal")

    # Data yang dipakai di semua template (nama sekolah, admin yang login, dll)
    @app.context_processor
    def inject_data():
        from flask import g

        return {"sekolah": get_sekolah(), "admin": g.get("admin")}

    # Halaman tidak ditemukan
    @app.errorhandler(404)
    def halaman_tidak_ada(error):
        return render_template("public/404.html", title="Halaman Tidak Ditemukan"), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)  # debug=True agar error mudah terlihat saat belajar
