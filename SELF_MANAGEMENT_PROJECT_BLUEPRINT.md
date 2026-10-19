# Self-Management — Project Blueprint

> **Jenis aplikasi:** Desktop productivity app  
> **Bahasa:** Python  
> **Platform target awal:** Windows  
> **Status dokumen:** Rancangan awal / project specification  
> **Prinsip desain:** Satu aplikasi, tiga modul utama, data lokal, dashboard berbasis panel.

---

## 1. Ringkasan Project

**Self-Management** adalah aplikasi desktop untuk membantu pengguna mengelola tiga area kehidupan sehari-hari:

1. **Study** — catatan pembelajaran, file dan folder, tugas, waktu belajar, serta playlist.
2. **Exercise** — jadwal dan riwayat olahraga, durasi latihan, checklist kebiasaan, serta estimasi kalori.
3. **Finance** — pemasukan, pengeluaran, anggaran bulanan, saldo bersih, dan target keuangan.

Ketiga modul menggunakan pola dashboard yang konsisten, tetapi isi panel menyesuaikan kebutuhan modul. Aplikasi sebaiknya tetap bermanfaat meskipun fitur integrasi eksternal seperti Spotify belum tersedia.

### Tujuan

- Menyatukan beberapa kebutuhan self-management dalam satu aplikasi desktop.
- Menyimpan data pengguna secara lokal dan mudah dicadangkan.
- Membuat informasi penting terlihat sekilas tanpa memenuhi layar dengan terlalu banyak elemen.
- Mengutamakan fungsi dasar yang stabil sebelum menambahkan fitur kompleks.

### Bukan tujuan versi awal

- Menggantikan aplikasi kesehatan profesional atau memberikan diagnosis medis.
- Menyambungkan rekening bank secara otomatis.
- Menyalin semua fitur Obsidian atau Spotify.
- Memerlukan akun cloud untuk dapat digunakan.

---

## 2. Prinsip UI dan Layout

Gambar referensi menggunakan dashboard dengan enam area bernomor. Nomor pada gambar menjadi acuan panel berikut:

| Area | Warna referensi | Study | Exercise | Finance |
|---|---|---|---|---|
| 1 | Hitam | Header, navigasi modul, judul halaman | Sama | Sama |
| 2 | Kuning | File/folder explorer | Kalender olahraga bulanan | Ringkasan bulan, filter periode, atau kalender transaksi |
| 3 | Cyan | Editor dan preview catatan | Pilihan jenis latihan dan sesi aktif | Ringkasan pemasukan, pengeluaran, dan saldo |
| 4 | Merah | To-do list/tugas | Kalender agenda dan rencana latihan | Target bulanan dan daftar target |
| 5 | Ungu | Pomodoro timer | Ringkasan aktivitas hari ini atau stopwatch | Jam saat ini dan ringkasan singkat |
| 6 | Hijau | Playlist / musik belajar | Playlist olahraga | Grafik atau ringkasan anggaran |

### Perilaku panel

- Panel 1 menjadi header utama dan tetap terlihat.
- Panel 2 dan 4 dapat dibuka/tutup karena berisi panel pendukung.
- Panel 3 menjadi area utama dan mendapatkan ruang terbesar.
- Panel 5 berukuran relatif tetap agar kontrol kecil mudah ditemukan.
- Panel 6 berada di bagian bawah dan dapat dibuat lebih pendek atau diperluas.
- Gunakan `QSplitter` untuk panel yang ukuran lebarnya perlu diubah oleh pengguna.
- Gunakan `QDockWidget` atau panel kustom dengan tombol collapse untuk panel yang dapat dibuka/tutup.
- Simpan preferensi ukuran dan visibilitas panel agar pulih setelah aplikasi dibuka kembali.
- Warna pada gambar adalah petunjuk pembagian area, bukan keharusan warna final. Sediakan tema gelap dan terang jika memungkinkan.

### Rekomendasi proporsi awal

Proporsi ini hanya titik awal dan perlu diuji di layar nyata:

- Header: sekitar 6–8% tinggi jendela.
- Panel kiri: sekitar 22–25% lebar area konten.
- Panel utama: sekitar 55–60% lebar area konten.
- Panel kanan: sekitar 20–23% lebar area konten.
- Panel bawah: sekitar 22–28% tinggi area konten.

Layout harus responsif terhadap ukuran jendela. Jangan mengunci semua panel pada ukuran absolut yang membuat aplikasi sulit digunakan pada layar kecil.

---

## 3. Navigasi Aplikasi

