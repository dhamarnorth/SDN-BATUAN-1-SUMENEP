"""Route dashboard admin (CMS).

Semua route di blueprint ini memakai @login_required, jadi admin yang
belum login tidak bisa membuka halaman dashboard.
"""

import math

from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.security import generate_password_hash

from db import count, execute, fetch_all, fetch_one
from utils import bersihkan_teks, delete_image, save_image

bp = Blueprint("admin", __name__, url_prefix="/admin")


# --------------------------------------------------------------------------
# Proteksi route: semua halaman dashboard hanya untuk admin yang sudah login
# --------------------------------------------------------------------------
@bp.before_request
def _harus_login():
    if g.get("admin") is None:
        flash("Silakan login terlebih dahulu untuk membuka dashboard.", "warning")
        return redirect(url_for("auth.login", next=request.path))


# --------------------------------------------------------------------------
# Helper
# --------------------------------------------------------------------------
def _wajib(nama, label):
    """Ambil nilai wajib dari form; jika kosong akan_flash + return None."""
    nilai = bersihkan_teks(request.form.get(nama, ""), 5000)
    if not nilai:
        flash(f"{label} wajib diisi.", "error")
    return nilai


def _angka(nama, label):
    """Ambil nilai angka dari form (default 0 bila kosong)."""
    mentah = request.form.get(nama, "0").strip()
    try:
        return int(mentah or 0)
    except ValueError:
        flash(f"{label} harus berupa angka.", "error")
        return 0


def _gambar_akhir(nama_lama, nama_baru):
    """Tentukan nama gambar yang akan dipakai.

    - Ada upload baru  -> pakai nama baru
    - Admin centang "hapus gambar" dan tidak ada upload baru -> gambar dihapus
    - Selain itu -> tetap memakai gambar lama
    """
    if nama_baru:
        return nama_baru
    if request.form.get("hapus_gambar") and nama_lama:
        delete_image(nama_lama)
        return None
    return nama_lama


# --------------------------------------------------------------------------
# Dashboard
# --------------------------------------------------------------------------
@bp.route("/")
@bp.route("")
def dashboard():
    """Ringkasan jumlah data + aktivitas terbaru."""
    statistik = {
        "berita": count("SELECT COUNT(*) FROM berita"),
        "pengumuman": count("SELECT COUNT(*) FROM pengumuman"),
        "galeri": count("SELECT COUNT(*) FROM galeri"),
        "profil": 1,
    }

    aktivitas = []
    for tabel, label, judul in (
        ("berita", "Berita", "judul"),
        ("pengumuman", "Pengumuman", "judul"),
        ("galeri", "Galeri", "judul"),
    ):
        for row in fetch_all(
            f"SELECT id, {judul} AS nama, created_at FROM {tabel} "
            "ORDER BY created_at DESC, id DESC LIMIT 3"
        ):
            row["jenis"] = label
            aktivitas.append(row)
    aktivitas.sort(key=lambda r: str(r["created_at"]), reverse=True)
    aktivitas = aktivitas[:8]

    return render_template(
        "admin/dashboard.html", title="Dashboard", statistik=statistik, aktivitas=aktivitas
    )


