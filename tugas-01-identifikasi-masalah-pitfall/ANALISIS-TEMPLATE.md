# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** 1

| Nama                                  | NIM          | Kontribusi                          |
| ------------------------------------- | ------------ | ----------------------------------- |
| Yan Chrisdaniel Partogi rayano Ludjen | 103072400010 | pitfall 4 - Topology doesn't change |
| Bima Luthfi Nurhakim                  | 103072400030 | pitfall 1 - The network is reliable |
| Jeremy Joving Winargo                 | 103072400085 | pitfall 3 - Arsitektur Monolitik    |
| Ahmad Nur Fajri                       | 103072430007 | pitfall 2 - Latency is zero         |

## Pitfall 1: The network is reliable — ditulis oleh Bima Luthfi Nurhakim

**Bukti di skenario:** Tim menemukan bahwa kode mereka menulis asumsi seperti `# network is always reliable, no need for retry` dan tidak ada _timeout_ sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** Karena pada sistem terdistribusi, jaringan tidak selalu dapat diandalkan. Request dapat mengalami kegagalan atau gangguan sehingga keberhasilan komunikasi antar-service tidak selalu dapat dijamin. Bisa dilihat dari aplikasi yang menjadi sangat lambat dan beberapa permintaan timeout sehingga keberhasilan pengiriman request tidak selalu dapat terjamin. Karena itu, FoodGo seharusnya tidak mengasumsikan bahwa setiap komunikasi antar-service akan selalu berhasil.

**Dampak ke FoodGo:** Ketika trafik meningkat sebagian komunikasi antar service bisa gagal/ mengalami gangguan karena FoodGo tidak memiliki mekanisme retry, request yang gagal tidak dicoba kembali sehingga proses yang bergantung pada request tersebut dapat gagal meskipun gangguan jaringan hanya bersifat sementara.

**Solusi desain awal:** Menambahkan _retry_ untuk mencoba kembali request yang sebelumnya gagal, selain itu jumlah percobaan perlu dibatasi dengan memberikan jeda yang semakin panjang sebelum melakukan percobaan berikutnya.

**Trade-off:** _retry_ dapat menambah beban jaringan dan service tujuan, jika service sedang overload dan banyak request melakukan retry secara bersamaan. Kondisi ini dapat memperparah `cascading failure`, karena itu retry harus dibatasi dan menggunakan backoff

---

## Pitfall 2: Latency is zero — ditulis oleh Ahmad Nur Fajri

**Bukti di skenario:** Modul pesanan meminta modul pembayaran memproses transaksi, lalu menunggu jawabannya tanpa batas waktu. Saat makan siang atau promo, aplikasi melambat dan beberapa permintaan mengalami timeout. Berarti disini sudah nampak bahwa pembayaran tidak selalu bisa merespons dengan cepat.

**Kenapa ini keliru:** Modul pesanan dan pembayaran tidak bekerja sebagai satu langkah yang langsung selesai. Pembayaran perlu memproses transaksi dan mengirimkan hasilnya kembali. Saat banyak orang memesan sekaligus, proses ini bisa memakan waktu lebih lama. Jadi, sistem harus siap menghadapi jawaban yang terlambat.

**Dampak ke FoodGo:** Selama menunggu pembayaran, permintaan pesanan terus memakai sumber daya server, seperti thread dan koneksi. Jika banyak permintaan menunggu bersamaan, sumber daya untuk melayani pesanan lain ikut berkurang. Akibatnya, pesanan makin lambat, permintaan menumpuk, sebagian mengalami timeout, dan server bisa kehabisan sumber daya hingga crash.

**Solusi desain awal:** Beri batas waktu atau timeout pada permintaan dari modul pesanan ke pembayaran. Jika batas waktu habis, hentikan penantian dan memberitau pengguna bahwa pembayaran belum terkonfirmasi, bukan langsung menyatakan seperti pembayaran gagal atau berhasil. Batas waktunya perlu ditentukan berdasarkan target waktu respons FoodGo. Jika mencoba kembali permintaan, batasi jumlah percobaan dan beri jeda yang makin panjang. Disini tetap memastikan percobaan ulang tidak membuat pelanggan tertagih dua kali, misalnya dengan memakai ID transaksi yang sama. Jika pembayaran terus lambat, circuit breaker dapat menghentikan sementara permintaan baru ke pembayaran. jadi circuit breaker ini seperti menjeda sementara permintaan agar request tidak menumpuk.

