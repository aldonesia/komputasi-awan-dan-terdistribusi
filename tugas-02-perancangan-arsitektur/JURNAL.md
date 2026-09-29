# Jurnal Proses — Tugas 2

## [Tanggal 29/09/2026]
- Opsi arsitektur yang dipertimbangkan:
Untuk mengatasi permasalahan coupling dan risiko downtime total pada sistem monolitik FoodGo, kami memilih kombinasi Service-Oriented Architecture (SOA / Microservices) dan Publish-Subscribe (Pub-Sub).
- Kenapa akhirnya pilih [SOA/Pub-Sub]:
Aplikasi food delivery seperti FoodGo sulit jika hanya memakai satu gaya saja. Oleh karena itu kami memilih kombinasi kedua nya karena SOA untuk modul/layanan inti yang butuh respons langsung (Order, Katalog, Payment secara REST API/gRPC), dan gunakan Pub-Sub via Message Broker untuk modul yang sifatnya event-driven (Notifikasi, Resto, Kurir).
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
