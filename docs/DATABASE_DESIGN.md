# FitTrack — Database Design

## Penyimpanan MVP

FitTrack menggunakan SQLite lokal dengan pendekatan offline-first. Database disimpan di direktori privat aplikasi (`App.user_data_dir`) pada perangkat Android. Untuk pengujian, lokasi database dapat diberikan secara eksplisit.

Koneksi mengaktifkan foreign key dan transaksi. Perubahan skema dikelola melalui tabel `schema_migrations`; jangan mengubah migration yang sudah dipakai, tambahkan nomor migration baru untuk perubahan berikutnya.

## Skema awal — versi 1

| Tabel | Fungsi |
|---|---|
| `schema_migrations` | Mencatat versi skema yang sudah diterapkan. |
| `users` | Satu profil lokal dan nama tampilan pengguna. |
| `user_profiles` | Preferensi pengalaman dan jenis latihan. |
| `body_measurements` | Riwayat tinggi/berat yang opsional. |
| `user_settings` | Preferensi aplikasi dasar. |

## Aturan data

- Primary key menggunakan UUID string.
- Timestamp disimpan dalam ISO 8601 UTC.
- Tinggi disimpan dalam cm dan berat dalam kg.
- Pengukuran bersifat opsional; tidak adanya data bukan berarti nilai nol.
- Pengukuran baru hanya ditambahkan jika nilainya berubah dari catatan terakhir.
- Jika hanya satu nilai pengukuran diperbarui, nilai terakhir untuk pengukuran lainnya tetap dipertahankan.
- Penghapusan user menggunakan foreign key cascade untuk menghapus data terkait.
- Ekspor JSON menyertakan tabel data pengguna dan versi skema.
- Jangan menyimpan data kesehatan atau lokasi yang tidak diperlukan.

## Lokasi database

- Android: direktori privat aplikasi dari `App.user_data_dir`.
- Pengujian: file sementara dari pytest.
- Desktop preview: direktori data Kivy pengguna jika tidak ada path khusus.