**Trade-off:** Timeout membuat modul pesanan tidak menunggu terlalu lama, tetapi pembayaran mungkin sebenarnya berhasil meskipun jawabannya terlambat. Karena itu, FoodGo perlu menyediakan cara untuk memeriksa status pembayaran sebelum meminta pelanggan mencoba lagi. Selain itu, terlalu banyak percobaan ulang bisa menambah beban pada pembayaran yang sedang lambat.

---

## Pitfall 3: Arsitektur Monolitik (SPOF) — ditulis oleh Jeremy Joving Winargo

**Bukti di skenario:** "Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama."

**Kenapa ini keliru:** Karena arsitektur monolitik menghalangi fault isolation, sehingga disaat satu modul mengalami lonjakan beban akan berdampak pada modul yang lain, dan juga menghalangi scaling boundary, setiap modul memiliki beban yang berbeda tetapi berada di satu server yang sama, sehingga kita tidak bisa menambah kapasitas kepada modul yang membutuhkan saja,tetapi harus menduplikasi keseluran monolit secara tidak efisien

**Dampak ke FoodGo:** terjadinya lonjakan trafik pada modul pesanan atau masalah pada modul notifikasi akan memakan CPU dan memori di sever yang sama. sehingga, modul lain yang seharusnya sehat seperti modul pembayaran ikut melambat. Terjadi Single point of failure yang mewajibkan restart secara keseluruhan

**Solusi desain awal:** memisahkan arsitektur monolitik menjadi beberapa bagian kecil(microservices) yang terpisah.Tempatkan tiap service di dalam container yang dapat di-skala secara horizontal berdasarkan beban trafik. 

**Trade-off:** dengan memecah arsitektur monolitik menjadi microseervices, akan menambah beban operasional, membutuhkan infrastruktur pemantauan,serta menjaga konsistensi data antar database terpisah menjadi rumit

---

## Pitfall 4: Topology doesn't change — ditulis oleh Yan Chrisdaniel Partogi Rayano Ludjen

**Bukti di skenario:** Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

**Kenapa ini keliru:** Dengan meningkatnya trafik atau perubahan kebutuhan sistem, kondisi dan struktur jaringan bisa mengalami perubahan. FoodGo tidak dapat mengandalkan jumlah server, koneksi, atau susunan komponen sistem yang selalu konstan, terutama saat terjadi peningkatan pesanan.

**Dampak ke FoodGo:** Saat trafik meningkat, satu server tidak lagi dapat menangani seluruh beban, menyebabkan kelebihan beban. Jika FoodGo menambah server atau mengatur ulang pembagian layanan untuk mengatasi beban ini, komunikasi antar komponen mungkin akan mengalami perubahan. Tanpa desain yang fleksibel untuk menyesuaikan diri dengan perubahan tersebut, aplikasi berisiko menjadi lambat, mengalami timeout, hingga server bisa crash.

**Solusi desain awal:** Merancang arsitektur yang mampu menyesuaikan diri dengan perubahan topologi, seperti dengan memanfaatkan load balancer dan service discovery, memungkinkan permintaan dialihkan ke server atau layanan yang tersedia ketika jumlah instance mengalami perubahan.

**Trade-off:** Pemanfaatan load balancer dan service discovery memang meningkatkan kompleksitas serta jumlah komponen yang perlu dikelola. Jika terjadi masalah pada komponen-komponen ini, proses penemuan atau pengarahan layanan juga bisa terkena dampaknya.

---

## Kesimpulan Kelompok
FoodGo dapat memisahkan layanan pesanan, pembayaran, dan notifikasi agar berjalan di beberapa instance. maka dari kasus ini load balancer untuk membagi trafik dan service discovery untuk menemukan layanan yang aktif. lalu menambahkan timeout, retry terbatas dengan jeda bertahap serta circuit breaker agar layanan lambat tidak membuat permintaan menumpuk.
