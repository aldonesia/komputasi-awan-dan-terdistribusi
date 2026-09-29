<!-- # Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Kelompok 13

| Nama | NIM | Kontribusi |
|---|---|---|
| [nama 1] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

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

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]


---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.] -->
