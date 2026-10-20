# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: ...

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: Pada percobaan pertama, sempat terjadi race condition di mana semua node mendeklarasikan dirinya sebagai leader secara bersamaan. Hal ini terjadi karena jeda waktu bawaan time.sleep(1) terlalu singkat untuk menyalakan 5 terminal secara manual. Node yang menyala lebih awal mengira node lain yang lebih tinggi sudah mati karena terminalnya belum sempat dijalankan. Masalah ini diselesaikan dengan memperpanjang waktu tunggu menjadi time.sleep(15) di fungsi main(), sehingga semua node bisa menyala bersamaan dan algoritma Bully berhasil memilih Node 5

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4
- Berapa lama waktu sampai leader baru terdeteksi: Berdasarkan interval sleep di fungsi monitor, biasanya ini memakan waktu sekitar 3 detik setelah Node 5 dimatikan, saat fungsi ping pertama kali mendeteksi kegagalan koneksi dan mengembalikan nilai False

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
