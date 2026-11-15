# FitTrack — Project Master Specification

> **Dokumen induk proyek untuk manusia, ChatGPT, dan AI coding agent.**  
> Versi: 1.1  
> Status: Draft fondasi / belum masuk implementasi  
> Nama kerja: **FitTrack**  
> Platform awal: **Android**  
> Bahasa utama aplikasi: Indonesia (struktur disiapkan agar mudah ditambah bahasa lain)

---

## 0. Instruksi untuk AI / Agent yang Membaca Dokumen Ini

Dokumen ini adalah sumber konteks utama proyek FitTrack. Jika kamu adalah ChatGPT, coding agent, atau developer yang melanjutkan proyek:

1. Baca seluruh dokumen sebelum mengusulkan perubahan besar atau menulis kode.
2. Jangan mengubah tujuan utama, ruang lingkup, teknologi, nama entitas database, atau aturan bisnis tanpa menjelaskan alasan dan meminta persetujuan pemilik proyek.
3. Jangan menganggap fitur yang ditulis sebagai selesai. Status implementasi hanya boleh diubah berdasarkan bukti kode, pengujian, atau konfirmasi pemilik proyek.
4. Kerjakan proyek secara bertahap. Selesaikan satu tahap, jelaskan file yang berubah, cara menjalankan, dan cara menguji. Setelah itu **berhenti dan tunggu konfirmasi pemilik proyek sebelum melanjutkan tahap berikutnya**.
5. Jangan mengklaim telah mengakses komputer lokal, menjalankan aplikasi, mengubah repository, atau melakukan commit jika tindakan tersebut tidak benar-benar dilakukan.
6. Utamakan solusi sederhana, dapat diuji, dan cocok untuk proyek ukuran menengah. Hindari menambah fitur hanya karena memungkinkan secara teknis.
7. Jangan memaksakan AI/ML. Gunakan perhitungan biasa dan aturan yang transparan jika sudah cukup.
8. Jangan mengarang data kesehatan, hasil GPS, nutrisi, atau hasil pengujian.
9. Jaga privasi. Data kesehatan, aktivitas, dan lokasi adalah data pribadi. Minta izin yang jelas, kumpulkan seperlunya, dan sediakan cara menghapus data.
10. Jika informasi penting belum ditentukan, ajukan satu pertanyaan yang paling menentukan. Jangan membuat banyak asumsi tersembunyi.

### Format laporan setiap tahap

Setiap penyelesaian tahap wajib melaporkan:

- Tujuan tahap.
- Fitur yang berhasil dibuat.
- Daftar file yang dibuat/diubah.
- Cara menjalankan.
- Cara menguji, termasuk hasil yang diharapkan.
- Batasan atau bug yang diketahui.
- Keputusan yang masih menunggu persetujuan.
- Status task list yang benar-benar selesai.

---

# 1. Ringkasan Proyek

## 1.1 Nama dan jenis aplikasi

**Nama aplikasi: FitTrack** (nama proyek yang ditetapkan; pemeriksaan merek dagang/nama aplikasi di toko aplikasi dilakukan sebelum publikasi).

FitTrack adalah aplikasi Android untuk mencatat dan memantau aktivitas kebugaran serta pola hidup sehari-hari. Pengguna dapat mencatat latihan, lari atau berjalan, asupan makanan, dan tidur dalam satu aplikasi, lalu melihat riwayat, streak, serta ringkasan konsistensi kebiasaan.

**Deskripsi singkat:** Aplikasi Android berbasis Python yang membantu pengguna memahami dan mengelola kebiasaan olahraga serta gaya hidup melalui pencatatan aktivitas, GPS, dan ringkasan perkembangan.

## 1.2 Masalah di lingkungan

Banyak orang ingin menjaga kebugaran dan pola hidup sehat, tetapi catatan olahraga, aktivitas kardio, makanan, dan tidur sering tersebar di aplikasi berbeda atau tidak dicatat secara konsisten. Akibatnya, pengguna kesulitan melihat hubungan antar-kebiasaan dan mengevaluasi perkembangan dirinya dari waktu ke waktu.

FitTrack menawarkan tempat pencatatan terpadu yang sederhana agar informasi aktivitas harian dan ringkasan kebiasaan lebih mudah dipantau.

FitTrack bukan aplikasi diagnosis medis, bukan pengganti dokter/pelatih, dan bukan alat untuk menentukan apakah tubuh seseorang ideal.

## 1.2 Masalah yang ingin diselesaikan

Pengguna sering memakai aplikasi berbeda untuk mencatat lari, latihan beban, makanan, dan tidur. Akibatnya, progres tersebar dan sulit dilihat sebagai satu rangkaian kebiasaan.

FitTrack menyatukan pencatatan tersebut dalam satu aplikasi sehingga pengguna dapat:

- Memahami kondisi dan kebiasaan awalnya.
- Membuat target aktivitas yang realistis.
- Mencatat latihan gym atau home workout.
- Melacak lari dan jalan menggunakan GPS.
- Mencatat kalori dan protein secara sederhana.
- Mencatat waktu tidur dan bangun.
- Memantau streak dan konsistensi.
- Melihat ringkasan mingguan, bulanan, dan tahunan.
- Memahami alasan di balik skor dan perubahan progres.

## 1.3 Prinsip produk

1. **Personal, bukan kompetitif:** target disesuaikan dengan kondisi dan kemampuan pengguna.
2. **Progress over perfection:** konsistensi jangka panjang lebih penting daripada satu hari yang sempurna.
3. **Rest is part of training:** hari istirahat terencana tidak dianggap gagal.
4. **Explainable score:** setiap skor harus memiliki komponen dan alasan yang bisa dilihat.
5. **Manual-first, integration-ready:** pencatatan manual tetap tersedia meskipun integrasi sensor/API belum ada.
6. **No forced AI:** AI hanya ditambahkan jika ada masalah yang memang lebih baik diselesaikan dengan AI.
7. **Privacy by design:** lokasi GPS dan informasi kesehatan tidak boleh dikumpulkan tanpa kebutuhan dan izin.

---

# 2. Sasaran Pengguna dan Batasan

## 2.1 Sasaran pengguna

Pengguna individu yang ingin mengelola kebiasaan olahraga dan gaya hidup sehari-hari, baik pemula maupun yang sudah terbiasa berolahraga.

## 2.2 Platform dan perangkat

- Target awal: Android.
- Bahasa pemrograman aplikasi: Python.
- UI Android: Kivy dan KivyMD.
- Database lokal utama: SQLite.
- ORM opsional: SQLAlchemy.
- Backend/server tidak diperlukan untuk MVP; FastAPI dapat dipertimbangkan nanti jika sinkronisasi multi-perangkat atau akun online benar-benar dibutuhkan.
- GPS menggunakan layanan lokasi perangkat Android, bukan membuat atau melatih model GPS sendiri.

## 2.3 Batasan versi awal

- Tidak membuat diagnosis kesehatan.
- Tidak mengklaim dapat mengukur massa otot dari foto.
- Tidak menilai kebugaran atau kesehatan hanya dari penampilan/foto.
- Tidak menyediakan rekomendasi diet ekstrem atau pembatasan kalori agresif.
- Tidak mengharuskan wearable/smartwatch.
- Tidak melakukan pelacakan lokasi secara diam-diam.
- Tidak mengumpulkan isi pesan, kontak, atau data perangkat yang tidak diperlukan.
- Tidak membutuhkan model ML pada MVP.
- Tidak membuat jejaring sosial, feed publik, kompetisi global, atau marketplace.

