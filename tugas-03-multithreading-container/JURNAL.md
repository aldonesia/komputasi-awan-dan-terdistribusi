# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 18
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Karena beberapa thread mengakses dan memodifikasi variabel `processed_count` secara bersamaan tanpa sinkronisasi, menyebabkan beberapa operasi penambahan diabaikan.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: Tidak ada

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 6 okt 2026 | Gemini | Cara menggunakan isi konfigurasi docker | Menggunakan base image, Menentukan direktori kerja di dalam container, Menyalin file package dan menginstall dependensi, Menyalin seluruh kode sumber aplikasi, Perintah untuk menjalankan aplikasi
| ... |