# --------------------------------------------------------------------------
# 1. Profil Sekolah
# --------------------------------------------------------------------------
@bp.route("/profil-sekolah", methods=("GET", "POST"))
def profil_sekolah():
    """Form ubah isi profil sekolah (sambutan, sejarah, visi, misi, dll)."""
    from db import get_sekolah

    sekolah = get_sekolah()

    if request.method == "POST":
        nama = _wajib("nama_sekolah", "Nama sekolah")
        kepala = _wajib("kepala_sekolah", "Nama kepala sekolah")
        visi = _wajib("visi", "Visi")
        misi = _wajib("misi", "Misi")

        try:
            foto_baru = save_image(request.files.get("foto"), prefix="profil")
        except ValueError as pesan:
            flash(str(pesan), "error")
            foto_baru = None

        execute(
            """
            UPDATE sekolah SET
                nama_sekolah = %s, npsn = %s, jenjang = %s, tahun_berdiri = %s,
                kepala_sekolah = %s, nip_kepsek = %s, slogan = %s, ringkasan = %s,
                sambutan = %s, sejarah = %s, visi = %s, misi = %s,
                foto = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
            """,
            (
                nama,
                bersihkan_teks(request.form.get("npsn", ""), 50),
                bersihkan_teks(request.form.get("jenjang", "SD"), 30),
                _angka("tahun_berdiri", "Tahun berdiri"),
                kepala,
                bersihkan_teks(request.form.get("nip_kepsek", ""), 50),
                bersihkan_teks(request.form.get("slogan", ""), 200),
                bersihkan_teks(request.form.get("ringkasan", ""), 2000),
                bersihkan_teks(request.form.get("sambutan", ""), 5000),
                bersihkan_teks(request.form.get("sejarah", ""), 5000),
                visi,
                misi,
                _gambar_akhir(sekolah["foto"], foto_baru),
            ),
        )
        flash("Profil sekolah berhasil disimpan.", "success")
        return redirect(url_for("admin.profil_sekolah"))

    return render_template(
        "admin/profil_sekolah.html", title="Profil Sekolah", sekolah=sekolah
    )


# --------------------------------------------------------------------------
# 2. Identitas Sekolah + statistik + kontak
# --------------------------------------------------------------------------
@bp.route("/identitas-sekolah", methods=("GET", "POST"))
def identitas_sekolah():
    """Form ubah identitas, kontak, statistik, dan link media sosial."""
    from db import get_sekolah

    sekolah = get_sekolah()

    if request.method == "POST":
        execute(
            """
            UPDATE sekolah SET
                nss = %s, npsn = %s, alamat = %s, desa = %s, kecamatan = %s,
                kabupaten = %s, provinsi = %s, kode_pos = %s,
                telepon = %s, whatsapp = %s, email = %s, website = %s,
                maps_embed = %s, facebook = %s, instagram = %s, youtube = %s,
                jam_operasional = %s,
                jumlah_siswa = %s, jumlah_guru = %s, jumlah_kelas = %s,
                jumlah_prestasi = %s, jumlah_ekskul = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
            """,
            (
                bersihkan_teks(request.form.get("nss", ""), 30),
                bersihkan_teks(request.form.get("npsn", ""), 50),
                bersihkan_teks(request.form.get("alamat", ""), 500),
                bersihkan_teks(request.form.get("desa", ""), 100),
                bersihkan_teks(request.form.get("kecamatan", ""), 100),
                bersihkan_teks(request.form.get("kabupaten", ""), 100),
                bersihkan_teks(request.form.get("provinsi", ""), 100),
                bersihkan_teks(request.form.get("kode_pos", ""), 10),
                bersihkan_teks(request.form.get("telepon", ""), 30),
                bersihkan_teks(request.form.get("whatsapp", ""), 30),
                bersihkan_teks(request.form.get("email", ""), 100),
                bersihkan_teks(request.form.get("website", ""), 100),
                bersihkan_teks(request.form.get("maps_embed", ""), 500),
                bersihkan_teks(request.form.get("facebook", ""), 200),
                bersihkan_teks(request.form.get("instagram", ""), 200),
                bersihkan_teks(request.form.get("youtube", ""), 200),
                bersihkan_teks(request.form.get("jam_operasional", ""), 200),
                _angka("jumlah_siswa", "Jumlah siswa"),
                _angka("jumlah_guru", "Jumlah guru"),
                _angka("jumlah_kelas", "Jumlah kelas"),
                _angka("jumlah_prestasi", "Jumlah prestasi"),
                _angka("jumlah_ekskul", "Jumlah ekskul"),
            ),
        )
        flash("Identitas sekolah dan statistik berhasil disimpan.", "success")
        return redirect(url_for("admin.identitas_sekolah"))

    return render_template(
        "admin/identitas_sekolah.html", title="Identitas Sekolah", sekolah=sekolah
    )