## 2.4 Catatan keselamatan kesehatan

FitTrack adalah alat pencatatan kebiasaan dan aktivitas, bukan sumber keputusan medis. Nilai berat badan, tinggi badan, kalori, protein, durasi tidur, dan skor harus ditampilkan sebagai data atau estimasi, bukan diagnosis.

Untuk pengguna yang masih dalam masa pertumbuhan, aplikasi tidak boleh otomatis mendorong bulking/cutting atau target defisit kalori. Target nutrisi yang berdampak pada pembatasan makan perlu arahan tenaga kesehatan yang kompeten. Aplikasi boleh mencatat makanan dan memberi edukasi umum, tetapi tidak boleh memberi target ekstrem atau menyebut angka tertentu sebagai kewajiban universal.

---

# 3. Tujuan Produk dan Indikator Keberhasilan

## 3.1 Tujuan utama

Menyediakan satu tempat untuk mencatat dan memahami progres aktivitas fisik serta kebiasaan harian.

## 3.2 Indikator keberhasilan produk

- Pengguna dapat menyelesaikan onboarding dan membuat profil.
- Pengguna dapat mencatat workout tanpa koneksi internet.
- Pengguna dapat mencatat aktivitas jalan/lari.
- Pengguna dapat melihat ringkasan aktivitas harian dan mingguan.
- Pengguna dapat mencatat makanan dan melihat total energi/protein yang tercatat.
- Pengguna dapat mencatat tidur secara manual.
- Streak dihitung dengan aturan yang jelas dan tidak menghukum rest day.
- Wellness Score dapat dijelaskan dari komponen dan data sumbernya.
- Pengguna dapat mengekspor atau menghapus datanya.

## 3.3 Bukan indikator keberhasilan

- Menjadi lebih kurus atau lebih berat.
- Mencapai bentuk tubuh tertentu.
- Mendapat skor sempurna setiap hari.
- Berolahraga setiap hari tanpa istirahat.
- Membandingkan tubuh pengguna dengan atlet atau pengguna lain.

---

# 4. Struktur Navigasi dan UI

## 4.1 Navigasi utama

Aplikasi menggunakan navigasi utama yang mudah dijangkau. Pada ponsel, gunakan bottom navigation atau tab yang jelas. Gesture swipe kanan/kiri boleh menjadi tambahan, tetapi jangan menjadi satu-satunya cara berpindah halaman karena tidak selalu mudah ditemukan atau diakses.

Menu utama:

1. **Home** — ringkasan harian dan akses cepat.
2. **Cardio** — lari, jalan, GPS, dan riwayat.
3. **Workout** — gym dan home workout.
4. **Food** — catatan makanan, kalori, dan protein.
5. **Sleep** — jadwal, pencatatan, dan konsistensi tidur.

Profile/Settings dapat diakses dari avatar atau ikon pengaturan di Home.

## 4.2 Home Dashboard

Home adalah pusat informasi. Komponen yang direncanakan:

- Sapaan dan tanggal.
- Ringkasan Wellness Score periode berjalan.
- Perubahan skor dibanding periode sebelumnya.
- Aktivitas hari ini.
- Progress target mingguan.
- Streak olahraga.
- Ringkasan tidur terakhir.
- Ringkasan nutrisi hari ini.
- Tombol cepat: Start Run, Log Workout, Add Food, Log Sleep.
- Informasi singkat yang menjelaskan progres atau hal yang perlu diperhatikan.

Jangan menampilkan semua grafik sekaligus. Gunakan kartu ringkas dan halaman detail untuk informasi lebih lengkap.

## 4.3 Cardio

Fitur:

- Memulai sesi lari/jalan.
- GPS route pada peta.
- Jarak, durasi, pace, dan kecepatan.
- Pause, resume, dan finish.
- Ringkasan setelah sesi selesai.
- Riwayat aktivitas.
- Detail rute dan statistik.
- Pencatatan manual jika GPS tidak tersedia.

Ketentuan GPS:

- Meminta izin lokasi saat fitur digunakan.
- Menjelaskan alasan izin lokasi.
- Mendukung lokasi saat aplikasi berada di background jika implementasi dan kebijakan Android mengizinkan.
- Menampilkan indikator bahwa tracking sedang berjalan.
- Menangani GPS tidak akurat, sinyal hilang, baterai rendah, dan aplikasi ditutup.
- Menyimpan titik GPS secara berkala dan menghubungkannya menjadi rute.
- Sediakan mode manual jika pengguna tidak ingin berbagi lokasi.
- Jangan mengunggah rute ke server tanpa persetujuan yang jelas.

Metrik:

- Distance: meter/kilometer.
- Duration: detik.
- Pace: menit per kilometer.
- Speed: kilometer per jam.
- Elevation gain: opsional, hanya jika sumber data mendukung.

Jangan menganggap kalori terbakar dari GPS sebagai pengukuran pasti. Jika ditampilkan, beri label estimasi dan jelaskan bahwa hasilnya dapat berbeda dari kondisi aktual.

## 4.4 Workout — Gym dan Home Workout

### Jenis latihan

- Gym / resistance training.
- Home workout / bodyweight training.

### Program/template latihan

Contoh template yang dapat disediakan sebagai pilihan, bukan kewajiban:

- Push / Pull / Legs.
- Upper / Lower.
- Full Body.
- Custom Routine.

### Exercise catalogue

Setiap exercise memiliki:

- Nama.
- Kategori otot/gerakan.
- Equipment.
- Jenis latihan.
- Instruksi singkat.
- Variasi yang relevan.
- Sumber referensi instruksi bila tersedia.

Contoh gym:

- Chest Press.
- Chest Fly.
- Shoulder Press.
- Lat Pulldown.
- Row.
- Squat.
- Leg Curl.

Contoh home workout:

- Push-up.
- Incline Push-up.
- Knee Push-up.
- Squat.
- Lunge.
- Plank.

### Workout session

Pengguna dapat:

- Memilih template atau membuat sesi kosong.
- Menambahkan exercise.
- Mengisi set, repetisi, beban, atau durasi sesuai jenis gerakan.
- Menandai set selesai.
- Menyimpan catatan.
- Mengakhiri sesi dan melihat ringkasan.

Data latihan harus fleksibel. Tidak semua gerakan memakai beban; sebagian memakai repetisi, durasi, atau jarak.

## 4.5 Food / Nutrition

Tujuan: pencatatan sederhana, bukan aplikasi diet yang sangat kompleks.

Fitur:

- Tambah makanan secara manual.
- Pilih waktu makan.
- Isi nama makanan dan porsi.
- Isi estimasi kalori dan protein.
- Lihat total harian.
- Lihat riwayat.
- Simpan makanan yang sering dikonsumsi sebagai favorit.

Data nutrisi dapat berasal dari input manual pada MVP. Integrasi database makanan/API dapat menjadi tahap lanjutan setelah sumber data dipilih dan lisensinya diperiksa.

Jangan menyatakan nilai kalori/protein sebagai pasti jika berasal dari estimasi atau input pengguna.

## 4.6 Sleep

Fitur awal:

- Target/rentang waktu tidur.
- Pengingat menjelang waktu tidur.
- Konfirmasi manual saat akan tidur.
- Konfirmasi waktu bangun.
- Durasi tidur berdasarkan catatan.
- Riwayat tidur.
- Ringkasan konsistensi jam tidur dan bangun.

Jangan menganggap pengguna tidur hanya karena membuka aplikasi pada jam tertentu. Notifikasi hanya meminta konfirmasi. Integrasi wearable/Health Connect dapat dipertimbangkan kemudian, dengan izin pengguna.

## 4.7 Gamification

Fitur:

- Daily activity streak.
- XP atau poin aktivitas.
- Badge/achievement.
- Weekly challenge.
- Progress bar.
- Reminder.

Aturan penting:

- Hari istirahat terencana tidak boleh dianggap kegagalan.
- Jangan mendorong olahraga berlebihan demi mempertahankan streak.
- Streak harus berdasarkan target yang dipilih pengguna dan jadwal aktivitas yang masuk akal.
- Pengguna dapat mematikan reminder.
- Jangan membuat pesan yang mempermalukan pengguna ketika melewatkan aktivitas.

---

# 5. Onboarding dan Initial Assessment

## 5.1 Tujuan

Mengumpulkan informasi minimum yang dibutuhkan untuk mengatur pengalaman aplikasi. Onboarding tidak dimaksudkan untuk menentukan apakah pengguna sehat atau memiliki tubuh atletis.

## 5.2 Data profil

- Display name.
- Tanggal lahir atau kelompok usia (pilih pengumpulan data minimum).
- Tinggi badan (opsional).
- Berat badan (opsional).
- Satuan metrik.
- Preferensi aktivitas.
- Pengalaman olahraga secara umum.
- Frekuensi aktivitas dalam periode terakhir.
- Pilihan gym/home workout.
- Hari latihan yang diinginkan.
- Jam pengingat tidur (opsional).

Hindari meminta data sensitif yang tidak diperlukan. Beri pilihan untuk melewati data berat/tinggi.

## 5.3 Riwayat olahraga

Pertanyaan onboarding dapat meliputi:

- Apakah pernah melakukan gym?
- Apakah pernah melakukan home workout?
- Apakah rutin berjalan atau berlari?
- Seberapa sering beraktivitas dalam beberapa minggu terakhir?
- Apakah ada aktivitas yang ingin dihindari atau keterbatasan yang perlu diperhatikan?

Jawaban digunakan untuk personalisasi tampilan dan target aktivitas awal yang konservatif, bukan untuk diagnosis.

## 5.4 Foto tubuh

Foto tidak menjadi persyaratan MVP. Jangan menggunakan foto untuk mengestimasi massa otot, persentase lemak, atau memberi label sehat/tidak sehat. Jika suatu saat fitur foto progres ditambahkan, simpan secara privat, minta persetujuan eksplisit, dan jangan menjalankan analisis penampilan tubuh sebagai skor kesehatan.

---

# 6. Wellness Score

## 6.1 Definisi

Nama yang disarankan: **Wellness Score** atau **Consistency Score**.

Skor ini adalah ringkasan kebiasaan yang tercatat di FitTrack. Skor bukan ukuran medis, bukan ukuran komposisi tubuh, dan bukan penilaian kualitas seseorang.

## 6.2 Periode

- Daily: ringkasan hari ini.
- Weekly: ringkasan 7 hari.
- Monthly: ringkasan bulan kalender.
- Yearly: ringkasan tahun kalender.

Untuk skor bulanan/tahunan, gunakan agregasi data harian/mingguan yang tersedia. Jangan membandingkan periode dengan jumlah data yang tidak setara tanpa memberi keterangan.

## 6.3 Komponen yang disarankan

Versi awal menggunakan empat komponen:

1. **Activity Consistency** — seberapa konsisten pengguna melakukan aktivitas yang direncanakan.
2. **Workout/Cardio Balance** — variasi aktivitas berdasarkan rencana pengguna, bukan kewajiban melakukan semua jenis latihan.
3. **Sleep Consistency** — konsistensi waktu tidur/bangun berdasarkan catatan pengguna.
4. **Nutrition Logging Consistency** — kelengkapan pencatatan makanan, bukan penilaian moral terhadap makanan.

Komponen nutrisi harus diperlakukan hati-hati. Tidak mencatat makanan bukan berarti pola makan buruk. Tampilkan tingkat kelengkapan data terpisah dari skor.

## 6.4 Rumus awal yang transparan

Rumus final harus diuji dan dapat diubah setelah prototipe. Contoh awal:

- Activity Consistency: 40%
- Workout/Cardio Balance: 20%
- Sleep Consistency: 25%
- Nutrition Logging Consistency: 15%

`Wellness Score = Σ (component_score × component_weight)`

Setiap component score berada pada skala 0–100. Komponen yang tidak memiliki cukup data tidak boleh otomatis dianggap 0. Sistem harus:
- Menandai komponen sebagai `insufficient_data`.
- Menyesuaikan bobot pada komponen yang memiliki data cukup, atau menampilkan skor parsial.
- Menampilkan tingkat kelengkapan data.
- Menjelaskan alasan skor berubah.

**Catatan:** bobot di atas hanya rancangan awal, bukan standar kesehatan ilmiah. Jangan menyebut skor 80 sebagai “sehat” atau skor 40 sebagai “tidak sehat”.

## 6.5 Informasi penjelas pada dashboard

Setiap skor harus disertai:
- Skor periode ini.
- Perubahan dibanding periode sebelumnya.
- Komponen yang meningkat/menurun.
- Jumlah hari dengan data.
- Data yang belum cukup.
- Saran kebiasaan yang ringan dan tidak menghakimi.

Contoh copy:

> “Konsistensi aktivitas tercatat meningkat dibanding minggu lalu. Catatan tidur baru tersedia untuk 3 malam, jadi komponen tidur belum cukup untuk dibandingkan.”

Hindari copy seperti:
- “Tubuhmu tidak sehat.”
- “Kamu gagal minggu ini.”
- “Kamu harus membakar lebih banyak kalori.”
- “Kamu harus olahraga setiap hari.”

---

# 7. Daily Streak dan Gamification Rules

## 7.1 Definisi streak

Streak menghitung hari ketika pengguna memenuhi target aktivitas harian yang telah ditentukan. Target harus personal dan realistis.

Contoh:
- Pengguna memilih target aktivitas 3 hari per minggu.
- Hari latihan yang direncanakan ditandai sebagai activity day.
- Hari istirahat terencana tidak memutus streak.
- Jika target mingguan tercapai, aplikasi memberikan progress/achievement.

Lebih baik gunakan konsep **weekly consistency streak** daripada mewajibkan olahraga setiap hari.

## 7.2 Data streak

- Current streak.
- Longest streak.
- Last qualified date.
- Planned activity days.
- Qualified activity days.
- Rest days.
- Streak history.

## 7.3 Syarat aktivitas memenuhi target

Contoh aturan awal yang dapat dikonfigurasi:
- Workout yang selesai dan memiliki durasi/isi valid.
- Cardio yang selesai dan memiliki durasi/jarak valid.
- Aktivitas ringan yang secara eksplisit didukung target pengguna.

Jangan memberi poin berdasarkan kalori terbakar semata. Jangan mendorong aktivitas tambahan ketika target sudah terpenuhi.

---

# 8. Model Data dan Database

## 8.1 Pilihan database

