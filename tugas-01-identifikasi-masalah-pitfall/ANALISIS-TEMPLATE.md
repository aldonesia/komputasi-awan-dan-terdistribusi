# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Ardian Hoart| 103072400098 | pitfall 1 |
| Muhammad Yusuf Ar Rahman | 103072400143 | pitfall 2 |
| [Ardian Hoart] | 103072400098 | pitfall 3 |

## Pitfall 1: Bandwidth is infinite — ditulis oleh Ardian Hoart

**Bukti di skenario:** Saat trafik naik, satu server yang menangani semua modul menjadi kewalahan.

**Kenapa ini keliru:** Server tidak memiliki resource yang tidak terbatas. CPU, RAM, koneksi, dan kemampuan server dalam memproses request semuanya memiliki batas. Jika jumlah pengguna meningkat secara tiba-tiba, server bisa kewalahan karena harus memproses terlalu banyak request dalam waktu yang bersamaan.

**Dampak ke FoodGo:** Saat jam makan siang atau ada promo besar, jumlah pengguna FoodGo meningkat dan banyak request masuk secara bersamaan. Karena semua modul seperti pesanan, pembayaran, dan notifikasi berjalan pada satu server, beban server menjadi terlalu tinggi. Akibatnya aplikasi menjadi lambat dan server bisa mengalami crash.

**Solusi desain awal:** FoodGo dapat menggunakan horizontal scaling, yaitu menambah beberapa server atau instance untuk membagi beban. Request dari pengguna dapat dibagi menggunakan load balancer. Untuk proses yang tidak harus langsung selesai, FoodGo juga dapat menggunakan message queue agar pekerjaan diproses secara bertahap.

**Trade-off:** Menambah server dapat membantu mengurangi beban pada satu server, tetapi biaya infrastruktur menjadi lebih besar. Selain itu, sistem juga menjadi lebih kompleks karena harus mengatur beberapa server dan melakukan monitoring terhadap masing-masing server.

---

## Pitfall 2: Latency is zero — ditulis oleh Muhammad Yusuf Ar Rahman

**Bukti di skenario:** Modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu karena tidak ada timeout pada pemanggilan antar service.

**Kenapa ini keliru:** Komunikasi antar service tidak selalu memiliki waktu respons yang sama. Service pembayaran bisa mengalami keterlambatan karena beban yang tinggi, masalah jaringan, atau sedang mengalami gangguan. Karena itu, sistem tidak boleh menganggap bahwa respons dari service lain akan selalu datang dengan cepat.

**Dampak ke FoodGo:** Saat trafik FoodGo meningkat, banyak request pesanan dapat memanggil modul pembayaran secara bersamaan. Jika modul pembayaran mengalami keterlambatan, request dari modul pesanan akan terus menunggu karena tidak memiliki timeout. Jika jumlah request yang menunggu semakin banyak, resource server seperti thread dan koneksi dapat ikut terpakai sehingga aplikasi menjadi semakin lambat dan pada kondisi tertentu dapat mengalami timeout atau crash.

**Solusi desain awal:** FoodGo dapat menerapkan timeout pada komunikasi antara modul pesanan dan pembayaran sehingga request tidak menunggu selamanya. Selain itu, circuit breaker dapat digunakan untuk menghentikan sementara pemanggilan ke service pembayaran ketika service tersebut terus mengalami kegagalan atau terlalu lambat.

**Trade-off:** Timeout dapat menyebabkan beberapa transaksi dianggap gagal atau belum selesai meskipun service pembayaran sebenarnya masih memprosesnya. Sementara itu, retry dapat membantu ketika terjadi gangguan sementara, tetapi jika dilakukan terlalu banyak saat service sedang overload, retry justru dapat menambah beban dan memperparah masalah.

---

## Pitfall 3: the network is reliable — ditulis oleh Ardian Hoart

**Bukti di skenario:** network is always reliable, no need for retry

**Kenapa ini keliru:** Dalam sistem terdistribusi, koneksi antar-service tidak selalu berjalan dengan baik. Bisa saja terjadi koneksi terputus, request gagal, atau service yang dituju tidak memberikan respons. Karena itu, sistem harus bisa menangani kemungkinan tersebut.

**Dampak ke FoodGo:**Jika komunikasi dengan service pembayaran mengalami gangguan, modul pesanan bisa tidak mendapatkan respons. Hal ini dapat membuat proses pesanan gagal dan pengguna mendapatkan error atau harus mencoba kembali.

**Solusi desain awal:**FoodGo bisa menambahkan retry dengan jumlah percobaan yang terbatas dan menggunakan exponential backoff. Selain itu, dapat ditambahkan timeout dan circuit breaker agar request tidak terus dikirim ke service yang sedang bermasalah.

**Trade-off:**Retry dapat membantu ketika gangguan hanya sementara. Namun, jika dilakukan terlalu sering, request tambahan justru bisa membuat beban server semakin tinggi dan memperparah masalah.

---

## Kesimpulan Kelompok

Berdasarkan ketiga pitfall yang dibahas, FoodGo perlu memiliki sistem yang lebih fleksibel dan tidak bergantung pada satu server. Beberapa modul dapat dipisahkan agar beban kerja bisa dibagi, kemudian menggunakan load balancer untuk mengatur trafik. Untuk komunikasi antar-service, dapat ditambahkan timeout, retry, dan circuit breaker. Dengan cara ini, FoodGo dapat lebih siap menghadapi trafik tinggi maupun gangguan pada salah satu service.
