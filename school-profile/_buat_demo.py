"""Buat preview statis dari template Flask asli (tanpa MySQL).

Jalankan:  python _buat_demo.py
Keluaran  : ../public/school-demo/  (bisa dibuka langsung di browser)

Skrip ini hanya alat bantu preview, tidak bagian dari aplikasi.
"""
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
KELUARAN = os.path.abspath(os.path.join(BASE, "..", "public", "school-demo"))
sys.path.insert(0, BASE)

import db as dbmod  # noqa: E402

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


class Row(dict):
    def __missing__(self, key):
        return ""


SEKOLAH = Row(
    id=1, nama_sekolah="SDN BATUAN 1 SUMENEP", slogan="Tumbuh, Berpikir, Berprestasi",
    tahun_berdiri=1986, kepala_sekolah="Bapak Ahmad Fauzi, S.Pd. (placeholder)",
    nip_kepsek="196805121994031005",
    ringkasan="SDN Batuan 1 adalah sekolah dasar negeri yang berada di Kecamatan Batuan, "
              "Kabupaten Sumenep, Jawa Timur. Kami menyiapkan generasi yang cinta belajar, "
              "berkarakter, dan berani berkarya.",
    sambutan="Assalamualaikum warahmatullahi wabarakatub. Segala puji bagi Tuhan Yang Maha Esa. "
             "Kami berterima kasih kepada seluruh warga sekolah yang terus bekerja sama. "
             "Dashboard sekolah ini dibuat sederhana agar mudah dikelola staf sekolah. "
             "Kami berharap SDN Batuan 1 menjadi rumah belajar yang nyaman dan menyenangkan "
             "bagi setiap anak. Wassalamualaikum warahmatullahi wabarakatub.",
    sejarah="SDN Batuan 1 berdiri pada tahun 1986 di tengah Desa Batuan, Kecamatan Batuan, "
            "Kabupaten Sumenep. Berawal dari satu bangunan sederhana, sekolah terus berkembang "
            "Bersama warga desa. Ruang kelas diperluas, laboratorium ditambahkan, dan kegiatan "
            "ekstrakurikuler makin beragam.",
    visi="Terwujudnya peserta didik yang beriman, bertakwa, berprestasi, serta berbudaya cinta tanah air.",
    misi="1. Menyelenggarakan pembelajaran yang aktif, kreatif, efektif, dan menyenangkan.\n"
         "2. Menanamkan ketakwaan dan akhlak mulia dalam setiap kegiatan sekolah.\n"
         "3. Mengembangkan bakat dan minat siswa melalui kegiatan ekstrakurikuler.\n"
         "4. Membangun lingkungan sekolah yang bersih, nyaman, dan ramah anak.\n"
         "5. Menjalin kerja sama yang baik dengan orang tua dan masyarakat.",
    foto="profil.svg", jumlah_siswa=248, jumlah_guru=18, jumlah_kelas=6,
    jumlah_prestasi=27, jumlah_ekskul=7, alamat="Dusun Sambil", desa="Batuan",
    kecamatan="Batuan", kabupaten="Sumenep", provinsi="Jawa Timur", kode_pos="62211",
    telepon="(0328) 000-0000", whatsapp="0800 0000 0000",
    email="info@sdbatuan1.example.sch.id", website="https://sdbatuan1.example.sch.id",
    maps_embed="", facebook="https://facebook.com/sdbatuan1",
    instagram="https://instagram.com/sdbatuan1", youtube="", jam_operasional="Senin - Jumat, 07.00 - 13.30 WIB",
    npsn="20531889", nss="10.02.05.0123456", jenjang="SD", created_at="2024-08-01 10:00:00",
)

