# Tugas 5 — Koordinasi & Konsensus: Bully Algorithm (FoodGo)

Simulasi pemilihan leader dengan Bully Algorithm: 5 proses Python (`src/node.py`), masing-masing satu node di port 5001–5005, komunikasi lewat TCP socket di `localhost`.

## Cara menjalankan

Buka 5 terminal, jalankan dari folder `tugas-05-koordinasi-konsensus/`:

```bash
python3 -u src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005 | tee bukti/log_node1.txt
python3 -u src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005 | tee bukti/log_node2.txt
python3 -u src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005 | tee bukti/log_node3.txt
python3 -u src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005 | tee bukti/log_node4.txt
python3 -u src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004 | tee bukti/log_node5.txt
```

## 1. Kenapa FoodGo butuh satu leader?

Di FoodGo, dua server mencatat urutan pesanan yang berbeda karena jam keduanya tidak sinkron. Kalau semua server boleh memutuskan urutan antrean sendiri-sendiri, pesanan yang sama bisa diproses dua kali atau diurutkan berbeda. Dengan satu **Node Leader** yang memegang antrean pusat, urutan pesanan ditentukan di satu tempat saja, jadi tidak ada konflik pemrosesan ganda. Server lain cukup meneruskan pesanan ke leader.

## 2. Cara kerja implementasi

- `ELECTION` dikirim ke semua node ber-ID lebih besar.
- Node yang menerima `ELECTION` dari ID lebih kecil membalas `OK`, lalu ikut menjalankan election sendiri.
- Kalau dalam 2 detik tidak ada `OK`, node menyatakan diri leader dan broadcast `COORDINATOR` ke semua node.
- Kalau ada `OK`, node berhenti mencalonkan diri dan menunggu `COORDINATOR`.
- `monitor_leader` mengirim `PING` ke leader tiap 3 detik. Kalau gagal connect, leader dianggap mati dan election dimulai lagi.

## 3. Kenapa selalu node ber-ID tertinggi yang masih hidup?

Setiap node hanya berhenti mencalonkan diri kalau ada node yang lebih besar menjawab `OK`. Jadi satu-satunya node yang tidak pernah menerima `OK` adalah node dengan ID terbesar di antara yang hidup — node itu pasti menang. Node yang lebih kecil selalu "kalah" (di-*bully*) selama ada yang lebih besar dan hidup.

## 4. Hasil skenario

### Skenario 1 — Start normal
Node 1–5 dinyalakan hampir bersamaan. Node 5 tidak menerima `OK` dari siapa pun, lalu broadcast `COORDINATOR`. Semua node mencatat **leader = node 5**.

![Menjalankan 5 node di 5 terminal](bukti/Menjalankan%205%20node%20di%205%20terminal.png)
![kelima node berjalan dan Node 5 menjadi leader](bukti/kelima%20node%20berjalan%20dan%20Node%205%20menjadi%20leader.png)

### Skenario 2 — Leader mati
Node 5 dimatikan dengan Ctrl+C. Dalam ≤3 detik node lain gagal mem-`PING` node 5 dan memulai election. Node 4 tidak menerima `OK` (node 5 mati), lalu broadcast `COORDINATOR`. Pesan ke node 5 gagal terkirim, dan semua node hidup mencatat **leader = node 4**.

![setelah Node 5 dihentikan, Node 4 menjadi leader](bukti/setelah%20Node%205%20dihentikan,%20Node%204%20menjadi%20leader.png)

## 5. Kelemahan Bully dibanding algoritma lain 

- **Jumlah pesan banyak.** Satu node ber-ID rendah yang memulai election mengirim `ELECTION` ke semua node di atasnya, dan masing-masing membalas lalu memulai election sendiri. Kasus terburuk (node 1 yang mendeteksi) menghasilkan pesan O(n²). Di log skenario 2 terlihat node 1, 2, 3 semuanya ikut kirim `ELECTION`, padahal hasilnya tetap node 4. Raft memakai voting dengan jumlah pesan jauh lebih sedikit.
- **Tidak ada leader selama election.** Dari leader mati sampai `COORDINATOR` baru diterima, ada jeda (deteksi ≤3 detik + timeout 2 detik). Untuk FoodGo, di jeda ini antrean pusat tidak punya pemilik: pesanan masuk bisa tertahan atau salah rute. Leader adalah single point of failure sampai leader baru terpilih.
- **Node tinggi yang restart langsung merebut leader**, walaupun leader sekarang sehat. Itu bisa memutus antrean yang sedang diproses. Raft hanya mengganti leader lewat term baru dan suara mayoritas.
- **Mengandalkan timeout dan asumsi jaringan andal.** Kalau jaringan terpisah (partition), kedua sisi bisa sama-sama punya leader (split-brain), karena Bully tidak butuh mayoritas. Raft butuh suara mayoritas, jadi aman dari masalah ini.

**Kelebihan Bully:** sederhana, mudah dipahami dan diimplementasikan, cocok untuk simulasi kecil seperti ini.