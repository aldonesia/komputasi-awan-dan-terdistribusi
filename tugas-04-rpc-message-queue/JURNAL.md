# Jurnal Proses — Tugas 4


## Jalur yang dipilih

[RPC / MQ / keduanya], alasan: ...


## Kendala teknis

Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...


## Uji "pesan tidak hilang" (khusus Jalur B)

Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
Hasil yang diamati: ...
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 12 Okt 2026 | Gemini | Fungsi2 libary from xmlrpc.server import SimpleXMLRPCServer | 1. Metode Utama untuk Registrasi & Pengaturan Server : register_function(function, name=None), register_instance(instance, allow_dotted_names=False), register_introspection_functions(), register_multicall_functions(). 2. Menjalankan Server: serve_forever() | ... |
| 12 Okt 2026| Gemini | Cara mengecek waktu tempuh |Penjelasan: - time.time(): Mengambil waktu saat ini dalam bentuk detik (timestamp epoch). - start = time.time(): Menandai titik awal sebelum request dikirim ke server. - end = time.time(): Menandai titik akhir ketika server selesai memproses dan client benar-benar telah menerima balasan. - end - start: Menghitung total durasi waktu yang dibutuhkan oleh jaringan dan server untuk memproses permintaan tersebut. Format :.4f digunakan untuk menampilkan hasil dalam 4 angka di belakang koma agar presisi.| ... |