**MVP:** SQLite sebagai database lokal di perangkat Android.

Aplikasi menggunakan pendekatan offline-first: pencatatan dasar tetap berjalan tanpa internet. Akses database dilakukan melalui modul repository/data-access agar logika aplikasi tidak bergantung langsung pada query SQL. SQLAlchemy dapat digunakan jika cocok dengan kebutuhan, tetapi penggunaan ORM bukan kewajiban. Jika kelak membutuhkan sinkronisasi multi-perangkat atau akun online, backend Python FastAPI dan PostgreSQL dapat ditambahkan sebagai tahap terpisah.

## 8.2 Aturan database

- Gunakan primary key UUID.
- Simpan waktu dalam UTC di database; konversi ke zona waktu perangkat saat ditampilkan.
- Gunakan `created_at` dan `updated_at` pada entitas yang relevan.
- Simpan satuan secara konsisten (misalnya meter, gram, detik).
- Hindari menyimpan data turunan yang bisa dihitung ulang, kecuali untuk snapshot historis.
- Data GPS harus dipisahkan dari ringkasan aktivitas.
- Terapkan foreign key dan index pada kolom pencarian.
- Hapus akun harus menghapus data terkait sesuai kebijakan retensi.
- Jangan menyimpan password dalam bentuk teks biasa; gunakan hash aman jika autentikasi dibuat.

## 8.3 Entitas inti

### `users`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| email | TEXT, nullable | Email jika akun online digunakan |
| password_hash | TEXT, nullable | Hash, tidak pernah plaintext |
| display_name | TEXT | Nama tampilan |
| timezone | TEXT | Contoh `Asia/Jakarta` |
| created_at | DATETIME | Waktu dibuat |
| updated_at | DATETIME | Waktu diubah |

Untuk mode lokal tanpa akun, user dapat dibuat sebagai profil lokal.

### `user_profiles`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| birth_date | DATE, nullable | Opsional; kumpulkan hanya jika dibutuhkan |
| height_cm | REAL, nullable | Tinggi terakhir yang dicatat |
| preferred_units | TEXT | `metric` untuk MVP |
| experience_level | TEXT | `beginner`, `intermediate`, `advanced`, `unspecified` |
| preferred_training_mode | TEXT | `gym`, `home`, `both` |
| created_at | DATETIME | Waktu dibuat |
| updated_at | DATETIME | Waktu diubah |

### `body_measurements`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| measured_at | DATETIME | Waktu pengukuran |
| weight_kg | REAL, nullable | Opsional |
| height_cm | REAL, nullable | Opsional |
| note | TEXT, nullable | Catatan pengguna |
| created_at | DATETIME | Waktu dibuat |

Catatan: pengukuran tubuh bersifat opsional dan bukan dasar tunggal Wellness Score.

### `activity_preferences`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| activity_type | TEXT | `workout`, `cardio`, `walking`, dll. |
| target_days_per_week | INTEGER | Target yang dipilih |
| planned_days_json | TEXT | Hari yang direncanakan |
| is_active | BOOLEAN | Status preferensi |

### `exercise_catalog`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| name | TEXT | Nama gerakan |
| category | TEXT | Contoh `push`, `pull`, `legs`, `core`, `cardio` |
| training_mode | TEXT | `gym`, `home`, `both` |
| equipment | TEXT, nullable | Alat yang dibutuhkan |
| tracking_type | TEXT | `reps_weight`, `reps`, `duration`, `distance` |
| instructions | TEXT, nullable | Instruksi singkat |
| is_custom | BOOLEAN | Apakah dibuat pengguna |

### `workout_templates`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID, nullable | Null untuk template bawaan |
| name | TEXT | Nama template |
| split_type | TEXT | `ppl`, `upper_lower`, `full_body`, `custom` |
| training_mode | TEXT | `gym`, `home`, `both` |
| description | TEXT, nullable | Keterangan |

### `workout_template_exercises`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| template_id | UUID | FK workout_templates |
| exercise_id | UUID | FK exercise_catalog |
| sort_order | INTEGER | Urutan gerakan |
| target_sets | INTEGER, nullable | Set target |
| target_reps | INTEGER, nullable | Repetisi target |

### `workout_sessions`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| template_id | UUID, nullable | Template yang digunakan |
| title | TEXT | Nama sesi |
| training_mode | TEXT | `gym` atau `home` |
| started_at | DATETIME | Mulai |
| ended_at | DATETIME, nullable | Selesai |
| duration_seconds | INTEGER, nullable | Durasi |
| notes | TEXT, nullable | Catatan |
| status | TEXT | `in_progress`, `completed`, `cancelled` |

### `workout_sets`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| session_id | UUID | FK workout_sessions |
| exercise_id | UUID | FK exercise_catalog |
| set_number | INTEGER | Nomor set |
| reps | INTEGER, nullable | Repetisi |
| weight_kg | REAL, nullable | Beban |
| duration_seconds | INTEGER, nullable | Durasi |
| distance_m | REAL, nullable | Jarak |
| is_completed | BOOLEAN | Set selesai atau belum |

### `cardio_activities`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| activity_type | TEXT | `run`, `walk`, `other` |
| started_at | DATETIME | Mulai |
| ended_at | DATETIME | Selesai |
| duration_seconds | INTEGER | Durasi |
| distance_m | REAL | Jarak |
| avg_pace_seconds_per_km | REAL, nullable | Pace rata-rata |
| avg_speed_kmh | REAL, nullable | Kecepatan rata-rata |
| elevation_gain_m | REAL, nullable | Opsional |
| source | TEXT | `gps`, `manual`, `import` |
| notes | TEXT, nullable | Catatan |

### `cardio_gps_points`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| cardio_activity_id | UUID | FK cardio_activities |
| recorded_at | DATETIME | Waktu titik direkam |
| latitude | REAL | Latitude |
| longitude | REAL | Longitude |
| altitude_m | REAL, nullable | Ketinggian |
| accuracy_m | REAL, nullable | Akurasi GPS |
| sequence_no | INTEGER | Urutan titik |

GPS points adalah data sensitif. Simpan hanya jika pengguna mengaktifkan GPS tracking. Pertimbangkan penghapusan titik GPS setelah statistik rute selesai jika pengguna memilih mode privasi.

### `food_entries`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| food_name | TEXT | Nama makanan |
| meal_type | TEXT | `breakfast`, `lunch`, `dinner`, `snack`, `other` |
| quantity_description | TEXT, nullable | Deskripsi porsi |
| calories_kcal | REAL, nullable | Estimasi kalori |
| protein_g | REAL, nullable | Estimasi protein |
| consumed_at | DATETIME | Waktu makan |
| source | TEXT | `manual`, `database`, `import` |
| notes | TEXT, nullable | Catatan |

### `sleep_logs`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| sleep_started_at | DATETIME | Waktu mulai tidur |
| wake_at | DATETIME | Waktu bangun |
| duration_minutes | INTEGER | Durasi hasil perhitungan |
| source | TEXT | `manual`, `health_connect`, `wearable` |
| quality_rating | INTEGER, nullable | Penilaian subjektif opsional |
| notes | TEXT, nullable | Catatan |

### `sleep_preferences`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| target_bedtime | TIME, nullable | Target waktu tidur |
| target_wake_time | TIME, nullable | Target waktu bangun |
| reminder_enabled | BOOLEAN | Pengingat aktif |
| reminder_minutes_before | INTEGER | Jarak pengingat |