Navigasi utama:

- **Study**
- **Exercise**
- **Finance**
- **Settings**

Pilih salah satu dari dua pendekatan berikut:

1. **Rekomendasi awal — satu jendela dengan halaman modul:** navigasi utama mengganti konten halaman, sedangkan header dan gaya visual tetap konsisten.
2. **Satu jendela terpisah per modul:** dapat dipertimbangkan nanti jika kebutuhan tiap modul menjadi sangat kompleks.

Untuk versi pertama, gunakan satu jendela utama dengan halaman modul. Ini lebih mudah dirawat dan tidak membuat terlalu banyak jendela.

---

# 4. Modul Study

## 4.1 Tujuan

Study adalah area manajemen pembelajaran yang terinspirasi oleh alur kerja aplikasi catatan seperti Obsidian. Pengguna dapat mengatur file dan folder, membuat catatan Markdown, mengedit teks, melihat preview, serta mengelola tugas belajar.

## 4.2 Panel dashboard

### Area 1 — Header

- Nama modul: Study.
- Tombol navigasi ke Study, Exercise, dan Finance.
- Tombol membuat catatan baru.
- Pencarian catatan.
- Indikator status penyimpanan, misalnya `Saved` atau `Unsaved`.
- Tombol Settings.

### Area 2 — File & Folder Explorer (kuning)

Fungsi:

- Menampilkan folder dan file Markdown.
- Membuat, mengganti nama, memindahkan, dan menghapus file/folder.
- Membuka file Markdown pada editor.
- Mencari file berdasarkan nama.
- Menandai catatan sebagai favorit/pin.
- Memilih folder kerja utama atau *notes vault*.
- Menampilkan konfirmasi sebelum menghapus file.

Aturan penting:

- Catatan disimpan sebagai file `.md` biasa, bukan hanya sebagai data di database.
- Gunakan `pathlib` untuk mengelola path.
- Batasi operasi file ke folder kerja yang dipilih pengguna agar operasi tidak sengaja menyentuh file di luar vault.
- Untuk penghapusan, gunakan konfirmasi dan pertimbangkan Trash/soft delete.
- Jangan menimpa file jika nama tujuan sudah digunakan tanpa memberi pilihan kepada pengguna.

### Area 3 — Markdown Editor & Preview (cyan)

Fungsi:

- Membuat dan mengedit catatan Markdown.
- Preview hasil render Markdown.
- Tombol atau shortcut untuk **bold**, *italic*, heading, link, list, checklist, blockquote, dan code block.
- Pengaturan alignment dan ukuran font untuk **tampilan editor**.
- Simpan manual dan autosave.
- Indikator perubahan yang belum tersimpan.
- Pencarian teks di dalam catatan.
- Dukungan gambar dan tautan relatif jika memungkinkan.

**Catatan teknis:** Markdown standar tidak menyimpan semua format seperti ukuran font, alignment, atau warna teks secara konsisten. Karena itu:
- Simpan isi catatan dalam Markdown standar agar mudah dipindahkan ke aplikasi lain.
- Ukuran font editor sebaiknya menjadi preferensi tampilan, bukan format isi catatan.
- Jika alignment atau styling per bagian benar-benar dibutuhkan, tentukan ekstensi Markdown yang didukung dan dokumentasikan batas kompatibilitasnya.
- Preview HTML harus disanitasi sebelum dirender jika ada kemungkinan konten yang tidak tepercaya.

### Area 4 — To-do List (merah, dapat dibuka/tutup)

Fungsi:

- Menambah, mengedit, menyelesaikan, dan menghapus tugas.
- Judul, catatan opsional, prioritas, tenggat, dan status.
- Filter: hari ini, mendatang, selesai, dan semua.
- Tautkan tugas ke file catatan terkait.
- Tandai tugas selesai dengan satu klik.
- Tampilkan tugas yang jatuh tempo atau terlambat.

Untuk MVP, simpan data tugas di SQLite. Sinkronisasi otomatis dua arah antara checklist di Markdown dan daftar tugas database dapat ditunda karena menambah kompleksitas.

### Area 5 — Pomodoro Timer (ungu)

Fungsi:

- Mode fokus dan istirahat.
- Durasi yang bisa diatur, misalnya 25 menit fokus dan 5 menit istirahat.
- Tombol Start, Pause, Resume, dan Reset.
- Penghitung sesi fokus.
- Pilihan mengaitkan sesi dengan catatan atau tugas.
- Notifikasi saat sesi berakhir.

