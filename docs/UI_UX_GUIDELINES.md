# FitTrack — UI/UX Guidelines

## 1. Arah desain

- Mobile-first: target utama adalah Android, bukan desktop.
- Bahasa antarmuka MVP: Indonesia.
- Gaya: modern, bersih, tenang, dan mudah dibaca.
- Navigasi utama berada di bagian bawah agar mudah dijangkau.
- Informasi disusun dalam kartu ringkas; halaman panjang memakai ScrollView.

## 2. Ukuran dan responsivitas

- Desktop preview diatur ke jendela portrait 390 x 844 px agar mendekati bentuk layar ponsel.
- Ukuran preview desktop hanya simulasi; bukan bukti bahwa APK sudah cocok di semua HP.
- Android menggunakan ukuran density-independent (dp) untuk layout dan scale-independent (sp) untuk teks.
- Hindari posisi dan ukuran absolut untuk konten utama; gunakan BoxLayout, GridLayout, size_hint, dan ScrollView.
- Lebar minimum desktop preview: 320 px; tinggi minimum: 560 px.
- Target uji manual: lebar 320, 360, 390, dan 430 dp; portrait terlebih dahulu.
- Periksa label panjang, tombol navigasi, keyboard, area sentuh, dan konten yang perlu discroll.

## 3. Design tokens

Warna disimpan pada `app/widgets/components.py` dalam `PALETTES`.

| Token | Light | Dark |
|---|---|---|
| Background | #F5F7FA | #12171F |
| Surface | #FFFFFF | #1F262F |
| Text | #1A242F | #EDF2F7 |
| Muted | #66737F | #A6B0BD |
| Accent | #1F7A63 | #33A889 |
| Border | #E0E5EB | #38424F |

- Spacing utama: kelipatan 4 dp.
- Radius kartu: 14 dp.
- Tinggi tombol: 46 dp.
- Ukuran teks isi: 12–14 sp; judul halaman: 21 sp.

## 4. Navigasi dan tema

- Menu utama: Home, Cardio, Workout, Food, Sleep.
- Profile diakses dari tombol pada header.
- Settings dapat dibuka dari Profile.
- Navigasi menggunakan ScreenManager tanpa membangun ulang root widget.
- Pergantian tema memperbarui warna widget yang sedang tampil dan mempertahankan halaman aktif.
- Tema belum disimpan permanen; penyimpanan preferensi masuk tahap settings/persistence berikutnya.

## 5. States dan komponen

- Empty state menjelaskan mengapa konten belum ada.
- Loading state digunakan untuk proses yang membutuhkan waktu.
- Kartu, tombol, input, dan chart container dibuat reusable.
- Grafik hanya ditampilkan ketika data aktual tersedia.

## 6. Batasan pengujian

- Data dashboard adalah placeholder, bukan data pengguna.
- Pengujian desktop portrait tidak menggantikan pengujian APK pada HP Android.
- Android perlu diuji untuk sentuhan, keyboard, status/navigation bars, izin, dan ukuran layar nyata.
- Belum ada klaim kompatibilitas untuk semua resolusi atau versi Android.