### `daily_activity_records`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| local_date | DATE | Tanggal lokal pengguna |
| planned_activity | BOOLEAN | Apakah hari latihan terencana |
| completed_activity | BOOLEAN | Apakah target aktivitas tercapai |
| planned_rest_day | BOOLEAN | Hari istirahat terencana |
| activity_minutes | INTEGER | Total menit aktivitas tercatat |
| created_at | DATETIME | Waktu dibuat |
| updated_at | DATETIME | Waktu diubah |

### `wellness_score_snapshots`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| period_type | TEXT | `daily`, `weekly`, `monthly`, `yearly` |
| period_start | DATE | Awal periode |
| period_end | DATE | Akhir periode |
| total_score | REAL, nullable | Null jika data belum cukup |
| activity_score | REAL, nullable | Komponen aktivitas |
| balance_score | REAL, nullable | Komponen variasi aktivitas |
| sleep_score | REAL, nullable | Komponen tidur |
| nutrition_logging_score | REAL, nullable | Kelengkapan pencatatan |
| data_completeness | REAL | Kelengkapan data |
| explanation_json | TEXT | Rincian alasan/perhitungan |
| calculated_at | DATETIME | Waktu dihitung |

### `streak_records`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| current_streak | INTEGER | Streak saat ini |
| longest_streak | INTEGER | Streak terpanjang |
| last_qualified_date | DATE, nullable | Tanggal terakhir memenuhi aturan |
| updated_at | DATETIME | Waktu diubah |

### `achievements`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| code | TEXT, unique | Kode achievement |
| name | TEXT | Nama |
| description | TEXT | Deskripsi |
| icon_key | TEXT, nullable | Identifier ikon |
| criteria_json | TEXT | Kriteria pencapaian |

### `user_achievements`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| achievement_id | UUID | FK achievements |
| unlocked_at | DATETIME | Waktu didapat |

### `reminders`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| reminder_type | TEXT | `workout`, `sleep`, `log_food`, dll. |
| scheduled_time | TEXT | Waktu lokal |
| days_json | TEXT | Hari aktif |
| enabled | BOOLEAN | Status |
| message | TEXT, nullable | Pesan |

### `user_settings`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | FK users |
| theme | TEXT | `system`, `light`, `dark` |
| distance_unit | TEXT | `km`, `mi` |
| weight_unit | TEXT | `kg`, `lb` |
| notifications_enabled | BOOLEAN | Status notifikasi |
| gps_privacy_mode | TEXT | Preferensi privasi |

## 8.4 Relasi inti

- `users` 1—1 `user_profiles`
- `users` 1—N `body_measurements`
- `users` 1—N `workout_sessions`
- `workout_sessions` 1—N `workout_sets`
- `exercise_catalog` 1—N `workout_sets`
- `users` 1—N `cardio_activities`
- `cardio_activities` 1—N `cardio_gps_points`
- `users` 1—N `food_entries`
- `users` 1—N `sleep_logs`
- `users` 1—N `wellness_score_snapshots`
- `users` 1—1 `streak_records`
- `users` 1—N `user_achievements`

---

# 9. Arsitektur Sistem

## 9.1 Rekomendasi stack

### Aplikasi Android (Python)

- Python 3 sebagai bahasa utama.
- Kivy untuk UI aplikasi.
- KivyMD untuk komponen UI bergaya Material (opsional, sesuai kompatibilitas versi).
- SQLite untuk penyimpanan lokal.
- SQLAlchemy sebagai ORM opsional; `sqlite3` bawaan Python juga cukup untuk MVP sederhana.
- Plyer untuk akses fitur perangkat yang didukung, seperti lokasi dan notifikasi; uji kompatibilitas Android pada perangkat nyata.
- `pyjnius` atau bridge Android yang sesuai jika API Android tertentu belum tersedia melalui Plyer.
- Matplotlib atau library grafik yang kompatibel jika grafik dibutuhkan; utamakan visualisasi sederhana.
- Pytest untuk pengujian logika dan database.

### Build dan pengujian Android

- Buildozer dan python-for-android untuk membangun APK.
- Lingkungan build Linux; jika komputer pengembangan menggunakan Windows, gunakan WSL2 dengan distro Linux yang didukung atau mesin Linux. Buildozer tidak diperlakukan sebagai alur build native Windows biasa.
- Android SDK/Platform Tools sesuai kebutuhan Buildozer.
- Android Emulator atau perangkat Android nyata untuk pengujian.
- Git dan GitHub untuk version control.
- VS Code atau editor pilihan pengguna.

### Backend (opsional, bukan bagian MVP)

- Python 3 dan FastAPI jika kelak diperlukan API online.
- Pydantic untuk validasi skema API.
- SQLAlchemy dan Alembic jika backend memakai database relasional.
- PostgreSQL untuk deployment multi-user.

**Catatan penting:** aplikasi dan logika utamanya tetap ditulis dengan Python. Android tetap menyediakan API sistem operasi untuk GPS, notifikasi, izin lokasi, dan proses latar belakang. Mengakses API tersebut melalui bridge tidak berarti UI atau logika aplikasi ditulis ulang dalam Kotlin/Java. Beberapa fitur Android mungkin memerlukan konfigurasi/build khusus dan tidak selalu berjalan sama di emulator.

## 9.2 Arsitektur logis

```text
FitTrack Android App (Python)
│
├── Presentation Layer (Kivy / KivyMD)
│   ├── Home Dashboard
│   ├── Cardio
│   ├── Workout
│   ├── Food
│   ├── Sleep
│   └── Profile / Settings
│
├── Application Layer
│   ├── Use Cases
│   ├── Validation
│   └── Wellness / Streak Rules
│
├── Data Layer
│   ├── Repositories
│   └── SQLite Database
│
└── Android Device Integration
    ├── GPS / Location API
    ├── Notifications
    └── Background Location (jika didukung dan diizinkan)

Optional future service:
Python FastAPI → PostgreSQL
```

## 9.3 Prinsip offline-first

Untuk MVP, pencatatan aktivitas dasar sebaiknya tetap dapat digunakan tanpa internet. Data disimpan lokal terlebih dahulu. Sinkronisasi akun/server dapat menjadi tahap lanjutan.

Jangan membuat sinkronisasi dua arah sebelum struktur data dan konflik perubahan dirancang.

## 9.4 Backend dan API di masa depan

Backend bukan kebutuhan MVP. Jangan membuat API, sistem login online, atau sinkronisasi sebelum aplikasi lokal selesai dan kebutuhan multi-perangkat sudah jelas. Jika dibutuhkan nanti, rancang FastAPI sebagai layanan Python terpisah dengan endpoint profil, workout, cardio, food, sleep, dashboard, wellness score, dan streak.

---

# 10. Struktur Folder Proyek

Struktur satu aplikasi Python Android yang disarankan:

```text
fittrack/
│
├── README.md
├── PROJECT_MASTER.md
├── CHANGELOG.md
├── requirements.txt
├── buildozer.spec
├── .gitignore
│
├── docs/
│   ├── DATABASE_DESIGN.md
│   ├── UI_UX_GUIDELINES.md
│   ├── PRIVACY_AND_SAFETY.md
│   ├── TEST_PLAN.md
│   └── DECISIONS/
│       ├── ADR-001-PYTHON-ANDROID-STACK.md
│       └── ADR-002-WELLNESS-SCORE.md
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── fonts/
│
├── app/
│   ├── main.py
│   ├── app.py
│   ├── core/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── errors.py
│   │   └── utils.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.py
│   │   └── repositories/
│   ├── integrations/
│   │   ├── location.py
│   │   └── notifications.py
│   ├── features/
│   │   ├── onboarding/
│   │   ├── home/
│   │   ├── cardio/
│   │   ├── workout/
│   │   ├── food/
│   │   ├── sleep/
│   │   ├── wellness/
│   │   ├── streak/
│   │   └── settings/
│   ├── services/
│   └── widgets/
│
├── tests/
│   ├── test_database.py
│   ├── test_streak.py
│   └── test_wellness_score.py
│
└── scripts/
    └── seed_exercises.py
```

### Aturan struktur kode

- `features/` berisi layar dan alur UI untuk setiap fitur.
- `database/` menangani koneksi, skema, dan akses SQLite.
- `repositories/` menjadi lapisan perantara antara fitur aplikasi dan database.
- `services/` berisi aturan bisnis seperti perhitungan streak dan Wellness Score, bukan kode UI.
- Jangan menaruh semua kode dalam satu file.
- Jangan membuat abstraksi berlebihan untuk fitur yang belum dibutuhkan.
- Pisahkan perhitungan Wellness Score agar bisa diuji tanpa UI.
- Pisahkan kalkulasi pace/jarak dari tampilan GPS.

---

# 11. Aturan Bisnis dan Perhitungan

## 11.1 Cardio calculations

- `duration_seconds = ended_at - started_at`
- `distance_km = distance_m / 1000`
- `pace_seconds_per_km = duration_seconds / distance_km` jika jarak > 0
- `speed_kmh = distance_km / (duration_seconds / 3600)` jika durasi > 0

Validasi:
- Jangan menghitung pace jika jarak nol/tidak valid.
- Buang atau tandai GPS point dengan akurasi sangat buruk sesuai aturan yang diuji.
- Jangan menghubungkan titik GPS yang terpisah jauh karena kehilangan sinyal tanpa penanganan.
- Tampilkan data GPS sebagai estimasi.

## 11.2 Workout calculations

Simpan data mentah set. Volume latihan dapat dihitung untuk gerakan yang menggunakan beban:

`volume = sum(weight_kg × reps)`

Jangan menerapkan rumus volume tersebut pada gerakan bodyweight tanpa menjelaskan asumsi. Untuk MVP, cukup tampilkan total set/repetisi dan riwayat beban untuk exercise yang relevan.

## 11.3 Nutrition calculations

- Total calories per day = jumlah `calories_kcal` pada tanggal lokal.
- Total protein per day = jumlah `protein_g` pada tanggal lokal.
- Data yang kosong tidak boleh dianggap nol secara diam-diam; tampilkan bahwa pencatatan belum lengkap.
- Nilai makanan adalah estimasi kecuali berasal dari sumber terverifikasi.

## 11.4 Sleep calculations

- `duration_minutes = wake_at - sleep_started_at`
- Tangani tidur lintas tengah malam dan zona waktu.
- Jangan menyimpulkan sleep quality hanya dari durasi.
- `quality_rating` adalah penilaian subjektif pengguna.

## 11.5 Streak calculations

Aturan streak harus memperhatikan:
- Jadwal aktivitas yang dipilih pengguna.
- Hari istirahat yang direncanakan.
- Aktivitas yang valid dan selesai.
- Zona waktu lokal.
- Perubahan jadwal di masa lalu.

Jangan memutus streak karena rest day yang sudah direncanakan. Jangan menghitung aktivitas yang sama berulang kali untuk menggandakan poin.

---

# 12. Keamanan, Privasi, dan Data

1. Minta izin lokasi hanya ketika pengguna menggunakan fitur GPS.
2. Jelaskan apakah lokasi direkam, disimpan lokal, atau dikirim ke server.
3. Jangan mengaktifkan background tracking tanpa penjelasan dan persetujuan.
4. Sediakan tombol berhenti dan hapus rute.
5. Jangan menampilkan rute GPS ke publik secara default.
6. Jangan menyimpan password plaintext.
7. Jangan memasukkan API key ke repository.
8. Jangan menyimpan API key atau secret di source code. Jika integrasi eksternal ditambahkan, gunakan konfigurasi yang aman dan jangan commit secret.
9. Sediakan export dan delete data.
10. Batasi data profil pada yang benar-benar diperlukan.
11. Jangan menggunakan foto tubuh untuk menilai kesehatan atau massa otot.
12. Notifikasi tidak boleh mempermalukan pengguna atau mendorong latihan berlebihan.

---

# 13. UI/UX Direction

## 13.1 Arah visual

Arah visual awal:
- Modern, bersih, dan mudah dibaca.
- Dashboard berbasis cards.
- Grafik sederhana dan tidak terlalu padat.
- Warna utama dapat dipilih setelah moodboard.
- Dark mode dan light mode dapat disediakan.
- Ikon konsisten.
- Tipografi jelas.
- Navigasi utama mudah dijangkau dengan satu tangan.

## 13.2 Referensi produk untuk studi UX

Gunakan sebagai referensi pola interaksi, bukan untuk menyalin desain:
- Strava: aktivitas cardio, peta, dan statistik.
- Hevy: pencatatan set/repetisi dan workout history.
- MyFitnessPal: food diary dan nutrisi.
- Duolingo: streak, progress, dan gamification.

## 13.3 Prinsip aksesibilitas

- Jangan mengandalkan warna saja untuk menyampaikan status.
- Gunakan label dan ikon yang jelas.
- Ukuran sentuh tombol memadai.
- Kontras teks cukup.
- Sediakan alternatif manual untuk fitur yang memakai sensor.

---

# 14. Rencana Pengembangan / Task List

Status awal semua task: `[ ] Not started`.

## Phase 0 — Project Foundation

- [x] Tetapkan nama kerja/final: FitTrack.
- [x] Tetapkan Android sebagai platform awal.
- [x] Tetapkan Python + Kivy/KivyMD sebagai stack aplikasi.
- [ ] Buat repository Git.
- [ ] Buat struktur folder aplikasi Python.
- [ ] Buat README dan `.gitignore`.
- [ ] Siapkan environment Python.
- [ ] Siapkan Buildozer dan dependensi Android.
- [ ] Buat keputusan arsitektur awal (ADR).
- [ ] Jalankan aplikasi Kivy kosong di desktop untuk pengembangan.
- [ ] Build dan jalankan APK percobaan di Android.

**Definition of Done:**
- Aplikasi Kivy minimal dapat dijalankan untuk pengembangan.
- APK percobaan dapat dibangun dan diuji di perangkat/emulator Android.
- Struktur proyek dan instruksi setup tersedia.
- Tidak ada secret di repository.

## Phase 1 — UI Foundation & Navigation

- [ ] Tentukan moodboard dan design tokens.
- [ ] Buat theme light/dark.
- [ ] Buat app shell.
- [ ] Buat navigasi Home/Cardio/Workout/Food/Sleep.
- [ ] Buat reusable card, button, input, dan chart container.
- [ ] Buat halaman Profile/Settings.
- [ ] Buat empty states dan loading states.

**Definition of Done:**
- Semua halaman utama dapat dibuka.
- Navigasi konsisten.
- Tampilan menggunakan data dummy yang diberi label jelas.