Timer tidak boleh bergantung pada jumlah pemanggilan callback saja. Simpan waktu akhir sesi dan hitung sisa waktu berdasarkan jam sistem agar lebih tahan terhadap jeda UI.

### Area 6 — Playlist / Music (hijau)

Pilihan implementasi:

1. **MVP:** daftar tautan playlist Spotify, YouTube, atau sumber musik lain yang dibuka di browser.
2. **Tahap lanjutan:** pemutaran lokal dari file audio milik pengguna.
3. **Tahap lanjutan:** integrasi Spotify resmi jika API, OAuth, ketentuan layanan, dan dukungan playback memungkinkan.

Jangan mengasumsikan aplikasi dapat mengendalikan semua fungsi Spotify hanya dengan menempelkan URL. Integrasi playback dan kontrol akun membutuhkan mekanisme resmi dan mungkin memiliki batasan.

## 4.3 Fitur lanjutan Study

- Tag dan pencarian isi catatan.
- Backlinks dan daftar catatan terkait.
- Template catatan.
- Riwayat versi atau backup sebelum perubahan besar.
- Ekspor catatan atau folder.
- Statistik waktu belajar.
- Shortcut keyboard yang bisa dikonfigurasi.

## 4.4 Kriteria selesai Study

- Pengguna bisa membuat folder dan file Markdown.
- Catatan dapat ditutup dan dibuka kembali tanpa kehilangan isi.
- Preview sesuai dengan Markdown yang didukung.
- Perubahan yang belum disimpan terlihat jelas.
- Timer dapat dijeda dan dilanjutkan.
- Tugas tetap ada setelah aplikasi ditutup dan dibuka lagi.

---

# 5. Modul Exercise

## 5.1 Tujuan

Exercise membantu pengguna merencanakan dan mencatat aktivitas fisik, melihat konsistensi latihan, serta memahami durasi dan perkiraan energi yang digunakan. Informasi kalori harus dianggap estimasi, bukan pengukuran medis yang pasti.

## 5.2 Panel dashboard

### Area 1 — Header

- Nama modul: Exercise.
- Tanggal hari ini.
- Ringkasan latihan hari ini.
- Navigasi modul dan Settings.

### Area 2 — Kalender Olahraga Bulanan (kuning, ukuran relatif tetap)

Fungsi:

- Kalender satu bulan.
- Setiap tanggal memiliki status: belum dicatat, selesai, istirahat terencana, atau terlewat.
- Hari dengan latihan selesai diberi penanda warna.
- Klik tanggal untuk melihat latihan dan durasi pada tanggal tersebut.
- Tombol pindah bulan dan kembali ke hari ini.
- Target frekuensi latihan mingguan.

Aturan:

- Warna hijau hanya berarti aktivitas dicatat selesai, bukan jaminan kondisi tubuh sehat.
- Hari istirahat tidak dihitung sebagai kegagalan.
- Pengguna dapat memperbaiki catatan jika salah menandai hari.
- Tanggal dan waktu mengikuti zona waktu lokal perangkat.

### Area 3 — Workout Planner & Active Session (cyan)

Fungsi:

- Memilih kategori: kardio, kekuatan, mobilitas/stretching, olahraga tim, atau aktivitas lain.
- Membuat rencana latihan dengan nama, durasi target, dan catatan.
- Memulai sesi latihan.
- Menampilkan timer sesi aktif.
- Tombol Start, Pause, Resume, Finish, dan Cancel.
- Menyimpan durasi aktual dan durasi target.
- Input intensitas opsional dan catatan setelah latihan.
- Riwayat sesi yang dapat diedit.

Contoh aktivitas:

- Berjalan kaki.
- Berlari.
- Bersepeda.
- Latihan kekuatan.
- Peregangan.
- Olahraga pilihan pengguna.

Jangan memaksakan target olahraga harian yang sama untuk semua orang. Target harus bisa disesuaikan dan mendukung hari istirahat.

### Area 4 — Calendar Manager / Workout Plan (merah, dapat dibuka/tutup)

Fungsi:

- Agenda latihan yang akan datang.
- Menjadwalkan jenis latihan pada tanggal tertentu.
- Mengubah atau membatalkan rencana.
- Pengingat opsional.
- Melihat rencana hari ini dan rencana yang akan datang.
- Membedakan jadwal yang direncanakan dengan aktivitas yang benar-benar selesai.

Panel ini lebih tepat menjadi **Workout Planner / Agenda** daripada kalender umum, agar tidak tumpang tindih dengan kalender bulanan di area 2.

### Area 5 — Ringkasan Aktivitas Hari Ini (ungu)

