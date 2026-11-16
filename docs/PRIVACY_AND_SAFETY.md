# FitTrack — Privacy & Safety

## Data yang dikumpulkan pada Phase 2

- Nama tampilan (wajib untuk membuat profil lokal).
- Preferensi pengalaman olahraga dan jenis latihan.
- Tinggi dan berat badan (opsional, hanya jika pengguna mengisinya).

FitTrack tidak meminta tanggal lahir, foto tubuh, alamat, atau data akun online pada tahap ini.

## Prinsip penggunaan data

- Tinggi dan berat hanya disimpan sebagai catatan yang dimasukkan pengguna.
- Data tersebut tidak digunakan untuk memberi label tubuh, menentukan nilai kesehatan, atau membuat target diet.
- Tidak mengisi data opsional tidak mengurangi fungsi inti aplikasi.
- Database berada di penyimpanan privat aplikasi pada perangkat.
- Tidak ada pengiriman data profil ke server pada MVP.

## Ekspor dan penghapusan

- Pengguna dapat membuat ekspor JSON dari halaman Profil.
- File ekspor pada implementasi awal disimpan di direktori privat aplikasi. Alur berbagi/menyalin ke penyimpanan umum akan ditambahkan setelah integrasi Android diuji.
- Penghapusan memerlukan konfirmasi kedua dan menghapus seluruh baris milik pengguna, tetapi mempertahankan tabel migration agar aplikasi tetap dapat berjalan.
