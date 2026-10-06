# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 0 (seharusnya 100)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): operasi increment seperti processed_count += 1 di Python bukanlah operasi tunggal yang instan (atomic operation), melainkan terdiri dari 3 langkah utama di tingkat mesin/CPU. Ketika ada banyak thread yang berjalan secara bersamaan (concurrently), urutan eksekusi langkah di atas bisa saling bertabrakan. Dampaknya, dua pesanan telah diproses oleh dua thread berbeda, tetapi counter hanya bertambah 1 angka saja (dari 10 menjadi 11, bukan 12). Hasil increment dari Thread A tertimpa oleh Thread B (lost update).

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100 (seharusnya 100)

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: pertama, menyalakan Virtual Machine Platform di ternminal Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform. kedua, install Windows subsystem for linux di ternminal wsl --install.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 7 OKTOBER | Gemini | "Mengapa hasil counter pada simulasi multithreading Python bisa kurang dari nilai yang seharusnya?" | Menjelaskan konsep race condition, ketiadaan sifat atomic pada increment, dan cara kerja threading.Lock | Dikarenakan adanya beberapa thread yang mau mengubah beberapa variabel secara bersamaan. seperti Operasi Increment Bukan Operasi Atomis, Pengalihan Konteks, dll |
|7 OKTOBER|GEMINI|"Mengapa error muncul di WSL 2 atau Virtual Machine Platform ketika saya menjalankan Docker Desktop di Windows? Saya mau tahu alasannya"|"Memberikan arahan umum mengenai fitur virtualisasi yang wajib aktif di Windows agar daemon Docker bisa berjalan"|"Mengikuti petunjuk perintah PowerShell untuk mengaktifkan VirtualMachinePlatform dan menjalankan wsl --install di laptop sendiri, sampai akhirnya Docker bisa berjalan dengan lancar. Setelah berhasil, mencatat semua langkah penyelesaian dalam file JURNAL.md."|
|7 OKTOBER |GEMINI|"Apa saja poin utama yang harus dibahas saat membandingkan multithreading vs multiprocessing untuk server yang boros resource?"|"Menyarankan kerangka perbandingan: overhead alokasi memori (fork vs thread), context switching, dan shared memory space"|"Mengembangkan kerangka pemikiran tersebut menjadi paragraf analisis utuh dengan bahasa sendiri pada file README.md"|