Rekomendasi isi:

- Total durasi latihan hari ini.
- Jumlah sesi yang selesai.
- Kemajuan menuju target pribadi.
- Tombol cepat memulai aktivitas.
- Jika tidak ada aktivitas, tampilkan pesan netral dan pilihan untuk membuat rencana.

Jam digital dapat ditambahkan, tetapi tidak perlu menjadi isi utama karena jam sistem sudah tersedia di taskbar. Ringkasan aktivitas lebih berguna untuk area ini.

### Area 6 — Playlist / Music (hijau)

- Daftar playlist untuk latihan.
- Buka playlist melalui aplikasi atau browser.
- Simpan playlist favorit berdasarkan kategori latihan.
- Kontrol pemutaran lanjutan hanya jika integrasi resmi mendukungnya.

## 5.3 Pencatatan kalori

- Kalori bersifat **perkiraan**.
- Penghitungan dapat bergantung pada jenis aktivitas, durasi, intensitas, dan data pengguna yang relevan.
- Jangan menampilkan hasil seolah-olah akurat secara medis.
- Jangan mewajibkan pengguna memasukkan berat badan untuk memakai fitur dasar.
- Bila memakai rumus atau MET, catat sumber metode dan jelaskan bahwa hasilnya merupakan estimasi.
- Pengguna dapat menyembunyikan informasi kalori jika tidak membutuhkannya.

## 5.4 Fitur lanjutan Exercise

- Grafik konsistensi mingguan dan bulanan.
- Pengingat aktivitas yang bisa dimatikan.
- Target berdasarkan durasi atau frekuensi, bukan hanya kalori.
- Template latihan.
- Ekspor riwayat aktivitas.
- Sinkronisasi perangkat kesehatan hanya jika ada integrasi resmi dan persetujuan pengguna.

## 5.5 Kriteria selesai Exercise

- Kalender dapat berpindah bulan dan menampilkan status harian.
- Rencana latihan dapat dibuat dan diedit.
- Timer dapat dimulai, dijeda, dilanjutkan, dan diselesaikan.
- Aktivitas yang selesai tercatat pada tanggal yang benar.
- Data tetap tersimpan setelah aplikasi ditutup.
- Estimasi kalori diberi label yang jelas sebagai perkiraan.

---

# 6. Modul Finance

## 6.1 Tujuan

Finance membantu pengguna memahami arus uang bulanan melalui pencatatan transaksi, perhitungan saldo, anggaran, dan target. Versi awal berfokus pada pencatatan manual, bukan akses otomatis ke rekening bank.

## 6.2 Panel dashboard

### Area 1 — Header

- Nama modul: Finance.
- Periode bulan yang sedang dipilih.
- Tombol tambah transaksi.
- Navigasi modul dan Settings.

### Area 2 — Month Overview / Transaction Filters (kuning)

Karena panel ini belum ditentukan, rekomendasi awalnya adalah **Month Overview**:

- Pemilih bulan dan tahun.
- Ringkasan jumlah transaksi.
- Filter jenis transaksi: pemasukan, pengeluaran, dan transfer internal.
- Filter kategori.
- Tombol menuju seluruh riwayat transaksi.
- Opsional: kalender transaksi untuk melihat tanggal dengan aktivitas keuangan.

Panel ini sebaiknya tidak menjadi tempat input transaksi utama; input transaksi dilakukan melalui tombol `Add Transaction` atau dialog khusus.

### Area 3 — Monthly Cash Flow (cyan)

Tampilkan tiga angka utama:

1. **Total Income** — total pemasukan pada periode yang dipilih.
2. **Total Expenses** — total pengeluaran pada periode yang dipilih.
3. **Net Balance / Cash Flow** — pemasukan dikurangi pengeluaran untuk periode tersebut.

Fungsi:

- Form input transaksi.
- Nama/judul transaksi.
- Nominal.
- Jenis: income atau expense.
- Kategori.
- Tanggal.
- Catatan opsional.
- Edit dan hapus transaksi.
- Grafik pemasukan dibandingkan pengeluaran.
- Riwayat transaksi terbaru.

Aturan perhitungan:

- `Net Cash Flow = Total Income - Total Expenses`.
- Angka bulanan dihitung dari transaksi yang tanggalnya masuk ke periode tersebut.
- Bedakan arus kas bulan ini dari saldo uang aktual. Saldo aktual memerlukan saldo awal atau pencatatan akun yang konsisten.
- Tentukan dengan jelas apakah transfer antar-akun dikecualikan dari income/expense agar tidak terhitung ganda.

