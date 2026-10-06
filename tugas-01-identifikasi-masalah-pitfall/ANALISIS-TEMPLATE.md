# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [Yang penting happy]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Bagas Bintang Saputro] | [103072400078] | [The Network is Realible] |
| [Wahyu Puji Riski Purwanto] | [103072400050] | [Latency is Zero] |
| [Andi Muh. Arief alfaizi ilham] | [103072400082] | [Single Point Of Failure ] |

## Pitfall 1: [the network is reliable] — ditulis oleh [Bagas Bintang Saputro]

**Bukti di skenario:** [Kami menemukan bahwa code mereka menulis asumsi seperti # network is realible, for need to retry]

**Kenapa ini keliru:** [Dalam dunia nyata jaringan fisik maupun virtual sangat rentan terhadap gangguan. Paket data bisa hilang (packet loss),lalu router bisa mengalami restart atau terjadinya fluktuasi sinyal pada sisi pengguna aplikasi seluler. Sistem terdistribusi yang tangguh harus berasumsi bahwa kegagalan jaringan adalah hal yang pasti terjadi (meskipun jarang) dan termasuk hal yang bukan mustahil untuk terjadi]

**Dampak ke FoodGo:** [Ketika terjadi kegagalan jaringan sementara asaat aplikasi mengirim data pesanan ke backend, sistem langsung menyerah dan gagal karena tidak memilii mekanisme retry. Hal ini menyebabkan pengguna mengalami error secara tiba-tiba meskipun server sebenarnya masih menyala]

**Solusi desain awal:** [Bisa diterapkan pola Retry dengan Exponential Backoff & Jitter. Jika terjadi kegagalan koneksi, sistem akan mencoba ulang pengiriman dengan jeda waktu yang bertambah secara eksponensial misalnya jeda 1 detik,lalu 2 detik, lalu 5 detik yang ditambah sedikit waktu acak (Jitter) agar tidak terjadi penumpukan request pada detik yang sama]

**Trade-off:** [Meskipun retry berguna untuk mengatasi kegagalan jaringan sementara, jika tidak dikonfigurasi dengan hati-hati, retry justru bisa menjadi pisau bermata dua. jika server backend sedang sangat lambat karena kelebihan beban trafik sungguhan, ratusan hingga ribuan user yang melakukan entry serentak akan memberikan beban tambahan yang eksponensial. Hal ini dapat menyebabkan cascading failure dimana server yang awalnya hanya sekedar lambat akhirnya hancur dihantam request ulang]

---

## Pitfall 2: [Latency Is Zero] — ditulis oleh [Wahyu Puji Riski Purwanto]

**Bukti di skenario:** [Tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)]

**Kenapa ini keliru:** [Komunikasi antar-service tidak selalu berjalan dengan cepat. Saat banyak pengguna melakukan transaksi secara bersamaan, modul pembayaran bisa membutuhkan waktu lebih lama untuk memberikan respons. Karena tidak ada timeout, modul pesanan akan terus menunggu sampai mendapatkan respons.]

**Dampak ke FoodGo:** [Ketika modul pembayaran lambat, banyak permintaan dari modul pesanan dapat ikut tertahan. Jika jumlah permintaan terus bertambah, beban sistem juga meningkat sehingga aplikasi menjadi lambat, mengalami timeout, atau bahkan crash.]

**Solusi desain awal:** [Menerapkan timeout agar modul pesanan memiliki batas waktu saat menunggu respons dari modul pembayaran. Jika respons tidak diterima sampai batas waktu tersebut, sistem dapat melakukan penanganan lain dan tidak terus menunggu. Selain itu, circuit breaker dapat digunakan jika modul pembayaran berulang kali mengalami masalah.]

**Trade-off:** [Jika timeout terlalu pendek, sistem bisa mengalami timeout padahal modul pembayaran sebenarnya masih memproses transaksi. Namun, jika terlalu panjang, permintaan tetap akan tertahan cukup lama sehingga penggunaan resource masih bisa meningkat.]

---

## Pitfall 3: [Single Point Of Failure ] — ditulis oleh [Andi Muh Arief Alfaizi Ilham]

**Bukti di skenario:** [satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.]

**Kenapa ini keliru:** [karena semua modul berada dalam 1 server yang dapat menyebabkan lag dan sistemnya mati total]

**Dampak ke FoodGo:** [karena semua modul berebut memori dan CPU di server yang sama, server  kemungkinan akan mengalami crash akibat terlalu banyak request yang terpaksa melakukan restart terhadap server]

**Solusi desain awal:** [Melakukan pemisahan setiap modul yang menjadi layanan tepisah]

**Trade-off:** [Komunikasi Antar modul menjadi lebih rumit karena harus bergantung pada jaringan internet/internal, dan merawat banyak layanan terpisah membutuhkan biaya serta usaha yang lebih besar di banding satu server monolitik]

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.

Kegagalan sistem FoodGo berakar dari arsitektur monolik yang digabungkan dengan optimisme berlebihan terhadap keandalan jaringan dan kecepatan respon layanan, karena semua modul berada di satu tempat (SPOF) dan saling terikat secara sinkron tanpa timeout, satu gangguan kecil pada modul pembayaran dapat memicu efek domino yang melumpuhkan seluruh sistem

dan untuk memperbaiki ketiga pitfall ini secara garis besar FoodGo harus beralih dari arsitektur Monolik menjadi sistem terdistribusi berbasis layanan (Microservices / Service-Oriented Architecture). Selain itu untuk mencegah layanan saling tunggu, komunikasi antar modul harus mulai asinkron. yang dimana desain ini akan dirancang lebih detail pada tugas 2.
]