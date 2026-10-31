# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Mengatur proses election agar berjalan dengan benar ketika beberapa node memulai election secara bersamaan, serta memastikan pesan "ELECTION, OK, dan COORDINATOR" diterima dan diproses oleh node yang sesuai.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: 
1. Semua node mulai dan memulai election 
- Node 1 menghubungi node dengan ID lebih tinggi yaitu 2–5.
- Node 2 menghubungi 3–5, Node 3 menghubungi 4–5, Node 4 menghubungi 5.
- Node 5 tidak punya peer dengan ID lebih tinggi, lalu menyatakan dirinya sebagai leader dan mengirim COORDINATOR.

2. Node-node menerima pengumuman leader
- Node 1–4 mengakui dirinya menjadi leader. Setelah menerima pesan COORDINATOR dari node bernomor lebih tinggi, mereka mengganti leader yang diketahui, dari Node 2, lalu 3, 4, hingga 5. 
- Jadi, jika semua node aktif dan pesan terkirim normal, Node 5 menjadi leader akhir.

Kelima node berhasil dijalankan pada port yang berbeda. Setiap node memulai proses election dan mengirim pesan kepada node dengan ID lebih tinggi. Node 5 terpilih sebagai leader karena memiliki ID tertinggi. Node lain menerima pesan COORDINATOR yang mengumumkan leader saat ini.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4
- Berapa lama waktu sampai leader baru terdeteksi: dari yang kami catat lama waktu  sampai leader baru terdeteksi oleh setiap node adalah sekitar 14~15 detik

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