### Area 4 — Monthly Goals / Budget (merah, dapat dibuka/tutup)

Rekomendasi isi:

- Target menabung bulan ini.
- Batas pengeluaran bulanan.
- Target pembelian tertentu.
- Nilai target, jumlah terkumpul, dan sisa target.
- Persentase kemajuan.
- Peringatan saat pengeluaran mendekati batas anggaran.
- Status target: berjalan, tercapai, atau dihentikan.

Pengguna boleh membuat beberapa target, bukan hanya satu. Jangan menyamakan target menabung dengan uang yang benar-benar tersedia jika transaksi dan saldo awal belum lengkap.

### Area 5 — Clock & Quick Summary (ungu)

Daripada timer, isi yang lebih berguna:

- Tanggal dan waktu saat ini, bila diinginkan.
- Sisa anggaran bulan ini.
- Total transaksi yang dicatat.
- Tombol cepat untuk menambahkan pemasukan atau pengeluaran.

Jam digital adalah elemen opsional; informasi anggaran sebaiknya lebih menonjol.

### Area 6 — Budget Insights (hijau)

Rekomendasi isi:

- Grafik pengeluaran berdasarkan kategori.
- Perbandingan income dan expense dari waktu ke waktu.
- Kategori dengan pengeluaran terbesar.
- Ringkasan terhadap anggaran.
- Pilihan periode mingguan, bulanan, atau rentang tanggal.

Untuk MVP, pilih satu visualisasi yang paling bermanfaat, misalnya grafik pengeluaran per kategori. Hindari terlalu banyak grafik kecil yang sulit dibaca.

## 6.3 Kategori transaksi awal

Kategori pemasukan:

- Uang saku / allowance.
- Gaji atau pendapatan.
- Hadiah.
- Lainnya.

Kategori pengeluaran:

- Makanan.
- Transportasi.
- Pendidikan.
- Kebutuhan pribadi.
- Hiburan.
- Tabungan atau tujuan keuangan.
- Lainnya.

Kategori harus dapat ditambah, diganti nama, dan dinonaktifkan oleh pengguna.

## 6.4 Privasi dan keamanan Finance

- Simpan data keuangan lokal secara default.
- Jangan meminta password bank atau PIN.
- Jangan mengirim data transaksi ke layanan luar tanpa persetujuan yang jelas.
- Sediakan backup dan ekspor CSV.
- Pertimbangkan proteksi file backup jika fitur tersebut ditambahkan.
- Konfirmasi sebelum menghapus transaksi.
- Gunakan tipe angka desimal yang tepat untuk nilai uang, bukan operasi floating-point sembarangan.
- Format mata uang mengikuti pengaturan pengguna, dengan IDR sebagai pilihan awal.

## 6.5 Kriteria selesai Finance

- Pengguna dapat mencatat dan mengedit transaksi.
- Total income, expense, dan net cash flow dihitung sesuai periode.
- Filter bulan mengubah ringkasan dengan benar.
- Target dan anggaran tersimpan.
- Grafik menggunakan data yang benar-benar tersimpan.
- Data dapat diekspor dan dicadangkan.

---

# 7. Integrasi Antar-Modul

Integrasi sebaiknya ringan dan tidak membuat modul saling bergantung secara berlebihan.

- **Study ↔ Pomodoro:** sesi fokus dapat dikaitkan dengan catatan atau tugas.
- **Exercise ↔ Agenda:** rencana dan hasil latihan menggunakan data tanggal yang konsisten.
- **Finance ↔ Target:** transaksi dapat digunakan untuk menghitung kemajuan anggaran dan target.
- **Dashboard utama:** menampilkan ringkasan dari ketiga modul, misalnya tugas terdekat, latihan hari ini, dan sisa anggaran.

Hindari menghubungkan setiap tabel database ke semua modul. Gunakan layanan atau fungsi khusus agar perubahan pada satu modul tidak merusak modul lain.

---

# 8. Arsitektur Teknis

## 8.1 Rekomendasi stack

| Kebutuhan | Pilihan awal | Catatan |
|---|---|---|
| Desktop UI | PySide6 | Mendukung layout panel yang fleksibel |
| Database lokal | SQLite | Cocok untuk aplikasi satu pengguna |
| Akses database | `sqlite3` atau SQLAlchemy | Mulai dengan `sqlite3` untuk scope kecil |
| Catatan | File Markdown | Tetap portabel dan bisa dibuka di editor lain |
| Markdown rendering | Library Markdown yang dipilih dan diuji | Sanitasi HTML sebelum preview |
| Grafik | Matplotlib atau Qt Charts | Pilih satu dulu |
| Timer | `QTimer` + timestamp | Hindari menghitung waktu dari tick semata |
| Pengaturan | JSON atau `QSettings` | Simpan tema dan preferensi UI |
| Testing | `pytest` | Uji logika dan perhitungan |
| Packaging | PyInstaller | Distribusi aplikasi Windows |