## Phase 2 — Onboarding & Local Database

- [ ] Buat onboarding.
- [ ] Buat profil pengguna.
- [ ] Buat pencatatan pengukuran opsional.
- [ ] Buat local database.
- [ ] Buat migration/schema awal.
- [ ] Buat repository untuk profil.
- [ ] Buat validasi input.
- [ ] Buat fungsi export/delete data dasar.

**Definition of Done:**
- Pengguna dapat menyelesaikan onboarding.
- Data tersimpan setelah aplikasi ditutup dan dibuka kembali.
- Pengguna dapat mengubah profil.
- Data opsional dapat dilewati.

## Phase 3 — Workout Module

- [ ] Buat exercise catalogue.
- [ ] Buat template workout.
- [ ] Tambahkan template PPL.
- [ ] Tambahkan template Upper/Lower.
- [ ] Tambahkan template Full Body.
- [ ] Tambahkan custom routine.
- [ ] Buat workout session.
- [ ] Buat pencatatan set/repetisi/beban/durasi.
- [ ] Buat riwayat workout.
- [ ] Buat detail workout.
- [ ] Buat unit tests untuk perhitungan.

**Definition of Done:**
- Pengguna dapat membuat dan menyelesaikan sesi gym/home workout.
- Data tersimpan lokal.
- Riwayat dapat dibuka kembali.

## Phase 4 — Cardio Module (Manual First)

- [ ] Buat pencatatan lari manual.
- [ ] Buat pencatatan jalan manual.
- [ ] Buat ringkasan jarak/durasi/pace.
- [ ] Buat riwayat cardio.
- [ ] Buat validasi data.

**Definition of Done:**
- Cardio dapat dicatat tanpa GPS.
- Perhitungan pace dan kecepatan lolos pengujian.

## Phase 5 — GPS Tracking

- [ ] Pilih package GPS yang aktif dipelihara.
- [ ] Periksa kebijakan Android untuk foreground/background location.
- [ ] Buat permission flow.
- [ ] Buat layar persiapan tracking.
- [ ] Buat start/pause/resume/finish.
- [ ] Simpan GPS points.
- [ ] Hitung jarak dari titik yang valid.
- [ ] Tampilkan rute di peta.
- [ ] Tangani GPS signal loss.
- [ ] Tangani aplikasi masuk background.
- [ ] Uji konsumsi baterai.
- [ ] Buat penghapusan rute.

**Definition of Done:**
- Tracking berjalan pada perangkat Android uji.
- Status tracking terlihat jelas.
- Pengguna dapat berhenti dan menghapus rute.
- Perilaku background telah diuji pada perangkat nyata, bukan hanya emulator.

## Phase 6 — Food / Nutrition

- [ ] Buat food entry manual.
- [ ] Buat meal type.
- [ ] Buat input kalori/protein estimasi.
- [ ] Buat total harian.
- [ ] Buat riwayat makanan.
- [ ] Buat favorite foods (opsional).
- [ ] Tampilkan kelengkapan pencatatan.
- [ ] Tambahkan sumber data makanan/API hanya setelah evaluasi.

**Definition of Done:**
- Pengguna dapat menambah, mengubah, dan menghapus makanan.
- Total harian dihitung dari data tanggal lokal.
- Estimasi diberi label yang benar.

## Phase 7 — Sleep Module

- [ ] Buat pengaturan jadwal tidur.
- [ ] Buat reminder tidur.
- [ ] Buat konfirmasi mulai tidur.
- [ ] Buat konfirmasi bangun.
- [ ] Buat sleep log manual.
- [ ] Buat durasi tidur.
- [ ] Buat riwayat dan grafik konsistensi.

**Definition of Done:**
- Pengguna dapat mencatat tidur secara manual.
- Notifikasi tidak otomatis menganggap pengguna sudah tidur.
- Data lintas tengah malam dihitung benar.

## Phase 8 — Streak & Gamification

- [ ] Tentukan aturan activity day.
- [ ] Tentukan aturan rest day.
- [ ] Buat current streak.
- [ ] Buat longest streak.
- [ ] Buat weekly consistency.
- [ ] Buat XP/achievement sederhana.
- [ ] Buat reminder yang dapat dimatikan.
- [ ] Uji perubahan timezone dan tanggal.

**Definition of Done:**
- Streak tidak putus karena rest day terencana.
- Aktivitas duplikat tidak menggandakan progres.
- Pengguna dapat memahami cara streak dihitung.

## Phase 9 — Wellness Score & Dashboard

- [ ] Finalisasi komponen Wellness Score.
- [ ] Finalisasi aturan minimum data.
- [ ] Buat fungsi kalkulasi terpisah dari UI.
- [ ] Buat daily summary.
- [ ] Buat weekly summary.
- [ ] Buat monthly summary.
- [ ] Buat yearly summary.
- [ ] Buat perbandingan periode.
- [ ] Buat data completeness indicator.
- [ ] Buat penjelasan perubahan skor.
- [ ] Uji kasus data kosong/tidak lengkap.

**Definition of Done:**
- Skor dapat ditelusuri ke data sumber.
- Data tidak cukup menghasilkan status yang jelas, bukan skor palsu.
- Skor tidak mengklaim diagnosis kesehatan.
- Rest day tidak diperlakukan sebagai kegagalan.

## Phase 10 — Backend & Sync (Optional after local MVP)

- [ ] Finalisasi API contract.
- [ ] Buat SQLAlchemy models.
- [ ] Buat Pydantic schemas.
- [ ] Buat authentication yang aman jika akun diperlukan.
- [ ] Buat API endpoints.
- [ ] Buat database migrations.
- [ ] Buat API client Python untuk aplikasi Android.
- [ ] Rancang conflict resolution.
- [ ] Buat sinkronisasi data.
- [ ] Buat integration tests.

**Definition of Done:**
- Data tersinkron dengan aturan konflik yang jelas.
- Token dan credential ditangani dengan aman.
- Penggunaan offline tetap masuk akal.

## Phase 11 — Quality, Release & Documentation

- [ ] Unit tests.
- [ ] Widget/UI tests.
- [ ] API tests.
- [ ] Uji perangkat Android nyata.
- [ ] Uji izin GPS ditolak.
- [ ] Uji mode offline.
- [ ] Uji data kosong.
- [ ] Uji timezone.
- [ ] Uji export/delete data.
- [ ] Perbaiki bug prioritas tinggi.
- [ ] Buat panduan pengguna.
- [ ] Buat dokumentasi instalasi.
- [ ] Buat demo dan screenshot.
- [ ] Siapkan build APK internal.

---

# 15. Testing Strategy

## 15.1 Unit testing

Uji fungsi:
- Perhitungan durasi.
- Perhitungan pace.
- Perhitungan kecepatan.
- Total kalori/protein tercatat.
- Durasi tidur lintas tengah malam.
- Streak dengan rest day.
- Wellness Score dengan data lengkap/tidak lengkap.
- Validasi input.

## 15.2 Integration testing

- Penyimpanan workout ke database.
- Penyimpanan cardio dan GPS points.
- Food entries dan agregasi harian.
- Sleep log dan summary.
- Repository lokal.
- Database lokal dan, jika backend opsional diaktifkan, API serta database server.

## 15.3 Manual testing

