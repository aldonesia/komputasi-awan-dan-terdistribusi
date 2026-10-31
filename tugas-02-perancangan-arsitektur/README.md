# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Materi terkait:** Architectural style (Layered, SOA, Peer-to-Peer, Publish-Subscribe).

**Kelompok :** Kelompok 2

| NAMA                                  | NIM          |
| ------------------------------------- | ------------ |
| Yan Chrisdaniel Partogi rayano Ludjen | 103072400010 |
| Bima Luthfi Nurhakim                  | 103072400030 |
| Jeremy Joving Winargo                 | 103072400085 |
| Ahmad Nur Fajri                       | 103072430007 |

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok

1. Pilih **satu** gaya arsitektur utama: **Service-Oriented Architecture (SOA)** atau **Publish-Subscribe**. Boleh dikombinasikan (mis. SOA untuk service inti + Pub-Sub untuk notifikasi), tapi harus dijustifikasi kenapa kombinasi ini yang dipilih.
2. Gambarkan minimal 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway jika relevan).
3. Jelaskan alur satu skenario penuh secara end-to-end di diagram (misalnya: pelanggan buat pesanan → bayar → resto terima notifikasi → kurir ditugaskan) — tunjukkan komponen mana berkomunikasi dengan siapa, dan **jenis komunikasinya** (sinkron/asinkron, request-response/event).
4. Analisis tertulis: kenapa gaya ini mengatasi masalah _coupling_ dari Tugas 1, dan apa trade-off-nya (mis. Pub-Sub menambah kompleksitas debugging karena alur tidak linear).

## Hasil Diskusi

### Planning Arsitektuk

<div align="justify">Memutuskan untuk memilih Service Oriented Architecture sebagai arsitektur utamanya dan memilih Publish Subscribe sebagai pola komunikasi asinkron untuk event dan notifikasi. mengapa kami memilih SOA tersebut, karena kebutuhan utamanya adalah memisahkan fungsi pesanan, pembayaran, katalog resto, dan kurir/notifikasi menjadi layanan dengan tanggung jawab dan kontrak yang jelas. Tim dapat mengembangkan dan memperbarui layanan secara terpisah. Lalu mengapa kita juga memilih Publish-Subcribe, karena untuk melengkapi SOA. ia digunakan sebagai alur yang tidak perlu menahan permintaan pelanggan sambil menunggu layanan lain, khususnya hasil pembayaran dan pemberitahuan ke resto maupun kurir. Jadi Pub-Sub bukan gaya arsitektuk utama kedua yang berdiri sendiri, ia merupakan pola komunikasi antar layanan dalam rancangan SOA FoodGo.</div>

### Diagram Arsitektur

<img src="diagram/DIAGRAM ARSITEKTUR FOOD-GO.jpg" alt="Diagram Arsitektur Food-Go" width="250">

### Keunggulan Arsitektur

<div align="justify">Keunggulan saat ini SOA sebagai arsitektur utama dan Publish-Subscribe untuk komunikasi event adalah keduanya saling melengkapi, jadi SOA ini menetapkan batas tanggung jawab dan kontrak layanan yang jelas Pesanan, Pembayaran, Katalog, Resto, dan Kurir/Notifikasi sehingga tiap layanan dapat dikembangkan, diskalakan, dan di-deploy lebih mandiri. Pub-Sub kemudian menghubungkan layanan untuk proses yang tidak membutuhkan jawaban langsung, misalnya hasil pembayaran dan pemberitahuan pesanan, sehingga penerbit event tidak perlu menunggu atau mengetahui detail setiap penerima. Dibanding SOA saja, kombinasi ini mengurangi ketergantungan pada komunikasi langsung dan waktu aktif layanan lain untuk alur asinkron, sehingga layanan Pesanan tidak perlu menahan proses sampai Pembayaran atau Notifikasi selesai. SOA saja tetap dapat memakai komunikasi sinkron yang lebih mudah dipahami, tetapi pemanggil dan layanan tujuan lebih terikat selama request berlangsung.</div>
<br>
<div align="justify">Dibanding Pub-Sub saja, SOA memberi struktur layanan dan pembagian tanggung jawab yang lebih tegas, sementara Pub-Sub saja dapat menyebarkan event dengan fleksibel tetapi tidak dengan sendirinya menentukan batas layanan, kepemilikan fungsi, atau alur request-response yang memang perlu jawaban segera contoh validasi menu oleh Katalog. Karena itu, kombinasi SOA + Pub-Sub membuat FoodGo tetap terstruktur untuk operasi inti dan lebih longgar untuk proses berbasis event, mendukung deployment independen, skala per layanan, dan juga mengurangi dampak gangguan sementara.</div>

