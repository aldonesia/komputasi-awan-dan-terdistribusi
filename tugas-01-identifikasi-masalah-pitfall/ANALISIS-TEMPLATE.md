# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [10]

| Nama | NIM | Kontribusi |
|---|---|---|
| Ahmad Diqri Wirayudha | 103072400084 | The Network Is Reliable |
| Vaylan Christopher | 103072400154 | Latency is Zero |
| Shaqeel Kenzie Ramadhansyah Dirganthara | 103072400061 | Single Point Of Failure |

## Pitfall 1: The Network Is Reliable — ditulis oleh Ahmad Diqri Wirayudha

**Bukti di skenario:** Melakukan Pembayaran order makanan non-tunai dari customer kepada pihak FoodGo melalui pihak ke 3 (bank), tanpa adanya mekanisme batas waktu tunggu (timeout), penanganan koneksi putus, maupun pembatasan pemanggilan berulang.

**Kenapa ini keliru:** 
Karena, jika terjadi suatu case/masalah yang di mana server atau koneksi dari pihak ke tiga (bank) mengalami gangguan saat proses pembayaran, maka hal ini bisa menjadi fatal.

**Dampak ke FoodGo:**
1. Server FoodGo tidak tahu harus berbuat apa karena tidak adanya batas waktu tunggu (timeout).
2. Aplikasi FoodGo tetap menahan koneksi (hang/freeze) sambil menunggu jawaban Bank.
3. 1 customer menunggu, 2 customer menunggu, lama-lama ratusan customer menunggu proses pembayaran.

Hasilnya: Server FoodGo kehabisan kapasitas (thread exhaustion) hanya untuk diam menunggu. Akhirnya aplikasi FoodGo mati total (crash), bahkan orang lain yang sedang melihat menu, jadi tidak bisa menggunakan aplikasi.

**Solusi desain awal:** 
1. Pasang Timeout (Batas waktu tunggu):
Memberi aturan: "Kalau dalam 5 detik Bank tidak membalas, anggap koneksi putus dan lepaskan antrean server."

2. Circuit Breaker (Sekring Listrik):
Mirip saklar MCB listrik di rumah. Semisal jika dalam 5 menit ada 100 transaksi ke Bank yang gagal terus-menerus, maka putus sementara jalurnya (open circuit). Beri tahu user: "Sistem pembayaran sedang gangguan, silakan gunakan metode lain" tanpa perlu membebani server FoodGo untuk mencoba koneksi yang jelas-jelas sedang rusak.

3. Idempotency (Cegah Bayar Double):
Saat jaringan putus dan sistem mencoba kirim ulang (retry), pastikan ada nomor unik transaksi agar saldo pelanggan tidak terpotong dua kali.

**Trade-off:**
1. Karena adanya fitur timeout dan circuit breaker, potensi rugi dari kedua pihak menaik : Transaksi yang sebenarnya mungkin bisa berhasil jika "ditunggu sedikit lebih lama" terpaksa digugurkan demi menyelamatkan kestabilan server

2. Risiko Serangan Balik (Self-Inflicted DDoS): Jika ratusan pelanggan checkout bersamaan dan jaringannya sedang goyang, fitur retry akan menyerang server pembayaran secara berkali-kali lipat (retry storm). koneksi yang sedang bermasalah justru bisa mati total karena kebanjiran request kirim ulang (retry) dari FoodGo sendiri.
---

## Pitfall 2: Latency is Zero — ditulis oleh Vaylan Christopher

**Bukti di skenario:** tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** 
banyak orang yang mengira suatu jaringan dengan latensi nol orang bisa mengirim data tanpa loading sama sekali.

**Dampak ke FoodGo:**
terjadi kehabisan ketersediaan port TCP pada sistem pembayaran. hal ini disebabkan oleh tumpukan koneksi yang sangat lambat yang tidak pernah ditutup secara otomatis maupun dikembalikan ke dalam connection pool untuk dapat digunakan kembali oleh proses lain.

**Solusi desain awal:** 
menerapkan perbaikan arsitektur dengan cara menghilangkan ketergantungan komunikasi yang bersifat mengunci dan sinkron (blocking synchronous) pada proses pemanggilan antar service.

**Trade-off:**
Alur pemrosesan transaksi tidak lagi berjalan secara terurut atau linier dalam satu waktu. Dampaknya, pengguna tidak bisa lagi langsung menerima status konfirmasi keberhasilan transaksi secara instan pada detik yang sama saat pemesanan dilakukan.

---

## Pitfall 3: Single Point Of Failure — ditulis oleh Shaqeel Kenzie Ramadhansyah Dirganthara

**Bukti di skenario:** Pada studi kasus dijelaskan bahwa seluruh modul utama, yaitu pesanan, pembayaran, dan notifikasi kurir, dijalankan pada satu server dan berada dalam satu proses monolitik yang sama. Selain itu, disebutkan juga bahwa server backend terkadang mengalami crash dan harus dinyalakan kembali secara manual.

**Kenapa ini keliru:** karena jika menempatkan seluruh layanan penting dalam satu server itu dapat membuat sistem terlalu bergantung pada satu titik. setiap server pasti memiliki keterbatasan sumber daya seperti CPU, memori, dan kapasitas jaringan. kalau beban kerja meningkat drastis atau terjadi gangguan pada server tersebut, maka seluruh layanan yang bergantung pada server itu akan ikut terdampak. Oleh karena itu, asumsi bahwa satu server dapat menangani semua kebutuhan sistem secara terus-menerus bukan pendekatan yang ideal untuk aplikasi dengan jumlah pengguna yang besar.

**Dampak ke FoodGo:** Ketika terjadi lonjakan pesanan, misalnya saat jam makan siang atau ketika ada promo besar, penggunaan sumber daya server meningkat secara signifikan. Karena semua modul berbagi sumber daya yang sama, modul pembayaran dan notifikasi kurir juga ikut terdampak meskipun sumber masalahnya berasal dari tingginya beban pada modul pesanan. Kondisi ini dapat menyebabkan aplikasi menjadi lambat, banyak permintaan mengalami timeout, hingga server mengalami crash. Akibatnya, seluruh layanan FoodGo tidak dapat beroperasi secara normal pada waktu yang bersamaan.

**Solusi desain awal:** Salah satu solusi yang dapat diterapkan adalah dengan memisahkan setiap modul menjadi service yang berdiri sendiri. Dengan cara ini, modul pesanan, pembayaran, dan notifikasi kurir dapat berjalan pada server yang berbeda. solusi tersebut memungkinkan setiap service untuk ditingkatkan kapasitasnya sesuai kebutuhan sesuai kebutuhan dan mengurangi resiko seluruh sistem berhenti/crash ketika salah satu service mengalami gangguan.

**Trade-off:** Meskipun solusi ini dapat meningkatkan keandalan sistem, penerapannya juga menambah kompleksitas arsitektur. yang pasti Tim pengembang harus mengelola lebih banyak service, mengatur komunikasi antar service, serta menyiapkan mekanisme monitoring dan load balancing. Selain itu, biaya operasional juga berpotensi meningkat karena diperlukan lebih banyak sumber daya infrastruktur dibandingkan menggunakan satu server monolitik.

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
