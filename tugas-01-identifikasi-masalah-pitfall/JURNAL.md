# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal 22/09/2026]
- Peserta: 1. delon 2. steven
- Poin diskusi: pitfall yang digunakan mencangkup network is reliable, latency is zero dan tightly coupled monolith

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
<<<<<<< HEAD
=======
| 22 September 2026 | Gemini | pitfall apa saja yang mungkin relevan | The network is reliable, Latency is zero, Tightly Coupled Monolith, Thread Pool Exhaustion, Lack of Asynchronous Processing | Kami memilih menggunakan the network is reliable, Latency is zero, dan Tightly Coupled Monolith |
|22 September 2026 | Gemini | Jika solusi ini diterapkan, apa trade-off yang mungkin terjadi | Sistem menjadi lebih kompleks karena harus mengelola beberapa layanan dan komunikasi antar-service. Proses debugging, deployment, dan pengelolaan infrastruktur juga menjadi lebih sulit dibandingkan ketika semuanya masih berada dalam satu sistem. | Pemecahan sistem menjadi layanan terpisah meningkatkan kompleksitas pengelolaan infrastruktur, komunikasi jaringan antar-service, serta kesulitan dalam proses debugging dan deployment. |
| 22 September 2026 | Gemini | mengapa jika melakukan pemecahan layanan debugging menjadi lebih sulit bukannya malah lebih gampang? | Debugging menjadi lebih sulit karena ketika sistem dipecah menjadi beberapa layanan, masalah yang muncul bisa berasal dari salah satu layanan atau dari interaksi antar-layanan. Hal ini membuat proses identifikasi sumber masalah menjadi lebih kompleks dibandingkan ketika semua fungsi berada dalam satu sistem monolitik. | ... |
| 22 September 2026 | Gemini | Bagaimana Jika Pengguna Menekan Tombol Bayar Lagi Ketika Sistem Sedang Timeout | Berdasarkan kondisi sistem yang mengalami keterlambatan, timeout, dan kegagalan jaringan saat trafik melonjak, modul pembayaran yang tidak dirancang dengan penanganan transaksi aman rentan menerima pengiriman data berulang (retry) dari pengguna atau sistem klien tanpa validasi status transaksi sebelumnya. | Jika sistem tidak memiliki mekanisme untuk mengenali transaksi yang sama, maka transaksi tersebut bisa diproses berulang. Hal ini dapat menyebabkan pengguna dikenakan biaya dua kali untuk satu transaksi yang sama. | 
>>>>>>> 82338d3917fe192f1a5f3a67a22dff3f4c6504f0
| 22/09/2026 | Gemini | Apa saja contoh kasus nyata Fallacies of Distributed Computing pada aplikasi food delivery dan bagaimana dampaknya pada thread pool? | Menjelaskan konsep thread exhaustion akibat blocking I/O dan memberi gambaran umum dampak latensi pada arsitektur monolitik | Mengaitkan konsep thread exhaustion tersebut ke kasus spesifik FoodGo, lalu menuliskan analisis dampak serta solusinya dengan narasi sendiri |