## 8.2 Struktur folder yang disarankan

```text
self-management/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── docs/
│   ├── PROJECT_BLUEPRINT.md
│   └── DATABASE_SCHEMA.md
├── assets/
│   ├── icons/
│   └── images/
├── src/
│   └── self_management/
│       ├── __init__.py
│       ├── main.py
│       ├── app.py
│       ├── core/
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── paths.py
│       │   ├── notifications.py
│       │   └── time_utils.py
│       ├── ui/
│       │   ├── main_window.py
│       │   ├── navigation.py
│       │   ├── widgets/
│       │   │   ├── collapsible_panel.py
│       │   │   └── timer_widget.py
│       │   └── styles/
│       │       ├── dark.qss
│       │       └── light.qss
│       ├── modules/
│       │   ├── study/
│       │   │   ├── page.py
│       │   │   ├── file_manager.py
│       │   │   ├── markdown_editor.py
│       │   │   ├── tasks.py
│       │   │   └── pomodoro.py
│       │   ├── exercise/
│       │   │   ├── page.py
│       │   │   ├── calendar.py
│       │   │   ├── workout_planner.py
│       │   │   ├── workout_session.py
│       │   │   └── estimates.py
│       │   └── finance/
│       │       ├── page.py
│       │       ├── transactions.py
│       │       ├── budgets.py
│       │       ├── goals.py
│       │       └── reports.py
│       └── services/
│           ├── backup_service.py
│           └── export_service.py
├── tests/
│   ├── test_finance.py
│   ├── test_timers.py
│   ├── test_tasks.py
│   └── test_workouts.py
└── user_data/
    ├── database/
    ├── notes/
    ├── backups/
    └── exports/
```

**Catatan:** `user_data/` adalah contoh konsep direktori data, bukan berarti data pengguna harus disimpan di dalam folder instalasi aplikasi. Pada aplikasi terpasang, gunakan direktori data pengguna yang sesuai dengan sistem operasi.

---

# 9. Rancangan Database Awal

Catatan Study disimpan sebagai file Markdown. SQLite digunakan untuk data terstruktur.

## 9.1 Tabel `tasks`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID tugas |
| `title` | TEXT | Judul |
| `description` | TEXT | Detail opsional |
| `status` | TEXT | pending / done |
| `priority` | TEXT | low / medium / high |
| `due_at` | TEXT nullable | Tenggat |
| `note_path` | TEXT nullable | Path catatan terkait |
| `created_at` | TEXT | Waktu dibuat |
| `completed_at` | TEXT nullable | Waktu selesai |

## 9.2 Tabel `study_sessions`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID sesi |
| `task_id` | INTEGER nullable | Tugas terkait |
| `note_path` | TEXT nullable | Catatan terkait |
| `started_at` | TEXT | Waktu mulai |
| `ended_at` | TEXT nullable | Waktu berakhir |
| `duration_seconds` | INTEGER | Durasi aktual |
| `session_type` | TEXT | focus / break |

## 9.3 Tabel `workout_sessions`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID sesi |
| `activity_type` | TEXT | Jenis aktivitas |
| `planned_minutes` | INTEGER nullable | Durasi rencana |
| `actual_seconds` | INTEGER | Durasi aktual |
| `started_at` | TEXT | Waktu mulai |
| `ended_at` | TEXT nullable | Waktu selesai |
| `intensity` | TEXT nullable | Intensitas opsional |
| `calories_estimate` | REAL nullable | Estimasi, bukan nilai pasti |
| `notes` | TEXT nullable | Catatan |

## 9.4 Tabel `workout_plans`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID rencana |
| `title` | TEXT | Nama rencana |
| `activity_type` | TEXT | Jenis aktivitas |
| `planned_at` | TEXT | Tanggal/waktu rencana |
| `planned_minutes` | INTEGER | Durasi target |
| `status` | TEXT | planned / completed / skipped |
| `notes` | TEXT nullable | Catatan |

