# Website Profil Sekolah + Admin Dashboard (CMS)

**SDN BATUAN 1 SUMENEP** &#183; Flask + MySQL/MariaDB (XAMPP)

Aplikasi sederhana dengan dua bagian:

1. **Website Publik** &#8212; beranda, profil sekolah, berita, galeri, dan kontak.
2. **Admin Dashboard** &#8212; login staf sekolah, lalu ubah semua konten website
   (profil, visi-misi, berita, pengumuman, galeri, kontak, dan statistik).

Semua data disimpan di **MySQL/MariaDB**. Admin mengubah data &#8594; data langsung
muncul di website publik tanpa perlu menyentuh kode.

---

## 1. Fitur Versi 1

### Website publik

| Halaman | Isi |
| --- | --- |
| Beranda (`/`) | Hero sekolah, pengumuman, ringkasan profil, kartu statistik, berita terbaru, galeri terbaru, kontak singkat |
| Profil (`/profil`) | Sambutan kepala sekolah, statistik, sejarah, visi, misi, tabel identitas sekolah |
| Berita (`/berita`) | Daftar berita, pencarian, filter kategori, pagination, halaman detail |
| Galeri (`/galeri`) | Grid foto dengan filter kategori |
| Kontak (`/kontak`) | Alamat, telepon, WhatsApp, email, media sosial, peta Google Maps |

### Admin dashboard

* Login username + password dengan **session Flask** dan password **hash**.
* Dashboard: jumlah berita, pengumuman, galeri, data profil, dan aktivitas terbaru.
* CRUD lengkap: **Berita**, **Pengumuman**, **Galeri**.
* Form ubah: **Profil Sekolah** (sambutan, sejarah, visi, misi, foto) dan
  **Identitas Sekolah** (alamat, kontak, statistik, peta, media sosial).
* **Akun Admin**: ganti username dan password.
* Tabel data, pencarian, filter, pagination, modal konfirmasi hapus, flash message.

> Fitur **Prestasi**, **Fasilitas**, dan **Program/Akademik** sengaja belum
> dikerjakan di versi 1. Schema tabelnya sudah disediakan dalam bentuk
> komentar di bagian akhir `database.sql`.

### Preview statis (opsional)

Folder `public/school-demo/` berisi hasil *render* seluruh halaman dari template
ini memakai data contoh, sehingga tampilan bisa dilihat tanpa MySQL:

```
public/school-demo/daftar-halaman.html   <- daftar semua halaman preview
public/school-demo/index.html            <- beranda
public/school-demo/admin-dashboard.html  <- dashboard admin
```

Preview ini cukup dibuka langsung di browser. Untuk membuat ulang preview
setelah template diubah, jalankan:

```bash
python _buat_demo.py
```

Folder preview boleh dihapus tanpa memengaruhi aplikasi.

---

## 2. Kebutuhan Sistem

