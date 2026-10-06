# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 38
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Meskipun perintah processed_count += 1 terlihat seperti satu tindakan saja, tapi sebenarnya di balik layar komputer ia sedang mengerjakannya dalam tiga langkah terpisah, yaitu : membaca nilai saat ini dari memori, menambahkannya dengan angka satu, lalu menyimpannya kembali. Nah, masalah ini muncul ketika sistem menjalankan banyak thread secara bersamaan, yang membuat langkah-langkah tersebut menjadi rentan untuk bertabrakan. Kurang lebih bayangannya sepert ini, Thread A dan Thread B membaca angka 10 di sepersekian detik yang sama, keduanya akan memproses hitungan masing-masing dan sama-sama menyimpan angka 11 kembali ke memori. Jadi, satu hitungannya hilang karena saling menimpa, padahal seharusnya nilainya bertambah dua kali menjadi 12. Karena puluhan thread ini terus-menerus berbalapan membaca dan menulis tanpa adanya antrean yang teratur, banyak proses pembaruan data yang menguap begitu saja, sehingga wajar saja jika hasil akhirnya meleset jauh dari target 100 dan hanya tercatat sebanyak 38.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100
- Nah hasil penghitungannya ini bisa kembali akurat ke angka 100 itu karena penggunaan metode Lock dari library threading yang bertindak layaknya kunci pintu pelindung untuk area kode yang sensitif. Sederhananya, ketika sebuah thread ingin memperbarui data, ia diwajibkan untuk mengambil kunci tersebut terlebih dahulu, jika kuncinya kebetulan sedang dipakai oleh thread lain, ia harus sabar menunggu dan mengantre di luar. Dengan adanya sistem penjagaan ini, thread yang memegang kunci bisa dengan tenang menyelesaikan tiga tahapan prosesnya, yaitu : membaca, menambah, dan menyimpan nilai—tanpa perlu khawatir diserobot atau diganggu oleh proses lain, untuk kemudian melepaskan kuncinya setelah selesai. Mekanisme inilah yang memaksa pembaruan data berjalan rapi satu per satu secara berurutan di titik kritisnya, sehingga efektif mencegah insiden data yang saling menimpa dan memastikan seratus thread yang berjalan berhasil mencatat angka tambahannya dengan sempurna.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: kendala dalam pengerjaan proyek kami adalah, kami sempat mengalami "failed to build: failed to solve: python:__ISI_VERSI__-slim: failed to resolve source metadata for docker.io/library/python:__ISI_VERSI__-slim: docker.io/library/python:__ISI_VERSI__-slim: not found", dan solusi nya adalah dengan menambahkan kode versi python komputer lokal yaitu 3.10-slim

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 05/10/26 | Gemini | Berikan struktur logika atau kode pembagian tugas multithreading, dengan pembagian 100 pesanan dengan 10 item | Menyarankan konsep pembagian batch (*chunking*) berbasis *step size* menggunakan `range(0, NUM_ORDERS, chunk_size)` untuk mengiris list ID pesanan ke tiap thread. | Mengubah pendekatan *step size* menjadi iterasi berbasis indeks worker `range(NUM_WORKERS)` dengan formula eksplisit `start` dan `end` (`start = i * NUM_ORDERS // NUM_WORKERS`, `end = (i + 1) * ...`) agar pembagian list terikat langsung pada ID tiap worker. |
