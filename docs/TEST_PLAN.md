# FitTrack — Test Plan

## Phase 1: UI Foundation & Navigation

- [x] App shell dapat dibangun.
- [x] Lima halaman utama terdaftar pada ScreenManager.
- [x] Profile dan Settings dapat dibuka.
- [x] Navigasi mengubah halaman aktif.
- [x] Tema light/dark dapat ditukar tanpa mengganti root atau ScreenManager.
- [x] Komponen reusable dapat dibuat.
- [ ] Verifikasi manual semua menu dan pergantian tema.
- [ ] Uji desktop preview pada beberapa lebar.
- [ ] Uji APK pada HP Android.

## Phase 2: Onboarding & Local Database

- [x] Migration awal membuat tabel dan dapat dijalankan ulang tanpa menggandakan skema.
- [x] Profil lokal dapat dibuat, dibaca, dan diperbarui.
- [x] Pengukuran tinggi/berat dapat dilewati.
- [x] Input tidak valid ditolak dengan pesan yang jelas.
- [x] Profil disimpan dalam file SQLite dan dapat dibaca kembali.
- [x] Ekspor JSON berisi data lokal.
- [x] Penghapusan data menghapus data pengguna dan mempertahankan versi skema.
- [x] Onboarding mengarahkan pengguna ke Home setelah profil disimpan.
- [ ] Verifikasi manual alur onboarding, edit profil, ekspor, dan hapus data.
- [ ] Uji penyimpanan pada APK/perangkat Android.

## Pengujian otomatis

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Desktop preview

Jalankan `python -m app.main`. Pada Windows/Linux/macOS, jendela preview dibuat portrait 390 x 844 px. Ubah ukuran jendela untuk memeriksa responsivitas.

## Pengujian manual Phase 2

1. Jalankan aplikasi dengan database baru.
2. Pastikan layar Onboarding muncul.
3. Isi nama tampilan saja, lalu simpan.
4. Pastikan Home terbuka.
5. Buka Profil, ubah nama, lalu simpan.
6. Tutup dan jalankan ulang aplikasi; profil harus tetap tersedia.
7. Coba isi pengukuran opsional dan ekspor JSON.
8. Uji penghapusan: ketukan pertama hanya meminta konfirmasi, ketukan kedua menghapus data dan membuka Onboarding.

## Pengujian Android

Setelah APK dibuat, uji pada HP nyata: ukuran layar, density, area status/navigation bar, keyboard, sentuhan, rotasi bila didukung, serta navigasi sistem Android. Ekspor JSON masih berada di direktori privat aplikasi pada tahap ini.