## 9.5 Tabel `transactions`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID transaksi |
| `title` | TEXT | Nama transaksi |
| `amount_minor` | INTEGER | Nominal dalam satuan terkecil mata uang |
| `type` | TEXT | income / expense / transfer |
| `category_id` | INTEGER nullable | Kategori |
| `transaction_date` | TEXT | Tanggal transaksi |
| `notes` | TEXT nullable | Catatan |
| `created_at` | TEXT | Waktu dibuat |
| `updated_at` | TEXT | Waktu diperbarui |

Untuk IDR, nominal dapat disimpan sebagai bilangan bulat rupiah. Jika mendukung mata uang dengan pecahan, definisikan skala mata uang secara eksplisit.

## 9.6 Tabel `categories`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID kategori |
| `name` | TEXT | Nama kategori |
| `type` | TEXT | income / expense |
| `is_active` | INTEGER | Status aktif |

## 9.7 Tabel `budgets`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID anggaran |
| `category_id` | INTEGER nullable | Kategori; null dapat berarti anggaran umum |
| `period_month` | TEXT | Periode `YYYY-MM` |
| `limit_amount_minor` | INTEGER | Batas anggaran |
| `created_at` | TEXT | Waktu dibuat |

## 9.8 Tabel `financial_goals`

| Kolom | Tipe konseptual | Fungsi |
|---|---|---|
| `id` | INTEGER | ID target |
| `title` | TEXT | Nama target |
| `target_amount_minor` | INTEGER | Nilai target |
| `current_amount_minor` | INTEGER | Nilai terkumpul jika dikelola manual |
| `target_date` | TEXT nullable | Tenggat |
| `status` | TEXT | active / completed / paused |

Tentukan satu sumber kebenaran untuk nilai target. Jika kemajuan dihitung dari transaksi, jangan sekaligus menambah `current_amount` secara manual tanpa aturan yang jelas karena dapat menyebabkan hitungan ganda.

---

# 10. Alur Pengguna Utama

## Study

1. Pengguna membuka Study.
2. Memilih atau membuat folder catatan.
3. Membuat file Markdown.
4. Menulis catatan dan melihat preview.
5. Menyimpan catatan.
6. Membuat tugas dan mengaitkannya dengan catatan.
7. Menjalankan Pomodoro.
8. Melihat sesi fokus yang tercatat.

## Exercise

1. Pengguna membuka Exercise.
2. Melihat kalender bulan ini.
3. Membuat rencana latihan atau memilih aktivitas.
4. Menentukan durasi target.
5. Memulai timer latihan.
6. Menyelesaikan sesi dan menyimpan catatan.
7. Kalender menandai hari tersebut sebagai aktivitas selesai.
8. Ringkasan mingguan diperbarui.

## Finance

1. Pengguna membuka Finance.
2. Memilih periode bulan.
3. Menambahkan transaksi pemasukan atau pengeluaran.
4. Ringkasan dihitung ulang.
5. Pengguna mengatur anggaran dan target.
6. Grafik menunjukkan pola pengeluaran.
7. Pengguna mengekspor data atau membuat backup.

---

# 11. Tahapan Pengembangan

Jangan membangun seluruh fitur sekaligus. Selesaikan satu lapisan yang dapat diuji sebelum melanjutkan.

## Phase 1 — Foundation

- [ ] Membuat struktur project Python.
- [ ] Membuat jendela utama PySide6.
- [ ] Membuat navigasi tiga modul.
- [ ] Membuat layout enam panel berdasarkan gambar.
- [ ] Menambahkan panel collapse dan resize.
- [ ] Menyimpan preferensi tema dan layout.
- [ ] Menyiapkan database SQLite dan migrasi skema awal.

**Hasil:** aplikasi bisa dijalankan, berpindah modul, dan memiliki kerangka dashboard.

## Phase 2 — Study MVP

- [ ] File/folder explorer.
- [ ] Membuat dan mengedit file Markdown.
- [ ] Preview Markdown.
- [ ] Penyimpanan dan autosave yang aman.
- [ ] To-do list dasar.
- [ ] Pomodoro timer.
- [ ] Daftar tautan playlist.

**Hasil:** pengguna dapat mengelola catatan dan sesi belajar dari satu halaman.

## Phase 3 — Exercise MVP

- [ ] Kalender bulanan.
- [ ] Pembuatan rencana latihan.
- [ ] Timer sesi latihan.
- [ ] Penyimpanan riwayat.
- [ ] Penanda kalender setelah sesi selesai.
- [ ] Ringkasan durasi aktivitas.
- [ ] Playlist latihan.

