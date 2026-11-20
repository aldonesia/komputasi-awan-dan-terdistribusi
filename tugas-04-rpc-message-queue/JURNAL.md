# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- Jalur yang dipilih adalah RPC karena lebih sederhana untuk disiapkan, menggunakan standard library Python, dan sesuai untuk operasi yang membutuhkan respons langsung seperti cek saldo dan proses pembayaran.

## Kendala teknis
- Tidak ada

## Analisis: apa yang terjadi pada request RPC jika server mati di tengah proses (Jalur A)
- Jika server RPC mati di tengah proses, request yang sedang diproses akan terhenti dan klien akan menerima error atau timeout karena tidak ada balasan dari server. Hal ini menunjukkan sifat sinkron dari RPC, dimana klien harus menunggu respons dari server sebelum melanjutkan eksekusi.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 12 Okt 2026 | Gemini | Fungsi2 libary from xmlrpc.server import SimpleXMLRPCServer | 1. Metode Utama untuk Registrasi & Pengaturan Server : register_function(function, name=None), register_instance(instance, allow_dotted_names=False), register_introspection_functions(), register_multicall_functions(). 2. Menjalankan Server: serve_forever() | ... |
| 12 Okt 2026| Gemini | Cara mengecek waktu tempuh |Penjelasan: - time.time(): Mengambil waktu saat ini dalam bentuk detik (timestamp epoch). - start = time.time(): Menandai titik awal sebelum request dikirim ke server. - end = time.time(): Menandai titik akhir ketika server selesai memproses dan client benar-benar telah menerima balasan. - end - start: Menghitung total durasi waktu yang dibutuhkan oleh jaringan dan server untuk memproses permintaan tersebut. Format :.4f digunakan untuk menampilkan hasil dalam 4 angka di belakang koma agar presisi.| ... |