Uji pada perangkat Android:
- Permission lokasi diberikan/ditolak.
- GPS aktif/tidak aktif.
- Aplikasi berpindah ke background saat lari.
- Layar terkunci saat tracking.
- Aplikasi ditutup paksa.
- Baterai rendah.
- Tidak ada koneksi internet.
- Notifikasi dinonaktifkan.
- Perubahan zona waktu.

---

# 16. Risiko Teknis dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| GPS tidak akurat | Jarak dan rute meleset | Filter titik berdasarkan accuracy dan uji di perangkat nyata |
| Background tracking dibatasi OS | Tracking berhenti saat layar mati | Gunakan mekanisme foreground service yang sesuai aturan Android |
| Konsumsi baterai GPS | Baterai cepat habis | Atur interval sampling dan beri indikator tracking |
| Data nutrisi tidak akurat | Ringkasan menyesatkan | Label estimasi dan izinkan input manual |
| Skor disalahartikan sebagai diagnosis | Pengguna salah mengambil keputusan | Gunakan nama Wellness/Consistency Score dan jelaskan komponennya |
| Scope terlalu besar | Proyek tidak selesai | Implementasi bertahap dan tunda backend sync/AI |
| Konflik sinkronisasi | Data hilang/duplikat | Mulai local-first; desain sync setelah MVP stabil |
| Data lokasi sensitif | Risiko privasi | Consent, minimisasi data, kontrol hapus, tidak publik secara default |

---

# 17. Fitur yang Ditunda (Not in MVP)

Fitur berikut tidak boleh masuk sebelum fitur inti stabil:

- AI/ML untuk analisis foto tubuh.
- Estimasi massa otot dari foto.
- Social feed dan leaderboard publik.
- Integrasi banyak wearable.
- Health Connect integration.
- Sinkronisasi multi-device kompleks.
- Database makanan eksternal.
- Rekomendasi nutrisi otomatis yang kompleks.
- Coaching AI.
- Program latihan adaptif otomatis.
- Apple Health/iOS support.
- Smartwatch app.

Fitur tersebut dapat dipertimbangkan setelah MVP diuji dan kebutuhan pengguna jelas.

---

# 18. Keputusan yang Masih Terbuka

Jangan menganggap hal-hal ini sudah final:

1. Nama final aplikasi.
2. Detail versi Kivy/KivyMD dan library integrasi Android yang kompatibel.
3. Apakah backend dan akun multi-user diperlukan setelah MVP (default: tidak untuk tahap awal).
4. Penyedia peta/GPS.
5. Apakah data awal disimpan hanya lokal atau memakai akun.
6. Desain visual final dan palet warna.
7. Rumus final Wellness Score.
8. Aturan detail streak.
9. Sumber database makanan.
10. Integrasi Health Connect.
11. Batas usia dan kebijakan penggunaan aplikasi jika akan dipublikasikan.

Sebelum keputusan final, jelaskan trade-off dan minta persetujuan pemilik proyek.

---

# 19. Konvensi Pengembangan

## 19.1 Git workflow

- Satu tahap kerja per commit atau kelompok commit yang jelas.
- Gunakan pesan commit deskriptif, misalnya:
  - `chore: initialize project structure`
  - `feat: add workout session logging`
  - `feat: add manual cardio tracking`
  - `fix: handle sleep duration across midnight`
  - `test: add wellness score unit tests`
- Jangan mengubah task menjadi completed sebelum diuji.
- Jangan menimpa pekerjaan pengguna tanpa memeriksa perubahan yang sudah ada.

## 19.2 Coding conventions

- Python: PEP 8, type hints, fungsi kecil, docstring untuk logika penting.
- Python: PEP 8, type hints, formatter (misalnya Ruff), dan pytest.
- Kivy/KivyMD: jaga pemisahan tampilan dan logika aplikasi.
- Validasi input di boundary aplikasi/API.
- Tangani error secara eksplisit.
- Hindari hard-coded secret.
- Gunakan dependency yang masih dipelihara.
- Catat alasan pemilihan dependency penting.

## 19.3 Definition of Done umum

Sebuah fitur baru dianggap selesai jika:
1. Tujuan dan perilakunya sesuai dokumen.
2. Input divalidasi.
3. Error state ditangani.
4. Data tersimpan dengan benar.
5. Ada pengujian yang relevan.
6. UI memiliki loading/empty/error state bila diperlukan.
7. Dokumentasi diperbarui.
8. Pemilik proyek telah meninjau hasil tahap tersebut.

---

# 20. Prompt untuk Memulai Sesi AI / Coding Agent Baru

Salin prompt berikut saat memulai sesi baru dan lampirkan dokumen ini:

```text
Kamu bertindak sebagai software architect, product engineer, dan coding assistant untuk proyek FitTrack.

Baca PROJECT_MASTER.md secara menyeluruh sebelum menjawab atau menulis kode. Dokumen tersebut adalah sumber konteks utama proyek.

Tugasmu:
1. Pahami tujuan, ruang lingkup, teknologi, arsitektur, database, aturan bisnis, privasi, dan task list.
2. Jangan mengubah keputusan proyek tanpa menjelaskan alasan dan meminta persetujuan saya.
3. Jangan memaksakan AI/ML. Utamakan solusi sederhana yang benar-benar berguna.
4. Jangan menganggap fitur selesai tanpa implementasi dan pengujian.
5. Jangan mengarang hasil eksekusi, akses file, atau commit Git.
6. Kerjakan satu tahap pada satu waktu.
7. Sebelum coding, jelaskan tujuan tahap, file yang akan dibuat/diubah, dan cara pengujiannya.
8. Setelah tahap selesai, berikan daftar file berubah, instruksi menjalankan, hasil pengujian, keterbatasan, dan task list terbaru.
9. Setelah menyelesaikan satu tahap, berhenti dan tunggu konfirmasi saya bahwa perubahan sudah saya review dan commit ke Git sebelum melanjutkan tahap berikutnya.
10. Jika ada keputusan penting yang belum ditentukan di dokumen, tanyakan satu pertanyaan paling penting terlebih dahulu.

Mulai dengan:
- Ringkas pemahamanmu tentang FitTrack.
- Sebutkan keputusan yang masih terbuka.
- Usulkan tahap pertama yang paling tepat.
- Jangan langsung membuat seluruh aplikasi.
```

---

# 21. Status Proyek Saat Dokumen Dibuat

- [x] Konsep utama aplikasi dirumuskan.
- [x] Modul utama diidentifikasi.
- [x] Kebutuhan streak dan Wellness Score dimasukkan.
- [x] Rancangan awal database dibuat.
- [x] Rekomendasi arsitektur dibuat.
- [x] Struktur folder dirancang.
- [x] Task list pengembangan dibuat.
- [ ] Nama final disetujui.
- [ ] Stack teknologi disetujui.
- [ ] Desain UI final disetujui.
- [ ] Implementasi dimulai.

**Status:** Perencanaan / specification draft. Belum ada klaim bahwa aplikasi sudah dibuat.

---

## Catatan penutup

Bangun FitTrack sebagai produk yang bisa selesai dan diuji, bukan sebagai kumpulan fitur sebanyak mungkin. Prioritaskan pencatatan workout, cardio, sleep, food, lalu dashboard dan streak. GPS background tracking serta sinkronisasi server adalah pekerjaan yang lebih kompleks dan sebaiknya dikerjakan setelah fondasi aplikasi stabil.