### Alur End-To-End (System FoodGo)

<div align="justify">Jadi awal alurnya adalah pelanggan menekan tombol Buat Pesanan di aplikasi FoodGo. Aplikasi mengirim HTTP request secara sinkron ke API Gateway, yang meneruskannya ke Modul Pesanan. Modul Pesanan memeriksa menu dan ketersediaannya dengan memanggil Modul Katalog melalui komunikasi request-response sinkron. Modul Pesanan menunggu hasil validasi sebelum melanjutkan. Jika menu tersedia, Modul Pesanan mencatat pesanan dengan status Menunggu Pembayaran, lalu menerbitkan event PaymentRequested ke Message Broker. Setelah permintaan diterima untuk diproses, API Gateway mengirim respons HTTP 202 Accepted kepada pelanggan. Respons ini hanya menandakan bahwa permintaan pesanan diterima, bukan bahwa pembayaran telah berhasil. Selanjutnya, Modul Pembayaran berlangganan event PaymentRequested, memproses pembayaran secara asinkron, lalu menerbitkan event PaymentSucceeded jika transaksi berhasil atau PaymentFailed jika gagal. Modul Pesanan menerima hasil tersebut dari broker dan memperbarui status pesanan. Jika pembayaran berhasil, Modul Pesanan menerbitkan event OrderConfirmed agar Modul Resto dapat menerima detail pesanan dan menyiapkannya.</div>
<br>
<div align="justify"> Setelah resto menyetujui pesanan, Modul Resto menerbitkan RestaurantAccepted. Modul Kurir/Notifikasi yang berlangganan event itu kemudian menugaskan kurir, menerbitkan CourierAssigned, dan mengirim push notification kepada pelanggan berisi informasi bahwa pesanan diterima resto dan kurir telah ditugaskan. Dengan begitu  Setelah resto menyetujui pesanan, Modul Resto menerbitkan RestaurantAccepted. Modul Kurir/Notifikasi yang berlangganan event itu kemudian menugaskan kurir, menerbitkan CourierAssigned, dan mengirim push notification kepada pelanggan berisi informasi bahwa pesanan diterima resto dan kurir telah ditugaskan. jika hasil pembayaran terlambat atau terjadi timeout, statusnya tetap menunggu konfirmasi karena timeout tidak otomatis berarti pembayaran gagal.</div>

### Analisis alasan Coupling dan trade-off

#### Analisis solusi coupling

<div align="justify">Di tugas satu sebelumnya itu seluruh modul FoodGo berjalan dalam satu aplikasi monolitik, sehingga perubahan atau deployment pada satu modul dapat mengharuskan seluruh aplikasi di-restart dan berisiko mengganggu modul lain. Dengan SOA, fungsi Pesanan, Pembayaran, Katalog, Resto, dan Kurir/Notifikasi dipisahkan menjadi layanan dengan tanggung jawab serta kontrak yang jelas, sehingga tiap tim dapat memperbarui dan men-deploy layanannya secara lebih mandiri. Pub-Sub melengkapi SOA untuk komunikasi asinkron, Modul Pesanan dapat menerbitkan event seperti OrderConfirmed ke Message Broker, lalu Modul Resto dan Kurir/Notifikasi memprosesnya secara mandiri tanpa membuat Modul Pesanan mengetahui detail tiap layanan atau menunggu semuanya selesai. Kombinasi ini mengurangi ketergantungan langsung dan membantu membatasi dampak keterlambatan satu layanan. Komunikasi sinkron tetap digunakan ketika jawaban langsung diperlukan, seperti validasi menu oleh Katalog.</div>

#### Trade off

<div align="justify">Alur Pub-Sub yang tidak linear membuat debugging dan pelacakan lebih kompleks, sehingga diperlukan correlation ID, log, tracing, dan pemantauan. Pemrosesan event asinkron juga dapat menyebabkan status antar-layanan tidak langsung seragam, pesan dapat terlambat atau terkirim ulang, sehingga diperlukan penanganan konsistensi, idempotensi, dan retry terbatas. Selain itu, FoodGo harus mengelola Message Broker dan kontrak event. Komunikasi sinkron yang masih digunakan tetap berisiko lambat atau gagal dan memerlukan timeout serta penanganan error. Jadi, SOA + Pub-Sub mengurangi coupling monolitik, tetapi menambah kompleksitas operasional dan tidak menghilangkan semua sumber gangguan.</div>
