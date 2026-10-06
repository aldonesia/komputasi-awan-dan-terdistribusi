# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 1 dari 100 pesanan.
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Pada percobaan pertama, `processed_count` diubah menggunakan `processed_count += 1` tanpa menggunakan Lock. Karena program menjalankan beberapa thread secara bersamaan, setiap thread dapat mengakses dan mengubah variabel `processed_count` pada waktu yang hampir bersamaan. Beberapa thread dapat membaca nilai counter yang sama sebelum thread lain selesai memperbaruinya. Ketika nilai tersebut kemudian ditambahkan dan disimpan kembali, perubahan dari thread lain dapat tertimpa. Hal ini menyebabkan beberapa proses penambahan tidak tercatat dan hasil akhirnya menjadi 1, padahal terdapat 100 pesanan yang harus diproses. Kondisi tersebut menunjukkan terjadinya race condition pada variabel bersama.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 dari 100 pesanan.
- Setelah menggunakan `with lock:`, proses perubahan nilai `processed_count` dilindungi oleh Lock. Dengan begitu, hanya satu thread yang dapat melakukan proses increment pada satu waktu, sehingga perubahan nilai counter tidak saling tertimpa. Hasil akhirnya menjadi sesuai dengan jumlah pesanan yang diproses, yaitu 100 dari 100 pesanan.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |

3 dan 4 |07-10-2026|ChatGPT|Saya sedang mengerjakan Tugas 3 tentang multithreading Python. Saya minta bantuan untuk mengisi bagian TODO, memahami race condition dan penggunaan Lock, serta cara menjalankan program menggunakan Docker Tolong jelaskan langkahnya satu per satu karena saya masih belajar.|AI menjelaskan cara menggunakan threading.Lock(), membuat worker dengan beberapa thread, menjelaskan penyebab race condition, dan membantu mengisi bagian Dockerfile serta menjalankan Docker.|diolah nya seperti yang ada pada tugas|
1 dan 2 |07-10-2026 |ChatGPT | Saya sedang mengerjakan Tugas 3 tentang multithreading Python. Tolong jelaskan langkah pengerjaan TODO 1, TODO 2, dan TODO 3 serta jelaskan juga kenapa bisa terjadi race condition | AI menjelaskan cara menggunakan threading.Lock(), cara kerja race condition, dan cara membuat beberapa thread untuk memproses pesanan. | Saya memahami penjelasannya lalu menerapkannya ke kode yang sudah diberikan dosen. Saya menyesuaikan kode sendiri, menjalankan program tanpa Lock untuk melihat race condition, kemudian menambahkan Lock dan membandingkan hasilnya. |
p