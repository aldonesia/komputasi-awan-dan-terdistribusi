# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat:

| Platform | Hasil
|---|---|
| Python | 42, 40, 41 |
| Docker | 56, 53, 55 | 

- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): 

  - Meskipun 100 pesanan sudah diproses, counter hanya mencatat sekitar 40-56 karena sebagian penambahan saling menimpa saat dikerjakan oleh banyak thread secara bersamaan. `Jeda time.sleep(0.0005)` ditambahkan agar kejadian ini lebih mudah untuk dilihat.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan:

| Platform | Hasil
|---|---|
| Python | 100, 100, 100 |
| Docker | 100, 100, 100 | 

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: 

- Kendala: Muncul line bahwa docker tidak dapat dikenali
  - Penyebab: Docker belum terpasang di laptop.
  - Solusi: Memasang Docker Desktop dan menjalankannya.


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 06 / 10 / 2026 | Claude AI | Saya mengerjakan praktikum tentang race condition pada program Python multithreading. Ada variabel bersama processed_count yang diakses oleh banyak thread untuk memproses 100 pesanan, dengan time.sleep(0.0005) sengaja ditambahkan agar race condition mudah terlihat. Saya menjalankannya di dua platform (Python langsung dan Docker), masing-masing 3 kali, dalam dua kondisi: tanpa lock dan dengan lock. | Race condition terjadi karena operasi processed_count += 1 bukan operasi atomik, melainkan terdiri dari tiga langkah (membaca, menambah, menulis), sehingga ketika beberapa thread membaca nilai yang sama sebelum ada yang menulis, penambahan satu thread tertimpa thread lain dan hasilnya meleset dari 100 (sekitar 40-56). Jeda time.sleep(0.0005) sengaja memperlebar celah antara membaca dan menulis agar kejadian ini mudah terlihat, dan perbedaan angka antara Python lokal dan Docker wajar karena hasilnya tidak deterministik, bergantung pada penjadwalan thread dan beban sistem, sehingga tidak bisa disimpulkan satu platform lebih baik. Dengan threading.Lock, bagian kritis hanya dijalankan satu thread pada satu waktu sehingga hasilnya selalu 100, dan kendala Docker (perintah docker tidak dikenali) disebabkan Docker belum terpasang, yang diselesaikan dengan memasang Docker Desktop, menjalankannya, lalu memverifikasi dengan docker --version.| Kelihatannya processed_count += 1 cuma satu baris, tapi sebenarnya Python mengerjakannya dalam tiga tahap. Di sela-sela tahap itu, thread lain bisa ikut masuk |
