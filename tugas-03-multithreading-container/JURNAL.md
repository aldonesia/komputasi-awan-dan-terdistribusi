# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 10 dari 100 pesanan
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Karena tiap thread membaca nilai saat ini, menambahkannya, lalu menulis kembali. Jika beberapa thread membaca nilai yang sama sebelum salah satunya sempat menulis, mereka bisa menimpa hasil satu sama lain sehingga beberapa pesanan tidak terhitung. karena itu nilainya bisa meleset. Lock mencegahnya dengan memastikan hanya satu thread pada satu waktu yang menjalankan bagian baca tambah tulis itu.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 dari 100 pesanan
- Dengan Lock, proses penambahan processed_count menjadi bergantian. sebelum membaca dan memperbarui nilai, satu thread mengunci bagian itu, sementara thread lain harus menunggu hingga kunci dilepas. Dengan begitu, setiap kenaikan tercatat dan tidak ada thread yang menimpa hasil thread lain.

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: Sebelumnya terdapat error yang terjadi saat mencoba docker build namun hasilnya gagal dikarenakan setelah install diasumsikan docker ia akan langsung berjalan di latar belakang namun tidak ia harus dibuka terlebih dahulu. setelah dibuka proses docker build berhasil. 

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
