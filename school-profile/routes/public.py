"""Route untuk website publik (tanpa login).

Semua data diambil langsung dari MySQL, jadi perubahan dari dashboard
admin langsung terlihat di halaman publik.
"""

from flask import Blueprint, abort, current_app, render_template, request

from db import count, fetch_all

bp = Blueprint("public", __name__)

# Kategori galeri yang dipakai di filter
KATEGORI_GALERI = [
    "Kegiatan Sekolah",
    "Pembelajaran",
    "Ekstrakurikuler",
    "Prestasi",
    "Fasilitas",
    "Acara",
]


def _paginasi(total, per_halaman, halaman):
    """Hitung data pagination sederhana."""
    per_halaman = max(1, per_halaman)
    total_halaman = max(1, (total + per_halaman - 1) // per_halaman)
    halaman = min(max(1, halaman), total_halaman)
    return {
        "halaman": halaman,
        "total_halaman": total_halaman,
        "offset": (halaman - 1) * per_halaman,
        "total": total,
    }


@bp.route("/")
def index():
    """Beranda: hero, pengumuman, statistik, berita & galeri terbaru."""
    pengumuman = fetch_all(
        "SELECT * FROM pengumuman WHERE aktif = 1 AND (tanggal_mulai IS NULL "
        "OR tanggal_mulai <= CURDATE()) AND (tanggal_selesai IS NULL "
        "OR tanggal_selesai >= CURDATE()) ORDER BY tanggal_mulai DESC, id DESC LIMIT 3"
    )
    berita_terbaru = fetch_all(
        "SELECT * FROM berita WHERE status = 'published' "
        "ORDER BY tanggal DESC, id DESC LIMIT 3"
    )
    galeri_terbaru = fetch_all(
        "SELECT * FROM galeri ORDER BY tanggal DESC, id DESC LIMIT 6"
    )

    return render_template(
        "public/index.html",
        title="Beranda",
        pengumuman=pengumuman,
        berita=berita_terbaru,
        galeri=galeri_terbaru,
    )


@bp.route("/profil")
def profil():
    """Halaman profil sekolah: sambutan, sejarah, visi, misi, identitas."""
    return render_template("public/profil.html", title="Profil Sekolah")


@bp.route("/berita")
def berita():
    """Daftar berita + pencarian + filter kategori + pagination."""
    kata_kunci = request.args.get("q", "").strip()
    kategori = request.args.get("kategori", "").strip()
    halaman = request.args.get("halaman", 1, type=int)

    kondisi = ["status = 'published'"]
    params = []
    if kata_kunci:
        kondisi.append("(judul LIKE %s OR ringkasan LIKE %s)")
        params += [f"%{kata_kunci}%", f"%{kata_kunci}%"]
    if kategori:
        kondisi.append("kategori = %s")
        params.append(kategori)

    where = " AND ".join(kondisi)
    per_halaman = current_app.config["ITEMS_PER_PAGE"]
    total = count(f"SELECT COUNT(*) FROM berita WHERE {where}", tuple(params))
    pag = _paginasi(total, per_halaman, halaman)

    data = fetch_all(
        f"SELECT * FROM berita WHERE {where} ORDER BY tanggal DESC, id DESC "
        "LIMIT %s OFFSET %s",
        tuple(params + [per_halaman, pag["offset"]]),
    )
    kategori_list = fetch_all(
        "SELECT DISTINCT kategori FROM berita WHERE kategori <> '' ORDER BY kategori"
    )

    return render_template(
        "public/berita.html",
        title="Berita Sekolah",
        berita=data,
        kategori_list=kategori_list,
        kategori_aktif=kategori,
        kata_kunci=kata_kunci,
        pag=pag,
    )


@bp.route("/berita/<int:berita_id>")
def detail_berita(berita_id):
    """Detail satu berita."""
    from db import fetch_one

    item = fetch_one(
        "SELECT * FROM berita WHERE id = %s AND status = 'published'", (berita_id,)
    )
    if not item:
        abort(404)

    lain = fetch_all(
        "SELECT id, judul, tanggal, thumbnail FROM berita "
        "WHERE id <> %s AND status = 'published' ORDER BY tanggal DESC LIMIT 3",
        (berita_id,),
    )
    return render_template(
        "public/detail_berita.html", title=item["judul"], berita=item, berita_lain=lain
    )


@bp.route("/galeri")
def galeri():
    """Galeri foto sekolah dengan filter kategori."""
    kategori = request.args.get("kategori", "").strip()

    if kategori:
        data = fetch_all(
            "SELECT * FROM galeri WHERE kategori = %s ORDER BY tanggal DESC, id DESC",
            (kategori,),
        )
    else:
        data = fetch_all("SELECT * FROM galeri ORDER BY tanggal DESC, id DESC")

    return render_template(
        "public/galeri.html",
        title="Galeri",
        galeri=data,
        kategori_list=KATEGORI_GALERI,
        kategori_aktif=kategori,
    )


@bp.route("/kontak")
def kontak():
    """Informasi kontak sekolah (alamat, telepon, email, media sosial)."""
    return render_template("public/kontak.html", title="Kontak")
