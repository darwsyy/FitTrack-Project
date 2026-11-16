# FitTrack - Test Plan

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
- [x] Verifikasi manual alur onboarding, edit profil, ekspor, dan hapus data.
- [ ] Uji penyimpanan pada APK/perangkat Android.

## Phase 3: Workout Module

### Automated tests

- [x] Migration v2 membuat tabel workout dan dapat dijalankan berulang.
- [x] Katalog exercise dan template bawaan di-seed tanpa duplikasi.
- [x] Template gym/home menampilkan pilihan exercise yang sesuai.
- [x] Custom routine membutuhkan nama dan minimal satu exercise.
- [x] Sesi dari template menyimpan exercise secara berurutan.
- [x] Sesi kosong dapat ditambah exercise.
- [x] Set repetisi/beban dan set durasi dapat disimpan.
- [x] Input set tidak valid ditolak.
- [x] Sesi tanpa set selesai tidak dapat diakhiri.
- [x] Sesi selesai tidak dapat diubah lagi.
- [x] Hanya satu sesi aktif yang diizinkan dan sesi aktif dapat dipulihkan.
- [x] Exercise gym-only ditolak pada sesi home dan sebaliknya.
- [x] Custom routine terikat ke profil pemilik dan ikut terhapus bersama profil.
- [x] Riwayat dan detail sesi dapat dibaca.
- [x] Penghapusan profil menghapus sesi workout terkait.
- [x] UI dapat memulai sesi, mencatat set, menyelesaikan sesi, dan membuat custom routine.

### Manual verification required

- [ ] Periksa layout Workout pada desktop portrait.
- [ ] Coba mode Gym dan Home workout.
- [ ] Mulai sesi dari template dan sesi kosong.
- [ ] Tambah exercise dan catat beberapa set.
- [ ] Coba gerakan berbasis durasi seperti plank.
- [ ] Coba validasi saat input kosong/tidak valid.
- [ ] Akhiri sesi dan buka detail riwayat.
- [ ] Buat custom routine lalu mulai sesi dari template tersebut.
- [ ] Tutup dan buka aplikasi; pastikan riwayat tetap tersimpan.
- [ ] Uji APK pada perangkat Android setelah packaging tersedia.

## Menjalankan pengujian otomatis

\`\`\`powershell
.\\.venv\\Scripts\\python.exe -m pytest -q
\`\`\`

## Desktop preview

Jalankan \`python -m app.main\`. Pada Windows/Linux/macOS, jendela preview dibuat portrait 390 x 844 px. Ubah ukuran jendela untuk memeriksa responsivitas.

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
