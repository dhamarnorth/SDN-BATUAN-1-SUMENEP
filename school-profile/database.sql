-- =====================================================================
--  DATABASE : sekolah_profile
--  APLIKASI : Website Profil Sekolah + Admin Dashboard (CMS)
--  SERVER   : MySQL / MariaDB (XAMPP)
--
--  CARA PAKAI:
--  1. Buka phpMyAdmin  ->  http://localhost/phpmyadmin
--  2. Klik menu "Import" (atau tab "SQL")
--  3. Pilih file ini  ->  Klik "Go"
--
--  Akun admin yang dibuat otomatis:
--     admin / admin123      guru / guru123      staf / staf123
--  Password disimpan sebagai hash, bukan teks biasa.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS sekolah_profile
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE sekolah_profile;

-- ---------------------------------------------------------------------
-- TABEL 1 : users (akun admin dashboard)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id          INT(11) NOT NULL AUTO_INCREMENT,
  username    VARCHAR(50) NOT NULL,
  password    VARCHAR(255) NOT NULL COMMENT 'hash password (pbkdf2)',
  nama        VARCHAR(100) NOT NULL,
  role        ENUM('admin','editor') NOT NULL DEFAULT 'admin',
  dibuat_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- TABEL 2 : sekolah (profil, identitas, kontak, statistik)