* Windows 10/11 + [XAMPP](https://www.apachefriends.org/) (Apache + MySQL/MariaDB)
* Python 3.9 atau lebih baru ([unduh Python](https://www.python.org/downloads/))
* VS Code + ekstensi **Python** (opsional, tapi disarankan)

---

## 3. Instalasi (langkah demi langkah)

### Langkah 1 &#8212; Nyalakan XAMPP

1. Buka **XAMPP Control Panel**.
2. Klik **Start** pada modul **Apache**.
3. Klik **Start** pada modul **MySQL**.
4. Pastikan keduanya berwarna hijau.

### Langkah 2 &#8212; Buat virtual environment

Buka VS Code, aktifkan terminal (`Ctrl + `), lalu pindah ke folder project:

```bash
cd school-profile

python -m venv venv
venv\Scripts\activate
```

### Langkah 3 &#8212; Install dependency

```bash
pip install -r requirements.txt
```

Isi `requirements.txt`:

```
Flask==3.0.3
mysql-connector-python==9.0.0
```

### Langkah 4 &#8211; Import database

1. Buka browser ke **http://localhost/phpmyadmin**
2. Klik tab **Import** di menu atas.
3. Pilih file **`database.sql`** dari folder project.
4. Klik **Go / Kirim**.

Database `sekolah_profile` beserta tabel dan data contoh akan dibuat otomatis.
Cek tabel yang sudah ada: `users`, `sekolah`, `berita`, `pengumuman`, `galeri`.

### Langkah 5 &#8212; Konfigurasi database

Buka file **`config.py`**. Nilai bawaan sudah cocok dengan XAMPP standar:

```python
DB_HOST     = "127.0.0.1"
DB_PORT     = 3306
DB_USER     = "root"
DB_PASSWORD = ""          # XAMPP: password root kosong
DB_NAME     = "sekolah_profile"
```

Ubah hanya bila Setting MySQL Anda berbeda. Nilai ini juga bisa diisi lewat
environment variable (`DB_USER`, `DB_PASSWORD`, `DB_NAME`, dan lainnya).

### Langkah 6 &#8212; Jalankan aplikasi

```bash
python app.py
```

### Langkah 7 &#8212; Buka di browser

* Website publik: **http://127.0.0.1:5000**
* Login admin: **http://127.0.0.1:5000/admin/login**

### Langkah 8 &#8212; Login admin

| Username | Password |
| --- | --- |
| `admin` | `admin123` |
| `guru` | `guru123` |
| `staf` | `staf123` |

> Ganti password setelah login lewat menu **Akun Admin**.

---

## 4. Struktur Folder

```
school-profile/
│
├── app.py                # entry point: membuat aplikasi & mendaftarkan blueprint
├── config.py             # konfigurasi database, upload, session
├── database.sql          # CREATE DATABASE, CREATE TABLE, data awal
├── db.py                 # koneksi database + fungsi query (fetch_one, execute, ...)
├── utils.py              # upload gambar, format tanggal, pembersih teks
├── requirements.txt      # daftar paket pip
├── README.md
│
├── routes/
│   ├── __init__.py
│   ├── public.py         # halaman untuk pengunjung (tanpa login)
│   ├── auth.py           # login, logout, session admin
│   └── admin.py          # dashboard + CRUD (butuh login)
│
├── templates/
│   ├── public/           # base, beranda, profil, berita, detail, galeri, kontak, 404
│   ├── auth/             # halaman login
│   └── admin/            # base admin, dashboard, tabel, form
│
└── static/
    ├── css/style.css     # seluruh tampilan (tema light terminal)
    ├── js/main.js        # menu mobile, modal konfirmasi, preview file
    ├── images/           # gambar contoh (SVG)
    └── uploads/          # hasil upload admin (dibuat otomatis)
```

Penjelasan singkat tiap folder:

* **`routes/`** &#8212; semua alamat URL dan semua proses yang membaca atau
  menyimpan data ke database. Dipisah tiga bagian agar mudah dibaca saat
  presentasi.
* **`templates/`** &#8212; kerangka HTML. Folder `public` untuk pengunjung,
  `admin` untuk dashboard, `auth` untuk login.
* **`static/`** &#8212; berkas yang dikirim apa adanya ke browser. CSS satu file,
  JS satu file, gambar contoh, dan folder upload.
* **`db.py`** &#8212; satu koneksi database per request, ditutup otomatis.

---

## 5. Daftar Route Utama

### Publik

| Method | URL | Fungsi |
| --- | --- | --- |
| GET | `/` | Beranda |
| GET | `/profil` | Profil sekolah |
| GET | `/berita` | Daftar berita (+ `?q=`, `?kategori=`, `?halaman=`) |
| GET | `/berita/<id>` | Detail berita |
| GET | `/galeri` | Galeri foto (+ `?kategori=`) |
| GET | `/kontak` | Kontak |

### Autentikasi

| Method | URL | Fungsi |
| --- | --- | --- |
| GET/POST | `/admin/login` | Halaman login admin |
| GET | `/admin/logout` | Keluar dari dashboard |

### Admin (butuh login)

| Method | URL | Fungsi |
| --- | --- | --- |
| GET | `/admin/` | Dashboard |
| GET/POST | `/admin/profil-sekolah` | Ubah profil, sambutan, sejarah, visi, misi, foto |
| GET/POST | `/admin/identitas-sekolah` | Ubah alamat, kontak, statistik, peta |
| GET | `/admin/berita` | Tabel berita (+ pencarian, filter, pagination) |
| GET/POST | `/admin/berita/tambah` | Tambah berita |
| GET/POST | `/admin/berita/<id>/ubah` | Ubah berita |
| POST | `/admin/berita/<id>/hapus` | Hapus berita |
| GET | `/admin/pengumuman` | Tabel pengumuman |
| GET/POST | `/admin/pengumuman/tambah` | Tambah pengumuman |
| GET/POST | `/admin/pengumuman/<id>/ubah` | Ubah pengumuman |
| POST | `/admin/pengumuman/<id>/hapus` | Hapus pengumuman |
| GET | `/admin/galeri` | Tabel galeri |
| GET/POST | `/admin/galeri/tambah` | Unggah foto |
| GET/POST | `/admin/galeri/<id>/ubah` | Ubah foto |
| POST | `/admin/galeri/<id>/hapus` | Hapus foto |
| GET/POST | `/admin/akun` | Ganti username & password |

Halaman yang tidak ada akan menampilkan **404** (template `public/404.html`).

---

## 6. Struktur Database

```
sekolah_profile
├── users             : akun admin (username, password hash, nama, role)
├── sekolah           : profil, identitas, kontak, statistik (1 baris, id = 1)
├── berita            : judul, kategori, ringkasan, isi, thumbnail, tanggal, status
├── pengumuman        : judul, isi, tanggal mulai/selesai, aktif
└── galeri            : judul, kategori, keterangan, foto, tanggal
```

Relasi: tabel `users` berdiri sendiri, tabel `berita`/`pengumuman`/`galeri`
juga berdiri sendiri, sedangkan `sekolah` dipakai bersama oleh seluruh halaman
publik sebagai sumber data profil, identitas, dan statistik.

---

## 7. Keamanan yang Diterapkan

* Password **tidak** disimpan sebagai teks biasa &#8212; memakai
  `werkzeug.security.generate_password_hash` / `check_password_hash`.
* **Session login**: admin yang belum login diarahkan ke `/admin/login`
  (diatur pada `routes/admin.py` fungsi `_harus_login`).
* Route hapus memakai **POST** + modal konfirmasi, bukan link GET.
* Validasi input: field wajib diperiksa, teks dibersihkan dan dipotong panjangnya.
* Validasi upload: hanya `jpg`, `jpeg`, `png`, `webp`, maksimal 5 MB.
* Nama file dibersihkan dengan `secure_filename` lalu diberi kode acak
  (`uuid4().hex[:8]`) agar tidak menimpa file lain.
* Database hanya menyimpan **nama file**, bukan gambar.
* `SECRET_KEY` di `config.py` harus diganti bila dipakai di server publik.

---

## 8. Cara Kerja Data (contoh alur)

```
Admin buka /admin/berita/tambah
        ↓  isi form + unggah thumbnail
POST /admin/berita/tambah  →  file disimpan ke static/uploads/
        ↓  INSERT ke tabel berita (hanya nama file)
Pengunjung buka /berita
        ↓  SELECT dari tabel berita
Berita baru tampil di website publik
```

Jadi begitu admin menyimpan data, halaman publik langsung berubah
(tanpa perlu mengedit kode atau me-restart server).

---

## 9. Masalah yang Sering Muncul

| Gejala | Penyebab & solusi |
| --- | --- |
| `Can't connect to MySQL server` | MySQL di XAMPP belum Start, atau port bukan 3306. Ubah `DB_PORT` di `config.py`. |
| `Unknown database 'sekolah_profile'` | `database.sql` belum di-import di phpMyAdmin. |
| `Access denied for user 'root'` | Password MySQL berbeda. Isi `DB_PASSWORD` di `config.py`. |
| Teks Indonesia berantakan (Ã©) | Gunakan `utf8mb4` saat import (sudah diatur di `database.sql`). |
| Foto tidak tampil | Format bukan jpg/jpeg/png/webp atau ukuran lebih dari 5 MB. |
| `Address already in use` | Port 5000 dipakai aplikasi lain. Jalankan `flask run --port 5001`. |

---

## 10. Ide Pengembangan (versi 2)

* Tambah modul **Prestasi**, **Fasilitas**, dan **Program/Akademik** (schema sudah
  disiapkan di `database.sql`).
* Multi-user: guru boleh menambah berita, admin yang menerbitkan.
* Ekspor daftar siswa ke Excel / PDF.
* Pagination dan filter tambahan pada dashboard.
