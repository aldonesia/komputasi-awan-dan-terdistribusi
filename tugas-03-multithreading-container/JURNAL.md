# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat = 100
- Kenapa bisa meleset = terjadi race condition karena beberapa thread mengubah `processed_count` secara bersamaan. Tapi pas saya coba hasilnya masih 100 jadi race condition belum kelihatan di percobaan bagian ini

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan = masih tetap 100

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya = pas saat menggunakan Docker, yang perlu diperhatikan adalah posisi file dan cara menjalankan program Python dari dalam container dan setelah itu Dockerfile disesuaikan, program bisa dijalankan di dalam container.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal    | Tool AI | Prompt yang diberikan                                                                                                                                                                                                                                                                                                         | Ringkasan saran/ide AI                                                                                                                                                                                                      | Bagaimana diolah jadi tulisan/kode sendiri                                                                                       |
| ---------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 06 10 2026 | Gemini Ai | Saya tes simulasi multithreading pada sistem pemrosesan pesanan. Saya ingin memahami kenapa penggunaan beberapa thread pada variabel yang sama bisa menyebabkan race condition, serta bagaimana lock dapat mencegah masalah tersebut. Tolong jelaskan konsepnya secara sederhana tanpa memberikan kodenya | dijelaskan race condition dapat terjadi ketika beberapa thread mengakses dan mengubah data yang sama secara bersamaan. Lock digunakan agar bagian tertentu hanya bisa diakses oleh satu thread pada satu waktu. | Penjelasan tersebut saya gunakan untuk memahami konsep race condition dan Lock sebelum melakukan percobaan sendiri pada program. |