# --------------------------------------------------------------------------
# 3. Berita
# --------------------------------------------------------------------------
@bp.route("/berita")
def berita():
    """Tabel berita + pencarian + filter + pagination."""
    kata_kunci = request.args.get("q", "").strip()
    kategori = request.args.get("kategori", "").strip()
    halaman = request.args.get("halaman", 1, type=int)

    kondisi = ["1 = 1"]
    params = []
    if kata_kunci:
        kondisi.append("(judul LIKE %s OR ringkasan LIKE %s)")
        params += [f"%{kata_kunci}%", f"%{kata_kunci}%"]
    if kategori:
        kondisi.append("kategori = %s")
        params.append(kategori)
    where = " AND ".join(kondisi)

    per_halaman = 8
    total = count(f"SELECT COUNT(*) FROM berita WHERE {where}", tuple(params))
    total_halaman = max(1, math.ceil(total / per_halaman))
    halaman = min(max(1, halaman), total_halaman)
    offset = (halaman - 1) * per_halaman

    data = fetch_all(
        f"SELECT * FROM berita WHERE {where} ORDER BY created_at DESC, id DESC "
        "LIMIT %s OFFSET %s",
        tuple(params + [per_halaman, offset]),
    )
    kategori_list = fetch_all(
        "SELECT DISTINCT kategori FROM berita WHERE kategori <> '' ORDER BY kategori"
    )

    return render_template(
        "admin/berita.html",
        title="Berita",
        berita=data,
        kategori_list=kategori_list,
        kategori_aktif=kategori,
        kata_kunci=kata_kunci,
        halaman=halaman,
        total_halaman=total_halaman,
        total=total,
    )


def _form_berita(berita=None):
    """Tampilan form tambah/ubah berita."""
    return render_template(
        "admin/berita_form.html",
        title="Tambah Berita" if not berita else "Ubah Berita",
        berita=berita,
    )


@bp.route("/berita/tambah", methods=("GET", "POST"))
def berita_tambah():
    if request.method == "POST":
        judul = _wajib("judul", "Judul berita")
        isi = _wajib("isi", "Isi berita")
        try:
            thumbnail = save_image(request.files.get("thumbnail"), prefix="berita")
        except ValueError as pesan:
            flash(str(pesan), "error")
            thumbnail = None

        if judul and isi:
            execute(
                """
                INSERT INTO berita (judul, kategori, ringkasan, isi, thumbnail,
                                    tanggal, penulis, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    judul,
                    bersihkan_teks(request.form.get("kategori", ""), 50),
                    bersihkan_teks(request.form.get("ringkasan", ""), 1000),
                    isi,
                    thumbnail,
                    request.form.get("tanggal") or None,
                    bersihkan_teks(request.form.get("penulis", ""), 100)
                    or g.admin["nama"],
                    request.form.get("status", "published"),
                ),
            )
            flash("Berita berhasil ditambahkan.", "success")
            return redirect(url_for("admin.berita"))

    return _form_berita()


@bp.route("/berita/<int:berita_id>/ubah", methods=("GET", "POST"))
def berita_ubah(berita_id):
    data = fetch_one("SELECT * FROM berita WHERE id = %s", (berita_id,))
    if not data:
        abort(404)

    if request.method == "POST":
        judul = _wajib("judul", "Judul berita")
        isi = _wajib("isi", "Isi berita")
        try:
            thumbnail_baru = save_image(request.files.get("thumbnail"), prefix="berita")
        except ValueError as pesan:
            flash(str(pesan), "error")
            thumbnail_baru = None

        if judul and isi:
            execute(
                """
                UPDATE berita SET judul = %s, kategori = %s, ringkasan = %s, isi = %s,
                    thumbnail = %s, tanggal = %s, penulis = %s, status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    judul,
                    bersihkan_teks(request.form.get("kategori", ""), 50),
                    bersihkan_teks(request.form.get("ringkasan", ""), 1000),
                    isi,
                    _gambar_akhir(data["thumbnail"], thumbnail_baru),
                    request.form.get("tanggal") or None,
                    bersihkan_teks(request.form.get("penulis", ""), 100)
                    or data["penulis"],
                    request.form.get("status", "published"),
                    berita_id,
                ),
            )
            flash("Berita berhasil diperbarui.", "success")
            return redirect(url_for("admin.berita"))

    return _form_berita(data)