**Hasil:** pengguna dapat merencanakan, mencatat, dan melihat riwayat latihan.

## Phase 4 — Finance MVP

- [ ] Input, edit, dan hapus transaksi.
- [ ] Filter berdasarkan bulan.
- [ ] Kalkulasi income, expense, dan net cash flow.
- [ ] Kategori transaksi.
- [ ] Anggaran dan target.
- [ ] Satu grafik utama.
- [ ] Ekspor CSV.

**Hasil:** pengguna dapat mencatat transaksi dan memahami arus kas bulanan.

## Phase 5 — Quality & Release

- [ ] Pengujian logika perhitungan.
- [ ] Pengujian timer.
- [ ] Validasi input dan pesan error.
- [ ] Backup dan pemulihan data.
- [ ] Pengujian ukuran jendela dan layout.
- [ ] Uji data kosong dan data dalam jumlah besar.
- [ ] Build aplikasi Windows dengan PyInstaller.
- [ ] Dokumentasi instalasi dan penggunaan.

## Phase 6 — Optional Enhancements

- [ ] Tema gelap dan terang yang lebih matang.
- [ ] Pencarian global.
- [ ] Grafik statistik lanjutan.
- [ ] Integrasi Spotify resmi jika memungkinkan.
- [ ] Sinkronisasi atau backup cloud yang opt-in.
- [ ] Fitur import/export lanjutan.

---

# 12. Aturan Kualitas dan Keamanan

- Pisahkan UI, logika bisnis, dan akses database.
- Jangan menaruh seluruh aplikasi dalam satu file Python.
- Jangan menaruh perhitungan finansial langsung di fungsi tombol UI.
- Validasi semua input, terutama nominal uang, tanggal, dan path file.
- Gunakan query SQL berparameter.
- Tangani kesalahan file dan database dengan pesan yang bisa dipahami pengguna.
- Hindari menghapus data secara permanen tanpa konfirmasi.
- Buat backup sebelum migrasi database yang berisiko.
- Jangan menyimpan kredensial API di dalam source code.
- Gunakan API resmi dan patuhi ketentuan layanan untuk integrasi eksternal.
- Uji logika inti secara terpisah dari tampilan UI.
- Pastikan semua fitur utama tetap berjalan tanpa koneksi internet.

---

# 13. Keputusan yang Perlu Ditetapkan

Keputusan berikut boleh berubah saat prototipe diuji:

1. **Target platform:** Windows terlebih dahulu atau lintas platform sejak awal.
2. **Tema:** gelap, terang, atau keduanya.
3. **Markdown:** Markdown standar atau ekstensi tertentu untuk alignment dan styling.
4. **Playlist:** tautan eksternal dahulu atau pemutar audio lokal.
5. **Data:** seluruhnya lokal dahulu atau perlu sinkronisasi lintas perangkat.
6. **Finance:** pencatatan manual dahulu atau integrasi layanan eksternal di masa depan.
7. **Exercise:** apakah kalori perlu ditampilkan di versi pertama atau cukup durasi dan konsistensi.
8. **Layout:** panel kanan dan panel bawah dapat di-collapse atau hanya panel tertentu.

**Rekomendasi:** gunakan penyimpanan lokal, tema gelap sebagai desain awal, Markdown standar, playlist berupa tautan, dan input keuangan manual. Keputusan ini menjaga scope tetap realistis untuk project Python pertama yang cukup besar.

---

# 14. Definisi MVP

Versi pertama dianggap layak dipakai jika:

- Aplikasi dapat dibuka tanpa error dan navigasi antar tiga modul berfungsi.
- Panel utama dapat di-resize sesuai kebutuhan.
- Study dapat membuat, mengedit, menyimpan, dan membuka kembali catatan Markdown.
- To-do list dan Pomodoro menyimpan hasil penting.
- Exercise dapat menjadwalkan dan mencatat sesi latihan.
- Finance dapat menyimpan transaksi dan menghitung ringkasan bulanan dengan benar.
- Data bertahan setelah aplikasi ditutup.
- Ada mekanisme backup atau ekspor untuk data penting.
- Tidak ada integrasi eksternal yang wajib agar fitur inti berjalan.

## Prioritas paling masuk akal

**Bangun Foundation → Study MVP → Exercise MVP → Finance MVP → Quality & Release.**

Selesaikan fondasi dashboard terlebih dahulu, lalu uji Study sampai benar-benar berfungsi. Setelah pola panel, database, dan penyimpanan stabil, dua modul lain akan lebih mudah dikembangkan tanpa membuat arsitektur berantakan.
