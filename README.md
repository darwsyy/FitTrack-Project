# FitTrack

FitTrack adalah aplikasi Android berbasis Python untuk mencatat aktivitas olahraga dan kebiasaan harian. Tahap pengembangan awal menggunakan Kivy dan dijalankan di desktop Windows untuk memudahkan pembuatan serta pengujian.

## Status

- Fondasi Python: disiapkan dengan Python 3.14.
- UI: Kivy.
- Database MVP: SQLite bawaan Python dengan migration versi 2.
- Onboarding dan profil lokal: tersedia.
- Workout: katalog exercise, template gym/home, custom routine, sesi latihan, pencatatan set, dan riwayat lokal tersedia untuk verifikasi manual.
- Ekspor data: JSON ke direktori privat aplikasi.
- Android packaging: belum diuji; Buildozer akan dikonfigurasi pada lingkungan Linux/WSL2 setelah aplikasi desktop stabil.
- Cardio GPS, Food, dan Sleep: belum diimplementasikan.

## Persyaratan

- Windows 10/11 64-bit untuk pengembangan desktop.
- Python 3.14.
- Git.

## Setup lingkungan

Buka PowerShell dari direktori proyek:

\`\`\`powershell
py -3.14 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
\`\`\`

Jika PowerShell memblokir aktivasi virtual environment, jalankan interpreter langsung:

\`\`\`powershell
.\\.venv\\Scripts\\python.exe -m pip install -r requirements-dev.txt
\`\`\`

## Menjalankan aplikasi

Dari direktori utama proyek:

\`\`\`powershell
python -m app.main
\`\`\`

Atau tanpa aktivasi virtual environment:

\`\`\`powershell
.\\.venv\\Scripts\\python.exe -m app.main
\`\`\`

## Menjalankan pengujian

\`\`\`powershell
.\\.venv\\Scripts\\python.exe -m pytest -q
\`\`\`

## Struktur utama

- app/main.py: entry point untuk menjalankan aplikasi.
- app/app.py: kelas aplikasi Kivy, navigasi, onboarding, profil, dan antarmuka workout.
- app/database/: koneksi SQLite, migration, dan repository.
- app/database/repositories/profile_repository.py: operasi profil lokal.
- app/database/repositories/workout_repository.py: katalog exercise, template, sesi, set, dan riwayat workout.
- app/features/onboarding/: validasi input onboarding/profil.
- app/services/data_manager.py: ekspor dan penghapusan data lokal.
- tests/: pengujian otomatis.
- docs/: dokumentasi desain, database, privasi, dan pengujian.
- FitTrack_PROJECT_MASTER.md: spesifikasi induk proyek.

## Catatan

KivyMD, Plyer, SQLAlchemy, dan Buildozer belum menjadi dependensi tahap ini. KivyMD dan SQLAlchemy bersifat opsional; Plyer akan dievaluasi ketika integrasi fitur perangkat diperlukan. Buildozer membutuhkan lingkungan Linux untuk proses build Android.
