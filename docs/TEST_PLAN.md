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

## Pengujian otomatis

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Desktop preview

Jalankan `python -m app.main`. Pada Windows/Linux/macOS, jendela preview dibuat portrait 390 x 844 px. Ubah ukuran jendela untuk memeriksa responsivitas.

## Pengujian manual di desktop

1. Buka Home dan semua menu utama.
2. Buka Profile lalu Settings.
3. Tekan tombol tema beberapa kali.
4. Pastikan halaman Settings tetap aktif dan tombol navigasi masih berfungsi.
5. Ubah ukuran jendela menjadi sempit dan lebar.
6. Pastikan dashboard dapat discroll dan teks tidak terpotong.

## Pengujian Android

Setelah APK dibuat, uji pada HP nyata: ukuran layar, density, area status/navigation bar, keyboard, sentuhan, rotasi bila didukung, serta navigasi sistem Android.