@bp.route("/berita/<int:berita_id>/hapus", methods=("POST",))
def berita_hapus(berita_id):
    data = fetch_one("SELECT * FROM berita WHERE id = %s", (berita_id,))
    if not data:
        abort(404)
    delete_image(data["thumbnail"])
    execute("DELETE FROM berita WHERE id = %s", (berita_id,))
    flash("Berita berhasil dihapus.", "success")
    return redirect(url_for("admin.berita"))


# --------------------------------------------------------------------------
# 4. Pengumuman
# --------------------------------------------------------------------------
@bp.route("/pengumuman")
def pengumuman():
    data = fetch_all("SELECT * FROM pengumuman ORDER BY created_at DESC, id DESC")
    return render_template(
        "admin/pengumuman.html", title="Pengumuman", pengumuman=data
    )


def _form_pengumuman(item=None):
    return render_template(
        "admin/pengumuman_form.html",
        title="Tambah Pengumuman" if not item else "Ubah Pengumuman",
        item=item,
    )


@bp.route("/pengumuman/tambah", methods=("GET", "POST"))
def pengumuman_tambah():
    if request.method == "POST":
        judul = _wajib("judul", "Judul pengumuman")
        isi = _wajib("isi", "Isi pengumuman")
        if judul and isi:
            execute(
                """
                INSERT INTO pengumuman (judul, isi, tanggal_mulai, tanggal_selesai, aktif)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    judul,
                    isi,
                    request.form.get("tanggal_mulai") or None,
                    request.form.get("tanggal_selesai") or None,
                    1 if request.form.get("aktif") else 0,
                ),
            )
            flash("Pengumuman berhasil ditambahkan.", "success")
            return redirect(url_for("admin.pengumuman"))
    return _form_pengumuman()


@bp.route("/pengumuman/<int:pengumuman_id>/ubah", methods=("GET", "POST"))
def pengumuman_ubah(pengumuman_id):
    data = fetch_one("SELECT * FROM pengumuman WHERE id = %s", (pengumuman_id,))
    if not data:
        abort(404)

    if request.method == "POST":
        judul = _wajib("judul", "Judul pengumuman")
        isi = _wajib("isi", "Isi pengumuman")
        if judul and isi:
            execute(
                """
                UPDATE pengumuman SET judul = %s, isi = %s, tanggal_mulai = %s,
                    tanggal_selesai = %s, aktif = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    judul,
                    isi,
                    request.form.get("tanggal_mulai") or None,
                    request.form.get("tanggal_selesai") or None,
                    1 if request.form.get("aktif") else 0,
                    pengumuman_id,
                ),
            )
            flash("Pengumuman berhasil diperbarui.", "success")
            return redirect(url_for("admin.pengumuman"))
    return _form_pengumuman(data)


@bp.route("/pengumuman/<int:pengumuman_id>/hapus", methods=("POST",))
def pengumuman_hapus(pengumuman_id):
    if not fetch_one("SELECT id FROM pengumuman WHERE id = %s", (pengumuman_id,)):
        abort(404)
    execute("DELETE FROM pengumuman WHERE id = %s", (pengumuman_id,))
    flash("Pengumuman berhasil dihapus.", "success")
    return redirect(url_for("admin.pengumuman"))


# --------------------------------------------------------------------------
# 5. Galeri
# --------------------------------------------------------------------------
@bp.route("/galeri")
def galeri():
    kategori = request.args.get("kategori", "").strip()
    if kategori:
        data = fetch_all(
            "SELECT * FROM galeri WHERE kategori = %s ORDER BY created_at DESC, id DESC",
            (kategori,),
        )
    else:
        data = fetch_all("SELECT * FROM galeri ORDER BY created_at DESC, id DESC")

    kategori_list = fetch_all(
        "SELECT DISTINCT kategori FROM galeri WHERE kategori <> '' ORDER BY kategori"
    )
    return render_template(
        "admin/galeri.html",
        title="Galeri",
        galeri=data,
        kategori_list=kategori_list,
        kategori_aktif=kategori,
    )