BERITA = [
    ("Kegiatan Muatan Lokal Batuan", "Akademik", "pembelajaran.svg", "2024-08-12", "Guru Kelas 4A",
     "Siswa kelas IV belajar mengenal lingkungan sekitar melalui pembelajaran tematik bersama guru kelas.",
     "Pagi yang cerah, siswa kelas IV mengikuti pembelajaran tematik bersama guru kelas. Materi yang "
     "dibahas adalah mengenal lingkungan sekitar, mulai dari nama tumbuhan sampai kebiasaan gotong royong di desa.\n\n"
     "Guru menggunakan benda nyata seperti daun dan batu agar siswa lebih mudah memahami.\n\n"
     "Kegiatan ini dilakukan setiap Selasa dan Kamis di ruang kelas 4A. Orang tua siswa juga dilibatkan "
     "agar anak mendapat pengalaman tentang kehidupan desa."),
    ("Perpustakaan Sekolah Ditata Ulang", "Fasilitas", "fasilitas.svg", "2024-07-28", "Tim Perpustakaan",
     "Rak buku dipindah agar lebih rapi, pencahayaan diperbaiki, dan koleksi buku anak bertambah.",
     "Ruang baca SDN Batuan 1 selesai ditata ulang. Rak buku dipindah agar lebih rapi dan mudah "
     "dijangkau anak. Pencahayaan dan ventilasi diperbaiki sehingga ruang baca terang dan nyaman "
     "dipakai pada jam istirahat.\n\nSetiap hari Jumat dijadwalkan jam membaca bersama di perpustakaan."),
    ("Jumat Bersih dan Literasi", "Kegiatan Sekolah", "kegiatan.svg", "2024-07-19", "Wali Kelas 5B",
     "Siswa bersama guru membersihkan sekolah dan membaca bersama di perpustakaan.",
     "Setiap Jumat warga sekolah melakukan kerja bakti membersihkan kelas, taman, dan toilet. "
     "Setelah selesai, siswa membaca bersama di perpustakaan.\n\nKegiatan ini melatih kebiasaan "
     "kebersihan dan kegigihan membaca."),
    ("Pelatihan Pembelajaran Daring untuk Guru", "Akademik", "pembelajaran.svg", "2024-06-25", "Tata Usaha",
     "Guru mengikuti pelatihan membuat materi ajar sederhana yang mudah diakses siswa dari rumah.",
     "Pelatihan membahas cara membuat materi ajar sederhana yang bisa diakses siswa dari rumah.\n\n"
     "Setiap guru membuat satu paket materi sederhana sebagai tugas akhir pelatihan."),
    ("Juara Lomba Mewarnai Tingkat Kecamatan", "Prestasi", "prestasi.svg", "2024-06-10", "Wali Kelas 4A",
     "Siswa kelas IV meraih juara pada lomba mewarnai tingkat kecamatan.",
     "Siswa kelas IV mengikuti lomba mewarnai tingkat kecamatan dan meraih juara. Kegiatan ini "
     "menjadi Motivation bagi siswa lain untuk terus berlatih."),
]

PENGUMUMAN = [
    ("PPDB Tahun Ajaran 2025/2026 Telah Dibuka",
     "Pendaftaran peserta didik baru dibuka mulai 1 Juni sampai 15 Juli. Berkas dikumpulkan ke Tata Usaha pada jam kerja."),
    ("Pendaftaran Ekstrakurikuler",
     "Pendaftaran kegiatan ekstrakurikuler dibuka untuk semua siswa. Pendaftaran dilakukan setelah pulang belajar."),
]

GALERI = [
    ("Upacara Bendera Hari Senin", "Acara", "acara.svg", "2024-08-12", "Pembukaan kegiatan belajar dengan upacara bendera."),
    ("Belajar di Luar Kelas", "Pembelajaran", "pembelajaran.svg", "2024-08-08", "Pembelajaran tematik di lingkungan desa."),
    ("Latihan Pramuka", "Ekstrakurikuler", "ekstrakurikuler.svg", "2024-08-05", "Latihan rutin kepanduan setiap Sabtu pagi."),
    ("Gedung Sekolah SDN Batuan 1", "Fasilitas", "profil.svg", "2024-07-30", "Tampak depan gedung sekolah."),
    ("Siswa Peraih Penghargaan", "Prestasi", "prestasi.svg", "2024-07-22", "Siswa kelas V menerima penghargaan lomba."),
    ("Kerja Bakti Jumat", "Kegiatan Sekolah", "kegiatan.svg", "2024-07-15", "Membersihkan kelas, taman, dan toilet sekolah."),
]


def tgl(teks):
    return f"{int(teks[8:10])} {BULAN[int(teks[5:7]) - 1]} {teks[:4]}"


