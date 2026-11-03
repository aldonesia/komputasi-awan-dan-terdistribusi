# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 9

| Nama | NIM | Kontribusi |
|---|---|---|
| Naufal Fudhail | 103072400013 | Pitfall 1 (The network is reliable) & Analisis |
| Diandra Nanditya Mulkis | 103072400075 | Pitfall 2 (Latency is zero) & Analisis |
| Samuel Nelson Wabiser | 103072400111 | Pitfall 3 (Monolithic) & Kesimpulan |

## Pitfall 1: Fallacy "The network is reliable" — ditulis oleh Naufal Fudhail

**Bukti di skenario:** Terdapat komentar pada kode yang berasumsi bahwa `# network is always reliable, no need for retry`.

**Kenapa ini keliru:** Dalam sistem terdistribusi nyata, jaringan tidak pernah 100% stabil. Sering terjadi latensi, *packet loss*, atau gangguan *router* terutama saat trafik sedang tinggi (seperti jam makan siang).

**Dampak ke FoodGo:** Karena tidak ada mekanisme coba ulang (*retry*), saat pesan dari aplikasi ke server gagal terkirim di tengah jalan, pesanan pelanggan akan *error* atau hilang. Pengguna hanya melihat layar *loading* yang berujung kegagalan.

**Solusi desain awal:** Menerapkan mekanisme **Retry dengan Exponential Backoff**. Jika permintaan gagal, sistem akan mencoba mengirim ulang dengan jeda waktu yang terus bertambah (misal 1 detik, lalu 2 detik, lalu 4 detik) sebelum akhirnya menyerah.

**Trade-off:** Risiko *cascading failure*. Jika banyak aplikasi klien melakukan *retry* secara bersamaan saat server sedang kewalahan (beban puncak), *retry* ini justru bertindak seperti serangan DDoS internal yang bisa membuat server *crash* total.

---

## Pitfall 2: Asumsi "Latency is zero" — ditulis oleh Diandra Nanditya Mulkis

**Bukti di skenario:** Modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu karena tidak ada *timeout* sama sekali pada pemanggilan antar *service*.

**Kenapa ini keliru:** Komunikasi antar-layanan melalui jaringan selalu memakan waktu. Mengasumsikan respons instan mengabaikan fakta bahwa layanan yang dipanggil (pembayaran) bisa melambat karena antrean *request* atau masalah koneksi.

**Dampak ke FoodGo:** Karena menunggu tanpa batas, antrean proses (*thread*) di server menumpuk saat modul pembayaran merespons lambat. Hal ini menguras *resource* server (CPU/RAM) hingga aplikasi melambat drastis dan menyebabkan *timeout* di sisi pengguna.

**Solusi desain awal:** Menerapkan **Timeout** pada setiap panggilan antar layanan. Jika layanan gagal merespons dalam batas waktu tertentu, sistem langsung membatalkan proses atau mengembalikan status gagal. Bisa juga dikombinasikan dengan pola **Circuit Breaker**.

**Trade-off:** Menentukan batas waktu *timeout* bisa jadi sulit. Jika *timeout* terlalu singkat, sistem bisa saja membatalkan transaksi yang sebenarnya berhasil diproses di modul pembayaran sehingga terjadi inkonsistensi data.

---

## Pitfall 3: Single Point of Failure (Arsitektur Monolitik) — ditulis oleh Samuel Nelson Wabiser

**Bukti di skenario:** Satu server menangani semua modul (pesanan, pembayaran, notifikasi kurir) dalam satu proses monolitik, yang membuatnya kewalahan saat trafik naik.

**Kenapa ini keliru:** Menggabungkan semua layanan dalam satu proses menghilangkan isolasi kegagalan. Kinerja dan ketahanan seluruh sistem menjadi bergantung penuh pada komponen yang paling rentan terhadap beban tinggi.

**Dampak ke FoodGo:** Lonjakan beban pada satu fitur (misal modul pembayaran) menghabiskan seluruh kapasitas CPU/RAM server. Akibatnya, modul lain yang tidak terkait langsung (seperti pencarian atau notifikasi kurir) ikut mati total (*crash*), melumpuhkan seluruh aplikasi.

**Solusi desain awal:** Melakukan pemisahan *service* secara bertahap (migrasi ke *Service-Oriented Architecture* atau *Microservices*). Modul pesanan, pembayaran, dan kurir dipisah ke layanan dan infrastruktur mandiri agar dapat di-*scale up* secara terpisah sesuai kebutuhan.

**Trade-off:** Kompleksitas sistem dan infrastruktur akan meningkat drastis. Tim *engineering* harus mengelola alur *deployment* yang lebih rumit, memonitor jaringan antar *service*, dan mengurus sinkronisasi *database* terdistribusi.

---

## Kesimpulan Kelompok

Jika FoodGo memperbaiki ketiga pitfall di atas, arsitektur yang disarankan secara garis besar adalah bertransisi dari sistem **Monolitik** menuju **Microservices** atau *Service-Oriented Architecture* (SOA). Dengan pemisahan ini, modul pesanan, pembayaran, dan notifikasi berjalan sebagai layanan independen. Isolasi ini memastikan bahwa lonjakan beban atau *crash* pada satu modul tidak akan melumpuhkan keseluruhan aplikasi.

Namun, karena arsitektur terdistribusi sangat bergantung pada komunikasi jaringan, sistem ini wajib mengadopsi prinsip *Design for Failure*. Setiap pemanggilan antar-*service* harus dilengkapi dengan jaring pengaman jaringan seperti **Timeout** yang tegas, **Retry dengan Exponential Backoff**, dan **Circuit Breaker**. Kombinasi antara arsitektur layanan yang terisolasi dan mekanisme toleransi kesalahan ini akan menjadi fondasi utama bagi FoodGo untuk masuk ke tahap perancangan arsitektur *cloud-native* yang sesungguhnya di Tugas 2.