-- Satu baris data saja (id = 1), كلها diedit dari dashboard.
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS sekolah;
CREATE TABLE sekolah (
  id              TINYINT(3) NOT NULL,
  nama_sekolah    VARCHAR(150) NOT NULL,
  npsn            VARCHAR(20)  DEFAULT NULL,
  nss             VARCHAR(20)  DEFAULT NULL,
  jenjang         VARCHAR(30)  DEFAULT 'SD',
  tahun_berdiri   SMALLINT     DEFAULT NULL,
  kepala_sekolah  VARCHAR(100) DEFAULT NULL,
  nip_kepsek      VARCHAR(30)  DEFAULT NULL,
  slogan          VARCHAR(200) DEFAULT NULL,
  ringkasan       TEXT         DEFAULT NULL,
  sambutan        TEXT         DEFAULT NULL,
  sejarah         TEXT         DEFAULT NULL,
  visi            TEXT         DEFAULT NULL,
  misi            TEXT         DEFAULT NULL,
  foto            VARCHAR(255) DEFAULT NULL,
  alamat          VARCHAR(500) DEFAULT NULL,
  desa            VARCHAR(100) DEFAULT NULL,
  kecamatan        VARCHAR(100) DEFAULT NULL,
  kabupaten       VARCHAR(100) DEFAULT NULL,
  provinsi        VARCHAR(100) DEFAULT NULL,
  kode_pos        VARCHAR(10)  DEFAULT NULL,
  telepon         VARCHAR(30)  DEFAULT NULL,
  whatsapp        VARCHAR(30)  DEFAULT NULL,
  email           VARCHAR(100) DEFAULT NULL,
  website         VARCHAR(100) DEFAULT NULL,
  maps_embed      TEXT         DEFAULT NULL,
  facebook        VARCHAR(200) DEFAULT NULL,
  instagram       VARCHAR(200) DEFAULT NULL,
  youtube         VARCHAR(200) DEFAULT NULL,
  jam_operasional VARCHAR(200) DEFAULT NULL,
  jumlah_siswa    SMALLINT     DEFAULT 0,
  jumlah_guru     SMALLINT     DEFAULT 0,
  jumlah_kelas    SMALLINT     DEFAULT 0,
  jumlah_prestasi SMALLINT     DEFAULT 0,
  jumlah_ekskul   SMALLINT     DEFAULT 0,
  dibuat_pada     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  diperbarui_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- TABEL 3 : berita
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS berita;
CREATE TABLE berita (
  id              INT(11) NOT NULL AUTO_INCREMENT,
  judul           VARCHAR(200) NOT NULL,
  kategori        VARCHAR(50)  DEFAULT 'Umum',
  ringkasan       VARCHAR(500) DEFAULT NULL,
  isi             TEXT         NOT NULL,
  thumbnail       VARCHAR(255) DEFAULT NULL,
  tanggal         DATE         DEFAULT NULL,
  penulis         VARCHAR(100) DEFAULT NULL,
  status          ENUM('draft','published') NOT NULL DEFAULT 'published',
  dibuat_pada     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  diperbarui_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_kategori (kategori),
  KEY idx_tanggal (tanggal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- TABEL 4 : pengumuman (tampil di beranda)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS pengumuman;
CREATE TABLE pengumuman (
  id              INT(11) NOT NULL AUTO_INCREMENT,
  judul           VARCHAR(200) NOT NULL,
  isi             TEXT         NOT NULL,
  tanggal_mulai   DATE         DEFAULT NULL,
  tanggal_selesai DATE         DEFAULT NULL,
  aktif           TINYINT(1)   NOT NULL DEFAULT 1,
  dibuat_pada     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  diperbarui_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- TABEL 5 : galeri
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS galeri;
CREATE TABLE galeri (
  id              INT(11) NOT NULL AUTO_INCREMENT,
  judul           VARCHAR(150) NOT NULL,
  kategori        VARCHAR(50)  NOT NULL DEFAULT 'Kegiatan Sekolah',
  keterangan      VARCHAR(500) DEFAULT NULL,
  foto            VARCHAR(255) NOT NULL,
  tanggal         DATE         DEFAULT NULL,
  dibuat_pada     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  diperbarui_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_kategori (kategori)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================================
--  DATA AWAL
--  (seluruh data di bawah dapat diganti dari dashboard admin)
-- =====================================================================

-- 1) Akun admin
INSERT INTO users (username, password, nama, role) VALUES
('admin', 'pbkdf2:sha256:600000$gz5n2YX48mk$ac114614b54df77265e2e743f51ffcc8e4219358f5cd4c608be44cbb456adb42', 'Administrator Sekolah', 'admin'),
('guru',  'pbkdf2:sha256:600000$DCgcBvo4s44$cf37a341fad6fb1332388fa5292efd0fb7ee237a4a66f5f030f3b12290d9cb9d',  'Guru Placeholder', 'editor'),
('staf',  'pbkdf2:sha256:600000$61cmcfCvFXg$2c7546474216bf9093ee6dae888a08876d700de2865208e276c3d72fa721c81e', 'Staf Placeholder', 'editor');

-- 2) Profil, identitas, kontak, dan statistik sekolah
INSERT INTO sekolah (
  id, nama_sekolah, npsn, nss, jenjang, tahun_berdiri, kepala_sekolah, nip_kepsek,
  slogan, ringkasan, sambutan, sejarah, visi, misi, foto,
  alamat, desa, kecamatan, kabupaten, provinsi, kode_pos,
  telepon, whatsapp, email, website, maps_embed,
  facebook, instagram, youtube, jam_operasional,
  jumlah_siswa, jumlah_guru, jumlah_kelas, jumlah_prestasi, jumlah_ekskul
) VALUES (
  1,
  'SDN BATUAN 1 SUMENEP',
  '20531889',
  '10.02.05.0123456',
  'SD',
  1986,
  'Bapak Ahmad Fauzi, S.Pd. (Placeholder)',
  '196805121994031005',
  'Tumbuh, Berpikir, Berprestasi',
  'SDN Batuan 1 adalah sekolah dasar negeri di Kecamatan Batuan, Kabupaten Sumenep, Jawa Timur. Kami menyiapkan generasi yang cinta belajar, berkarakter, dan berani berkarya.',
  'Assalamualaikum warahmatullahi wabarakatub. Segala puji bagi Tuhan Yang Maha Esa. Kami berterima kasih kepada seluruh warga sekolah yang terus bekerja sama. Dashboard sekolah ini dibuat sederhana agar mudah dikelola staf sekolah. Kami berharap SDN Batuan 1 menjadi rumah belajar yang nyaman dan menyenangkan bagi setiap anak. Wassalamualaikum warahmatullahi wabarakatub.',
  'SDN Batuan 1 berdiri pada tahun 1986 di tengah Desa Batuan, Kecamatan Batuan, Kabupaten Sumenep. Berawal dari satu bangunan sederhana, sekolah terus berkembang bersama warga desa. Ruang kelas diperluas, laboratorium ditambahkan, dan kegiatan ekstrakurikuler makin beragam. Hari ini sekolah melayani enam rombongan belajar dengan lingkungan yang asuh dan nyaman.',
  'Terwujudnya peserta didik yang beriman, bertakwa, berprestasi, serta berbudaya cinta tanah air.',
  '1. Menyelenggarakan pembelajaran yang aktif, kreatif, efektif, dan menyenangkan.
2. Menanamkan ketakwaan dan akhlak mulia dalam setiap kegiatan sekolah.
3. Mengembangkan bakat dan minat siswa melalui kegiatan ekstrakurikuler.
4. Membangun lingkungan sekolah yang bersih, nyaman, dan ramah anak.
5. Menjalin kerja sama yang baik dengan orang tua dan masyarakat.',
  'profil.svg',
  'Dusun Sambil, Desa Batuan',
  'Batuan',
  'Batuan',
  'Sumenep',
  'Jawa Timur',
  '62211',
  '(0328) 000-0000',
  '0800 0000 0000',
  'info@sdbatuan1.example.sch.id',
  'https://sdbatuan1.example.sch.id',
  '',
  'https://facebook.com/sdbatuan1',
  'https://instagram.com/sdbatuan1',
  'https://youtube.com/@sdbatuan1',
  'Senin - Jumat, 07.00 - 13.30 WIB',
  248, 18, 6, 27, 7
);

-- 3) Berita dummy
INSERT INTO berita (judul, kategori, ringkasan, isi, thumbnail, tanggal, penulis, status) VALUES
('Kegiatan Muatan Lokal Batuan', 'Akademik',
 'Siswa kelas IV belajar mengenal lingkungan sekitar melalui pembelajaran tematik bersama guru kelas.',
 'Pagi yang cerah, siswa kelas IV mengikuti pembelajaran tematik bersama guru kelas. Materi yang dibahas adalah mengenal lingkungan sekitar, mulai dari nama tumbuhan sampai kebiasaan gotong royong di desa.

Guru menggunakan benda nyata seperti daun dan batu agar siswa lebih mudah memahami.

Kegiatan ini dilakukan setiap Selasa dan Kamis di ruang kelas 4A. Orang tua siswa juga dilibatkan agar anak mendapat pengalaman tentang kehidupan desa.

Kegiatan muatan lokal akan terus dilanjutkan pada tahun ajaran berikutnya.',
 'pembelajaran.svg', '2024-08-12', 'Guru Kelas 4A', 'published'),

('Perpustakaan Sekolah Ditata Ulang', 'Fasilitas',
 'Rak buku dipindah agar lebih rapi, pencahayaan diperbaiki, dan koleksi buku anak bertambah.',
 'Ruang baca SDN Batuan 1 selesai ditata ulang. Rak buku dipindah agar lebih rapi dan mudah dijangkau anak. Pencahayaan dan ventilasi diperbaiki sehingga ruang baca terang dan nyaman dipakai pada jam istirahat.

Koleksi buku cerita anak bertambah dari 120 buku menjadi 185 buku. Siswa dapat meminjam maksimal dua buku selama satu minggu.

Setiap hari Jumat dijadwalkan jam membaca bersama di perpustakaan. Semua siswa wajib hadir dan membawa buku baca.',
 'fasilitas.svg', '2024-07-28', 'Tim Perpustakaan', 'published'),

('Jumat Bersih dan Literasi', 'Kegiatan Sekolah',
 'Siswa bersama guru membersihkan sekolah dan membaca bersama di perpustakaan.',
 'Setiap Jumat warga sekolah melakukan kerja bakti membersihkan kelas, taman, dan toilet. Setelah selesai, siswa membaca bersama di perpustakaan.

Kegiatan ini melatih kebiasaan kebersihan dan kegigihan membaca.',
 'kegiatan.svg', '2024-07-19', 'Wali Kelas 5B', 'published'),

('Pelatihan Pembelajaran Daring untuk Guru', 'Akademik',
 'Guru mengikuti pelatihan membuat materi ajar sederhana yang mudah diakses siswa dari rumah.',
 'Pelatihan membahas cara membuat materi ajar sederhana yang bisa diakses siswa dari rumah.

Setiap guru membuat satu paket materi sederhana sebagai tugas akhir pelatihan.',
 'pembelajaran.svg', '2024-06-25', 'Tata Usaha', 'published');

-- 4) Pengumuman
INSERT INTO pengumuman (judul, isi, tanggal_mulai, tanggal_selesai, aktif) VALUES
('PPDB Tahun Ajaran 2025/2026 Telah Dibuka',
 'Pendaftaran peserta didik baru dibuka mulai 1 Juni sampai 15 Juli. Berkas dikumpulkan ke Tata Usaha pada jam kerja.',
 '2024-06-01', '2024-07-15', 1),
('Rapat Orang Tua Murid',
 'Rapat orang tua siswa kelas I sampai VI dilaksanakan di ruang kelas masing-masing. Kehadiran orang tua sangat kami harapkan.',
 '2024-05-20', '2024-05-20', 0),
('Pendaftaran Ekstrakurikuler',
 'Pendaftaran kegiatan ekstrakurikuler dibuka untuk semua siswa. Pendaftaran dilakukan setelah pulang belajar.',
 '2024-08-01', '2024-08-31', 1);

-- 5) Galeri dummy
INSERT INTO galeri (judul, kategori, keterangan, foto, tanggal) VALUES
('Upacara Bendera Hari Senin', 'Acara', 'Pembukaan kegiatan belajar dengan upacara bendera.', 'acara.svg', '2024-08-12'),
('Belajar di Luar Kelas', 'Pembelajaran', 'Pembelajaran tematik di lingkungan desa.', 'pembelajaran.svg', '2024-08-08'),
('Latihan Pramuka', 'Ekstrakurikuler', 'Latihan rutin kepanduan setiap Sabtu pagi.', 'ekstrakurikuler.svg', '2024-08-05'),
('Gedung Sekolah SDN Batuan 1', 'Fasilitas', 'Tampak depan gedung sekolah.', 'profil.svg', '2024-07-30'),
('Siswa Peraih Penghargaan', 'Prestasi', 'Siswa kelas V menerima penghargaan lomba.', 'prestasi.svg', '2024-07-22'),
('Kerja Bakti Jumat', 'Kegiatan Sekolah', 'Membersihkan kelas, taman, dan toilet sekolah.', 'kegiatan.svg', '2024-07-15');

-- ---------------------------------------------------------------------
-- CATATAN VERSI 2
-- Tabel berikut belum dipakai di versi 1. Hapus tanda -- (--) bila
-- sudah dikerjakan fitur prestasi, fasilitas, dan program akademik.
-- ---------------------------------------------------------------------
-- CREATE TABLE prestasi (
--   id INT(11) NOT NULL AUTO_INCREMENT,
--   nama_prestasi VARCHAR(150) NOT NULL,
--   tingkat VARCHAR(50),
--   tahun SMALLINT,
--   penerima VARCHAR(150),
--   foto VARCHAR(255),
--   dibuat_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   PRIMARY KEY (id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
--
-- CREATE TABLE fasilitas (
--   id INT(11) NOT NULL AUTO_INCREMENT,
--   nama VARCHAR(100) NOT NULL,
--   deskripsi TEXT,
--   foto VARCHAR(255),
--   dibuat_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   PRIMARY KEY (id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
--
-- CREATE TABLE program_akademik (
--   id INT(11) NOT NULL AUTO_INCREMENT,
--   nama VARCHAR(100) NOT NULL,
--   kategori VARCHAR(50),
--   deskripsi TEXT,
--   dibuat_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   PRIMARY KEY (id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
