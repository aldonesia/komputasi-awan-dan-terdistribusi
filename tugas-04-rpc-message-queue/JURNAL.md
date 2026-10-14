# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- RPC, alasan: RPC, karena hanya seperti memanggil local func biasa. Untuk Setup nya pun tidak sulit. tidak perlu menjalankan docker, install broker, dll

## Kendala teknis
- Error Connection Refused : Klien gagal terhubung karena server.pybelum dijalankan atau port di klien dan server lain.

Solusi : Pastikan server.pysudah jalan duluan sebelum client.pydijalankan.

- Error Port Sudah Digunakan : Server gagal jalan karena port 8000 lagi dipakai aplikasi lain.

Solusi : Ganti port di server.pydan client.pyke port lain (misal: 8001), atau matikan aplikasi yang pakai port 8000.

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
