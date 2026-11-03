<!-- # Tugas 1 — Analisis Pitfall FoodGo

<<<<<<< HEAD
**Kelompok:** Kelompok 13

| Nama | NIM | Kontribusi |
|---|---|---|
| [nama 1] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |
=======
**Kelompok:** [Kelompok 13]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Delon] | [103072400156] | [Arsitektur Monolitik dan Single Point of Failure] |
| [Delon] | [103072400156] | [Double Payment] |
| [Steven] | [103072400070] | [Latency is Zero] |
>>>>>>> 82338d3917fe192f1a5f3a67a22dff3f4c6504f0

## Pitfall 1: [Arsitektur Monolitik dan Single Point of Failure] — ditulis oleh [Delon]

**Bukti di skenario:** Saat trafik naik,satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama, hingga server kadang crash total dan perlu di-restart manual.

**Kenapa ini keliru:** Penggunaan satu server untuk menangani seluruh fungsi sistem menjadi masalah ketika jumlah pengguna dan trafik semakin tinggi. Semua proses saling bergantung pada server yang sama. Jadi, ketika server mengalami masalah atau kehabisan sumber daya, seluruh bagian sistem juga ikut terdampak. Hal ini membuat sistem sulit untuk tetap berjalan ketika terjadi lonjakan trafik.

**Dampak ke FoodGo:** Karena menggunakan sumber daya dari satu server yang sama untuk semua modul, tidak ada pembagian beban atau pemisahan layanan, server bisa kehabisan kapasitas. Akibatnya sistem crash secara keseluruhan.

**Solusi desain awal:** Solusi yang dapat diterapkan adalah memisahkan modul-modul menjadi layanan terpisah (microservices) yang berjalan di server berbeda. Dengan begitu, jika satu layanan mengalami masalah, layanan lainnya tetap bisa berjalan. Selain itu, bagian yang memiliki beban tinggi, seperti layanan pesanan, bisa ditambah kapasitasnya secara mandiri tanpa harus ikut meningkatkan seluruh sistem.

**Trade-off:** Pemecahan sistem menjadi layanan terpisah meningkatkan kompleksitas pengelolaan infrastruktur, komunikasi jaringan antar-service, serta kesulitan dalam proses debugging dan deployment.

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: Latencty is Zero — ditulis oleh Steven Indramer
**Bukti di skenario:** "Aplikasi jadi sangat lambat, beberapa permintaan timeout modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu."

**Kenapa ini keliru:** Proses pemanggilan fungsi dalam memori lokal (in-memory function call) membutuhkan waktu dalam hitungan nanodetik, sedangkan pemanggilan layanan melalui jaringan memerlukan waktu milidetik (bahkan detik jika terdistribusi antar wilayah/cloud). Mengabaikan akumulasi waktu transit data di jaringan memicu desain sistem yang mengandalkan pemanggilan synchronous berantai (tight coupling).

**Dampak ke FoodGo:** Pengembang menulis alur bisnis secara synchronous yang berasumsi balasan dari modul pembayaran dan notifikasi kurir akan langsung diterima seketika. Pada lonjakan trafik, latensi jaringan meningkat tajam. Karena modul pesanan menunggu balasan dari modul pembayaran secara sinkron sebelum bisa membalas aplikasi pengguna, waktu respons (latency) ujung-ke-ujung bagi pengguna terakumulasi menjadi sangat tinggi hingga melampaui batas timeout di sisi aplikasi seluler/klien.

**Solusi desain awal:** 
Mengubah komunikasi berantai dari synchronous menjadi Asynchronous Event-Driven Architecture menggunakan Message Broker (seperti RabbitMQ atau Apache Kafka).
Ketika pesanan dibuat, modul pesanan menerbitkan event OrderCreated ke broker data dan langsung mengembalikan respons 202 Accepted ke aplikasi pengirim, lalu pemrosesan pembayaran serta notifikasi kurir dilakukan secara asynchronous di latar belakang (background job).

**Trade-off:** Arsitektur asynchronous meningkatkan kompleksitas sistem secara keseluruhan dan mengorbankan konsistensi seketika (immediate consistency) menjadi eventual consistency. Tim engineering perlu menangani skenario batas (edge cases), seperti penanganan konsistensi state jika pembayaran ternyata gagal setelah pesanan dikonfirmasi sementara ke pengguna.

---

## Kesimpulan Kelompok

<<<<<<< HEAD
[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.] -->
=======
Untuk mengatasi tiga pitfall utama, yaitu Single Point of Failure, double payment, dan masalah latency, FoodGo perlu mengubah arsitektur monolitik menjadi sistem yang lebih decoupled dan resilient.

Solusinya adalah menggunakan kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub). SOA memisahkan sistem menjadi beberapa service, sedangkan Pub-Sub mengurangi ketergantungan komunikasi langsung antar-service.
>>>>>>> 82338d3917fe192f1a5f3a67a22dff3f4c6504f0
