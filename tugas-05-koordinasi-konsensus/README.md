# Laporan Tugas 5 — Koordinasi & Konsensus (Bully Algorithm)
**Kelompok:**
**Anggota:**
1. Diandra Nanditya Mulkis (103072409975) — melakukan pengujian pada kondisi normal dan pada kondisi leader dimatikan
2. Naufal Fudhail (10307240013) — menyusun analisis trade-off Bully vs Raft
3. Samuel Nelson Wabiser (103072400111) — mengimplementasikan Bully Algorithm di `src/node.py`, termasuk sinkronisasi balasan `OK` dengan `threading.Event()` pada `start_election()` serta mekanisme pergantian leader otomatis

## 1. Kenapa Sistem Membutuhkan Leader?
Pada sistem terdistribusi seperti FoodGo, banyak server menerima pesanan secara bersamaan. Tanpa satu leader sebagai penentu urutan, tiap server bisa memutuskan urutan sendiri sehingga data tidak konsisten dan pesanan yang sama bisa diproses dua kali (*double processing*). Leader menjadi satu titik keputusan sehingga semua node mengikuti urutan yang sama.

## 2. Mengapa Bully Algorithm Selalu Memilih Node Ber-ID Tertinggi?
Algoritma ini menjadikan ID sebagai prioritas. Node yang memulai election hanya mengirim `ELECTION` ke node ber-ID lebih besar. Kalau ada yang membalas `OK`, node itu mengambil alih dan menjalankan election sendiri ke node di atasnya, sehingga prosesnya naik bertahap. Node yang tidak mendapat balasan dari siapa pun berarti ber-ID tertinggi di antara node yang hidup, dan ia mengumumkan diri lewat `COORDINATOR`. Hasilnya selalu sama selama kumpulan node yang hidup sama.

## 3. Analisis Trade-off: Bully vs Raft
* **Bully Algorithm:**
  * *Kelebihan:* Mudah dibuat dan dipahami, serta cepat menghasilkan leader selama node tertinggi aktif.
  * *Kelemahan:* Pesan yang dikirim saat election banyak karena beberapa node bisa memicu election bersamaan. Kalau node ber-ID tertinggi sering mati-hidup (*flapping*), election terus berulang dan leader berganti-ganti.
* **Raft Consensus:**
  * *Kelebihan:* Memakai timeout acak dan suara mayoritas (*quorum*) sehingga bentrok election jarang terjadi, dan sekaligus menangani replikasi log sehingga data tetap konsisten.
  * *Kelemahan:* Jauh lebih rumit untuk diimplementasikan dan di-debug dibanding Bully.

## 4. Hasil Pengujian Skenario
* **Skenario 1 (Start Normal):** Node 1 sampai 5 dijalankan di terminal masing-masing. Setiap node menjalankan election, dan setelah pesan `COORDINATOR` saling diterima, semua node mengakui Node 5 (ID tertinggi) sebagai leader. Setelah itu hanya `PING` berkala yang tampak di log.
* **Skenario 2 (Leader Mati):** Proses Node 5 dihentikan dengan `Ctrl+C`. Dalam sekitar 3 detik, node lain gagal melakukan `PING` ke Node 5 dan memulai election ulang. Node 4 menjadi leader baru karena tidak ada lagi node aktif di atasnya, lalu menyiarkan `COORDINATOR` ke node lain.
