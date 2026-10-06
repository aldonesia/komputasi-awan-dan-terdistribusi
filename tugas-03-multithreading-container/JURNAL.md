# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
Race condition dibuat untuk membaca counter sebelum `Barrier.wait()`.
Setelah seluruh thread membaca nilai 0, semuanya menulis nilai 1. Hasil pengujian
lokal 100 pesanan menunjukkan 100 worker selesai tetapi counter hanya 1;
sebanyak 99 update hilang.
## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: ...

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
