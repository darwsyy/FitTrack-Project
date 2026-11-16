# FitTrack - Database Design

## Penyimpanan MVP

FitTrack menggunakan SQLite lokal dengan pendekatan offline-first. Database disimpan di direktori privat aplikasi (\`App.user_data_dir\`) pada perangkat Android. Untuk pengujian, lokasi database dapat diberikan secara eksplisit.

Koneksi mengaktifkan foreign key dan transaksi. Perubahan skema dikelola melalui tabel \`schema_migrations\`; jangan mengubah migration yang sudah dipakai, tambahkan nomor migration baru untuk perubahan berikutnya.

## Skema versi 1 - Profil

| Tabel | Fungsi |
|---|---|
| \`schema_migrations\` | Mencatat versi skema yang sudah diterapkan. |
| \`users\` | Satu profil lokal dan nama tampilan pengguna. |
| \`user_profiles\` | Preferensi pengalaman dan jenis latihan. |
| \`body_measurements\` | Riwayat tinggi/berat yang opsional. |
| \`user_settings\` | Preferensi aplikasi dasar. |

## Skema versi 2 - Workout

| Tabel | Fungsi |
|---|---|
| \`exercises\` | Katalog exercise bawaan dengan kategori, equipment, mode latihan, dan instruksi singkat. |
| \`workout_templates\` | Template bawaan dan custom routine milik pengguna. |
| \`template_exercises\` | Urutan exercise dalam template. |
| \`workout_sessions\` | Sesi workout, mode gym/home, waktu mulai/selesai, catatan, dan status. |
| \`workout_session_exercises\` | Exercise yang dipakai pada sesi tertentu. |
| \`workout_sets\` | Set dengan repetisi, beban opsional, durasi, atau jarak. |

### Aturan workout

- Katalog dan template bawaan di-seed secara idempotent; menjalankan seed berulang tidak menggandakan data.
- Template gym dan home dipisahkan agar daftar exercise sesuai peralatan yang tersedia.
- Template PPL, Upper/Lower, Full Body, dan template home disediakan sebagai pilihan, bukan kewajiban.
- Custom routine minimal memiliki nama dan satu exercise, serta terikat ke profil pemiliknya.
- Custom routine hanya terlihat untuk profil pemilik; menghapus profil ikut menghapus custom routine.
- Sesi harus terkait dengan profil lokal.
- Hanya satu sesi berstatus aktif yang diizinkan; sesi aktif dipulihkan saat halaman Workout dibuka kembali.
- Exercise gym-only tidak dapat ditambahkan ke sesi home workout, dan sebaliknya.
- Set dapat dicatat berdasarkan repetisi atau durasi; beban bersifat opsional dan tidak wajib untuk bodyweight.
- Nilai repetisi/durasi/jarak harus positif; beban tidak boleh negatif.
- Sesi hanya dapat diakhiri setelah minimal satu set selesai dicatat.
- Exercise dan set yang menjadi bagian sesi tidak dapat ditambahkan setelah sesi selesai.
- Menghapus profil menghapus sesi, exercise sesi, dan set terkait melalui foreign key cascade.
- Katalog exercise dan template bawaan tetap tersedia setelah data pengguna dihapus.

## Migrasi versi 3 - Perbaikan kompatibilitas Workout

- Menambahkan kolom `user_id` pada `workout_templates` untuk database lama yang sudah mencatat migration v2 tetapi belum memiliki kolom tersebut.
- Migration memeriksa kolom yang tersedia terlebih dahulu, sehingga aman untuk database baru yang sudah memiliki `user_id`.
- Data template dan profil yang sudah ada tetap dipertahankan.

## Aturan data umum

- Primary key menggunakan UUID string.
- Timestamp disimpan dalam ISO 8601 UTC.
- Tinggi disimpan dalam cm dan berat dalam kg.
- Pengukuran bersifat opsional; tidak adanya data bukan berarti nilai nol.
- Pengukuran baru hanya ditambahkan jika nilainya berubah dari catatan terakhir.
- Jika hanya satu nilai pengukuran diperbarui, nilai terakhir untuk pengukuran lainnya tetap dipertahankan.
- Penghapusan user menggunakan foreign key cascade untuk menghapus data terkait.
- Ekspor JSON menyertakan seluruh tabel data dan versi skema.
- Jangan menyimpan data kesehatan atau lokasi yang tidak diperlukan.

## Lokasi database

- Android: direktori privat aplikasi dari \`App.user_data_dir\`.
- Pengujian: file sementara dari pytest.
- Desktop preview: direktori data Kivy pengguna jika tidak ada path khusus.
