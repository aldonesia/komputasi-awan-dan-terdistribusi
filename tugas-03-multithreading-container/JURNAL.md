# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
Race condition dibuat untuk membaca counter sebelum `Barrier.wait()`.
Setelah seluruh thread membaca nilai 0, semuanya menulis nilai 1. Hasil pengujian
lokal 100 pesanan menunjukkan 100 worker selesai tetapi counter hanya 1;
sebanyak 99 update hilang.
## Percobaan dengan Lock
Setelah menggunakan threading.Lock(), nilai processed_count menjadi 100, sesuai dengan jumlah pesanan. Lock membuat thread bergantian memperbarui counter sehingga tidak saling menimpa hasil penambahan. Pada percobaan di dalam Docker, tidak ada penambahan counter yang hilang dan hasilnya sesuai harapan.

## Kendala Docker
- Error disaat instalasi docker desktop (human error), namun saat mencoba build dan run, tidak ada kendala sama sekali

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 6 Oktober 2026 | ChatGPT | Jelaskan langkah pengerjaan untuk pemula. | Menjelaskan pengujian Python, Docker, penyimpanan bukti, dan push ke GitHub. | Panduan digunakan untuk menjalankan program dan menyiapkan bukti. |
| 6 Oktober 2026 | ChatGPT | Mengapa hasil tanpa lock berbeda setiap run? | Menjelaskan penjadwalan thread dan pembaruan counter yang saling tertimpa. | Penjelasan digunakan untuk memahami hasil pengujian. |
| ... | ... | ... | ... | ... |
