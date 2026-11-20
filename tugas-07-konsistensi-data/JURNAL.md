# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
1. Data harus tetap sesuai dengan transaksi terakhir yang dilakukan pengguna.
2. Proses pengiriman data dari satu server ke server lain membutuhkan waktu, sehingga terkadang data yang muncul belum diperbarui.
3. Eventual Consistency digunakan agar data di setiap server bisa diperbarui secara bertahap.
4. Read-Your-Writes digunakan supaya pengguna tetap bisa melihat data terbaru setelah melakukan perubahan.
- Kesimpulan akhir & alasan: Model yang dipilih adalah Eventual Consistency dengan tambahan Read-Your-Writes. Alasannya, proses replikasi data tidak harus langsung selesai, tetapi pengguna tetap bisa melihat data terbaru setelah melakukan transaksi. Jadi, sistem tetap bisa berjalan dengan baik tanpa harus menunggu semua server selesai memperbarui data.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: 
1. hasil skenario naif
Saat pengguna melakukan top-up sebesar Rp50.000 di server Jakarta, kemudian langsung mengecek saldo melalui server Bandung, saldo yang muncul masih 0. Hal ini terjadi karena data dari Jakarta belum selesai dikirim ke Bandung. Proses replikasi membutuhkan waktu sekitar 2 detik.
2. hasil read-your-writes
Pada skenario kedua, pengguna melakukan top-up sebesar Rp20.000 sehingga saldo menjadi Rp70.000. Ketika pengguna langsung mengecek saldo melalui Bandung, sistem mengetahui bahwa data di Bandung belum diperbarui. Karena itu, sistem mengarahkan pembacaan ke Jakarta agar saldo yang ditampilkan tetap benar.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|18-11-2026|ChatGPT|Meminta ide mengenai perbedaan Eventual Consistency dan Read-Your-Writes.|Memberikan gambaran mengenai fungsi kedua model konsistensi dan contoh penerapannya|Menggunakan ide tersebut sebagai bahan pertimbangan dan memahami konsep sebelum mengerjakan tugas.|
| ... | ... | ... | ... | ... |