ROWS_BERITA = [
    Row(id=i + 1, judul=b[0], kategori=b[1], ringkasan=b[5], isi=b[6], thumbnail=b[2],
        tanggal=b[3], penulis=b[4], status="published", created_at=f"{b[3]} 09:00:00")
    for i, b in enumerate(BERITA)
]
ROWS_GALERI = [
    Row(id=i + 1, judul=g[0], kategori=g[1], keterangan=g[4], foto=g[2], tanggal=g[3],
        created_at=f"{g[3]} 08:00:00")
    for i, g in enumerate(GALERI)
]
ROWS_PENGUMUMAN = [
    Row(id=i + 1, judul=p[0], isi=p[1], tanggal_mulai="2024-06-01", tanggal_selesai="2024-07-15",
        aktif=1, created_at="2024-05-20 08:00:00")
    for i, p in enumerate(PENGUMUMAN)
]
USER = dict(id=1, username="admin",
            password="pbkdf2:sha256:600000$gz5n2YX48mk$ac114614b54df77265e2e743f51ffcc8e4219358f5cd4c608be44cbb456adb42",
            nama="Administrator Sekolah", role="admin")


def fetch_all(sql, params=()):
    q = sql.lower()
    if "from berita" in q:
        return ROWS_BERITA
    if "from galeri" in q:
        return ROWS_GALERI
    if "from pengumuman" in q:
        return ROWS_PENGUMUMAN
    if "distinct kategori" in q:
        return [Row(kategori="Akademik"), Row(kategori="Kegiatan Sekolah"), Row(kategori="Prestasi")]
    return []


def fetch_one(sql, params=()):
    q = sql.lower()
    if "from users" in q:
        return USER if params and params[0] in (1, "admin") else None
    if "from sekolah" in q:
        return SEKOLAH
    if "from berita" in q:
        if params and params[0] in (1, "2"):
            return ROWS_BERITA[int(params[0]) - 1]
        return ROWS_BERITA[0]
    if "from galeri" in q:
        return ROWS_GALERI[0]
    if "from pengumuman" in q:
        return ROWS_PENGUMUMAN[0]
    return None


dbmod.fetch_all = fetch_all
dbmod.fetch_one = fetch_one
dbmod.get_sekolah = lambda: SEKOLAH
dbmod.close_db = lambda exception=None: None

import app as appmod  # noqa: E402
import routes.admin as admin_routes  # noqa: E402
import routes.auth as auth_routes  # noqa: E402
import routes.public as public_routes  # noqa: E402

appmod.get_sekolah = lambda: SEKOLAH
appmod.close_db = lambda exception=None: None
for mod in (public_routes, admin_routes):
    mod.fetch_all = fetch_all
    mod.fetch_one = fetch_one
    mod.count = lambda sql, params=(): 9
auth_routes.fetch_one = fetch_one