def _form_galeri(item=None):
    return render_template(
        "admin/galeri_form.html",
        title="Tambah Foto" if not item else "Ubah Foto",
        item=item,
    )


@bp.route("/galeri/tambah", methods=("GET", "POST"))
def galeri_tambah():
    if request.method == "POST":
        judul = _wajib("judul", "Judul foto")
        try:
            foto = save_image(request.files.get("foto"), prefix="galeri")
        except ValueError as pesan:
            flash(str(pesan), "error")
            foto = None
        if not foto:
            flash("Pilih foto yang ingin diunggah (JPG/JPEG/PNG/WEBP).", "error")

        if judul and foto:
            execute(
                """
                INSERT INTO galeri (judul, kategori, keterangan, foto, tanggal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    judul,
                    bersihkan_teks(request.form.get("kategori", "Kegiatan Sekolah"), 50),
                    bersihkan_teks(request.form.get("keterangan", ""), 1000),
                    foto,
                    request.form.get("tanggal") or None,
                ),
            )
            flash("Foto berhasil ditambahkan ke galeri.", "success")
            return redirect(url_for("admin.galeri"))
    return _form_galeri()


@bp.route("/galeri/<int:galeri_id>/ubah", methods=("GET", "POST"))
def galeri_ubah(galeri_id):
    data = fetch_one("SELECT * FROM galeri WHERE id = %s", (galeri_id,))
    if not data:
        abort(404)

    if request.method == "POST":
        judul = _wajib("judul", "Judul foto")
        try:
            foto_baru = save_image(request.files.get("foto"), prefix="galeri")
        except ValueError as pesan:
            flash(str(pesan), "error")
            foto_baru = None
        if judul:
            execute(
                """
                UPDATE galeri SET judul = %s, kategori = %s, keterangan = %s,
                    foto = %s, tanggal = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (
                    judul,
                    bersihkan_teks(request.form.get("kategori", "Kegiatan Sekolah"), 50),
                    bersihkan_teks(request.form.get("keterangan", ""), 1000),
                    _gambar_akhir(data["foto"], foto_baru),
                    request.form.get("tanggal") or data["tanggal"],
                    galeri_id,
                ),
            )
            flash("Foto berhasil diperbarui.", "success")
            return redirect(url_for("admin.galeri"))
    return _form_galeri(data)


@bp.route("/galeri/<int:galeri_id>/hapus", methods=("POST",))
def galeri_hapus(galeri_id):
    data = fetch_one("SELECT * FROM galeri WHERE id = %s", (galeri_id,))
    if not data:
        abort(404)
    delete_image(data["foto"])
    execute("DELETE FROM galeri WHERE id = %s", (galeri_id,))
    flash("Foto berhasil dihapus dari galeri.", "success")
    return redirect(url_for("admin.galeri"))


# --------------------------------------------------------------------------
# 6. Akun Admin
# --------------------------------------------------------------------------
@bp.route("/akun", methods=("GET", "POST"))
def akun():
    """Ganti username & password admin yang sedang login."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password_baru = request.form.get("password_baru", "")
        konfirmasi = request.form.get("password_konfirmasi", "")

        if not username:
            flash("Username wajib diisi.", "error")
        elif password_baru and password_baru != konfirmasi:
            flash("Password baru dan konfirmasi tidak sama.", "error")
        elif len(password_baru) < 6:
            flash("Password minimal 6 karakter.", "error")
        else:
            if password_baru:
                execute(
                    "UPDATE users SET password = %s WHERE id = %s",
                    (generate_password_hash(password_baru), g.admin["id"]),
                )
            execute("UPDATE users SET username = %s WHERE id = %s", (username, g.admin["id"]))
            flash("Akun admin berhasil diperbarui.", "success")
            return redirect(url_for("admin.akun"))

    return render_template("admin/akun.html", title="Akun Admin", admin=g.admin)
