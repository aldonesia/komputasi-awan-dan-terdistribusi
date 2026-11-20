# Jurnal Proses — Tugas 2

## [29/09/2026] 
- Opsi arsitektur yang dipertimbangkan:
Untuk mengatasi permasalahan coupling dan risiko downtime total pada sistem monolitik FoodGo, kami memilih kombinasi Service-Oriented Architecture (SOA / Microservices) dan Publish-Subscribe (Pub-Sub).
- Kenapa akhirnya pilih [SOA/Pub-Sub]:
Aplikasi food delivery seperti FoodGo sulit jika hanya memakai satu gaya saja. Oleh karena itu kami memilih kombinasi kedua nya karena SOA untuk modul/layanan inti yang butuh respons langsung (Order, Katalog, Payment secara REST API/gRPC), dan gunakan Pub-Sub via Message Broker untuk modul yang sifatnya event-driven (Notifikasi, Resto, Kurir).
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 29/09/2026 | Gemini | "Bagaimana cara memisahkan alur synchronous dan asynchronous pada aplikasi food delivery menggunakan kombinasi SOA dan Pub-Sub?" | Memberikan saran pemisahan: transaksi/pembayaran awal menggunakan synchronous REST/gRPC, sedangkan notifikasi, dapur, dan penugasan kurir menggunakan asynchronous event bus. | Menyesuaikan alur tersebut ke 4 modul utama FoodGo, lalu merancang sendiri urutan step-by-step transaksi di tabel alur end-to-end pada README.md |
| 29/09/2026 | Gemini | "Jelaskan alur skenario end-to-end dan analisis trade-off (decoupling vs kompleksitas) untuk Tugas 2 berdasarkan diagram Markdown yang telah dibuat." | Memberikan struktur penjelasan alur transaksi per langkah (pengirim, penerima, pesan, jenis komunikasi) serta poin-poin trade-off teknis seperti tracing, eventual consistency, dan beban operasional | Memilih poin-poin analisis yang paling relevan dengan permasalahan coupling dari Tugas 1, lalu menuliskan kembali seluruh narasi skenario dan analisis trade-off menggunakan gaya bahasa kelompok sendiri di README.md |
| 29/09/2026 | Gemini | "Apa saja poin analisis kunci untuk membuktikan bahwa Pub-Sub mengatasi tight coupling pada monolitik, serta apa trade-off utamanya?" | Memberikan poin-poin dampak seperti fault isolation, decoupled scaling, serta tantangan distributed tracing dan eventual consistency. | Mengaitkan poin-poin tersebut dengan temuan kegagalan FoodGo pada Tugas 1, lalu menguraikan analisis dampak dan langkah mitigasinya |