app = appmod.create_app()
app.config["UPLOAD_FOLDER"] = os.path.join(BASE, "static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

PETA_URL = {
    "/": "index.html", "/profil": "profil.html", "/berita": "berita.html",
    "/berita/1": "berita-detail.html", "/galeri": "galeri.html", "/kontak": "kontak.html",
    "/admin/login": "login.html", "/admin/logout": "#", "/admin": "admin-dashboard.html",
    "/admin/": "admin-dashboard.html", "/admin/profil-sekolah": "admin-profil.html",
    "/admin/identitas-sekolah": "admin-identitas.html", "/admin/berita": "admin-berita.html",
    "/admin/berita/tambah": "admin-berita-form.html", "/admin/berita/1/ubah": "admin-berita-form.html",
    "/admin/pengumuman": "admin-pengumuman.html",
    "/admin/pengumuman/tambah": "admin-pengumuman-form.html",
    "/admin/pengumuman/1/ubah": "admin-pengumuman-form.html",
    "/admin/galeri": "admin-galeri.html", "/admin/galeri/tambah": "admin-galeri-form.html",
    "/admin/galeri/1/ubah": "admin-galeri-form.html", "/admin/akun": "admin-akun.html",
}


def rapikan(html):
    """Ganti URL Flask dengan link relatif antar file demo."""
    def ganti(match):
        attr, url = match.group(1), match.group(2)
        if url.startswith("/static/"):
            return f'{attr}="assets/{url[len("/static/"):]}"'

        # abbreviation query string (pagination, filter)
        jalur = url.split("?")[0]
        if re.fullmatch(r"/berita/\d+", jalur):
            jalur = "/berita/1"
        elif re.fullmatch(r"/admin/berita/\d+/ubah", jalur):
            jalur = "/admin/berita/tambah"
        elif re.fullmatch(r"/admin/galeri/\d+/ubah", jalur):
            jalur = "/admin/galeri/tambah"
        elif re.fullmatch(r"/admin/pengumuman/\d+/ubah", jalur):
            jalur = "/admin/pengumuman/tambah"
        elif jalur.endswith("/"):
            jalur = jalur.rstrip("/")
        return f'{attr}="{PETA_URL.get(jalur, jalur)}"'
    return re.sub(r'(href|src)="([^"]+)"', ganti, html)


def main():
    os.makedirs(KELUARAN, exist_ok=True)

    # 1. salin aset (css, js, gambar)
    for sub in ("css", "js", "images"):
        tujuan = os.path.join(KELUARAN, "assets", sub)
        shutil.rmtree(tujuan, ignore_errors=True)
        shutil.copytree(os.path.join(BASE, "static", sub), tujuan)

    client = app.test_client()
    halaman = [
        ("/", "index.html"), ("/profil", "profil.html"), ("/berita", "berita.html"),
        ("/berita/1", "berita-detail.html"), ("/galeri", "galeri.html"),
        ("/kontak", "kontak.html"), ("/admin/login", "login.html"),
    ]
    for url, nama in halaman:
        respons = client.get(url)
        with open(os.path.join(KELUARAN, nama), "w", encoding="utf-8") as berkas:
            berkas.write(rapikan(respons.get_data(as_text=True)))
        print("public:", nama, respons.status_code)

    client.post("/admin/login", data={"username": "admin", "password": "admin123"})
    halaman_admin = [
        ("/admin/", "admin-dashboard.html"), ("/admin/profil-sekolah", "admin-profil.html"),
        ("/admin/identitas-sekolah", "admin-identitas.html"), ("/admin/berita", "admin-berita.html"),
        ("/admin/berita/tambah", "admin-berita-form.html"),
        ("/admin/pengumuman", "admin-pengumuman.html"),
        ("/admin/pengumuman/tambah", "admin-pengumuman-form.html"),
        ("/admin/galeri", "admin-galeri.html"),
        ("/admin/galeri/tambah", "admin-galeri-form.html"),
        ("/admin/akun", "admin-akun.html"),
    ]
    for url, nama in halaman_admin:
        respons = client.get(url)
        with open(os.path.join(KELUARAN, nama), "w", encoding="utf-8") as berkas:
            berkas.write(rapikan(respons.get_data(as_text=True)))
        print("admin :", nama, respons.status_code)

    # 2. halaman daftar preview
    with open(os.path.join(KELUARAN, "index.html"), "w", encoding="utf-8") as berkas:
        respons = client.get("/")
        berkas.write(rapikan(respons.get_data(as_text=True)))

    tautan = [("index.html", "Beranda (public)"), ("profil.html", "Profil Sekolah"),
              ("berita.html", "Daftar Berita"), ("berita-detail.html", "Detail Berita"),
              ("galeri.html", "Galeri"), ("kontak.html", "Kontak"),
              ("login.html", "Login Admin"), ("admin-dashboard.html", "Dashboard Admin"),
              ("admin-profil.html", "Admin - Profil Sekolah"),
              ("admin-identitas.html", "Admin - Identitas Sekolah"),
              ("admin-berita.html", "Admin - Tabel Berita"),
              ("admin-berita-form.html", "Admin - Form Berita"),
              ("admin-pengumuman.html", "Admin - Pengumuman"),
              ("admin-pengumuman-form.html", "Admin - Form Pengumuman"),
              ("admin-galeri.html", "Admin - Galeri"),
              ("admin-galeri-form.html", "Admin - Form Galeri"),
              ("admin-akun.html", "Admin - Akun")]
    daftar = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in tautan)
    with open(os.path.join(KELUARAN, "daftar-halaman.html"), "w", encoding="utf-8") as berkas:
        berkas.write(
            '<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Daftar Halaman - Preview</title>'
            '<link rel="stylesheet" href="assets/css/style.css"></head><body>'
            '<div class="container" style="padding:40px 20px">'
            '<div class="section-head"><div class="kicker">// preview statis</div>'
            '<h2>Daftar Halaman Preview</h2>'
            '<p>Halaman di bawah di-generate dari template Flask asli dengan data contoh. '
            'Jalankan aplikasinya sendiri lewat <code>python app.py</code> di folder school-profile.</p></div>'
            f'<div class="card"><ul class="navlinks" style="flex-direction:column;align-items:stretch">'
            f'{daftar}</ul></div></div></body></html>'
        )
    print("selesai ->", KELUARAN)


if __name__ == "__main__":
    main()
