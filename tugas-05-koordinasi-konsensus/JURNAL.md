# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: ...

## Skenario 1: Start normal
- Leader yang terpilih: leader 5 
- Log/observasi: 1. Siapa yang jadi leader dan dari mana kalian tahu. Node 5 mencetak “Saya jadi LEADER”, dan node 1-4 mencetak “Leader sekarang: node 5”.
                 2. Alur election yang terlihat. Node ber-ID kecil mengirim ELECTION ke semua node di atasnya, lalu dibalas OK oleh node yang lebih tinggi dan mundur menunggu COORDINATOR.
                 3. Kenapa node 5 yang menang. Node 5 tidak punya peer yang lebih tinggi (peer lebih tinggi: {}), jadi tidak ada yang membalas OK, timeout 2 detik habis, lalu dia broadcast COORDINATOR.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: leader 4 
- Berapa lama waktu sampai leader baru terdeteksi: sekitar 11,62 detik dengan waktu reaksi manual 

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah menjadi pekerjaan sendiri |
|---|---|---|---|---|
| 20 Oktober 2026 | Claude | Bagaimana cara menangani pesan ELECTION, OK, dan COORDINATOR pada Bully Algorithm menggunakan Python? | Pesan ELECTION digunakan untuk memulai pemilihan leader. Node dengan ID lebih besar akan membalas OK dan memulai election sendiri. Pesan OK menandakan ada node dengan ID lebih tinggi yang masih aktif, sedangkan COORDINATOR digunakan untuk memberi tahu node lain tentang leader baru. | Saya menerapkan logika tersebut pada fungsi `on_message()` dengan menyesuaikan kondisi berdasarkan ID node dan jenis pesan yang diterima. |
| 20 Oktober 2026 | Claude | Bagaimana cara menentukan leader menggunakan timeout dan balasan dari node lain pada Bully Algorithm? | Node mengirim pesan ELECTION ke semua peer yang memiliki ID lebih besar. Jika tidak menerima balasan OK sampai waktu yang ditentukan, node dapat menyatakan dirinya sebagai leader. Jika menerima OK, node menunggu pengumuman leader baru. | Saya melengkapi fungsi `start_election()` dengan memanfaatkan `ok_received`, `ELECTION_TIMEOUT`, dan `send_message()` yang sudah tersedia pada program. |
| 20 Oktober 2026 | Claude | Bagaimana cara mengumumkan leader baru kepada semua node dalam Bully Algorithm? | Node yang menjadi leader perlu menyimpan ID-nya sendiri sebagai leader dan mengirim pesan COORDINATOR ke seluruh peer agar setiap node mengetahui hasil pemilihan. | Saya melengkapi fungsi `declare_leader()` dengan memperbarui `leader_id` dan mengirim pesan COORDINATOR ke semua peer yang terdaftar. |
| 20 Oktober 2026 | Claude | Bagaimana cara mendeteksi leader yang mati dan memulai pemilihan leader baru menggunakan Python socket? | Node dapat memeriksa apakah leader masih merespons melalui koneksi socket. Jika koneksi gagal, informasi leader perlu diperbarui dan proses election dimulai kembali. | Saya melengkapi bagian pemantauan pada `monitor_leader()` dengan memeriksa respons leader melalui `send_message()` dan memanggil `start_election()` ketika leader tidak merespons. |


