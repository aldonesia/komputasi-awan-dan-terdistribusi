# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): logika pencarian hanya melakukan iterasi untuk mencari node dengan ID yang lebih besar atau sama dengan (>=) dari key_hash. Akibatnya, ketika nilai key_hash lebih besar daripada seluruh ID node yang ada di dalam ring, fungsi gagal menemukan penanggung jawab karena tidak memperhitungkan sifat wrap-around dari topologi Chord.
- Cara memperbaikinya: Mengurutkan daftar ID node terlebih dahulu menggunakan sorted(), lalu melakukan iterasi pengecekan node >= key_hash. Jika perulangan habis dan tidak ditemukan, fungsi ditambahkan logika wrap-around untuk mengembalikan node pertama dengan ID terkecil di dalam ring (sorted_nodes[0]).

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung:
  Sebelum: Pemetaan data dikelola oleh 4 node awal (node-jakarta-1, node-jakarta-2, node-bandung-1, node-surabaya-1), dan hasil lookup kurir-001 serta kurir-002 berhasil mengembalikan IP masing-masing.
  Sesudah: Saat node-medan-1 (id=123) bergabung, node baru ini masuk ke dalam urutan ring dan mengambil alih tanggung jawab data yang berada di rentangnya dari successor lama. Hasil lookup kurir-001 tetap akurat mengembalikan IP aslinya.
- Hasil sebelum & sesudah node keluar:
  Sebelum: node-jakarta-1 (id=177) keluar, proses pencarian lookup berjalan normal melalui node tersebut dan node lainnya.
  Sesudah: node-jakarta-1 dikeluarkan (leave), sistem secara otomatis memindahkan tanggung jawab data ke successor barunya yaitu node-bandung-1 (id=40) via aturan wrap-around. Pengujian lookup untuk kurir-001 dan kurir-002 tetap berhasil mengembalikan alamat IP yang benar tanpa error.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|30/10/2026|Gemini AI|Meminta brainstorming logika implementasi find_successor, join, dan leave pada skeleton Chord DHT Python.|Memberikan konsep sorting kunci node, pengecekan kondisi >= key_hash dengan wrap-around ke indeks pertama, serta logika penyaringan key untuk perpindahan tanggung jawab (successor).|Logika dasar dipelajari untuk memahami aturan successor Chord, lalu kode diketik/disesuaikan sendiri ke dalam struktur skrip chord_simulation.py dan diuji langsung di terminal.|
| ... | ... | ... | ... | ... |
