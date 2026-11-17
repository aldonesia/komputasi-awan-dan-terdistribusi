# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
1. sistem ini membutuhkan jaminan konsistensi yang lebih ketat, yakni mengarah pada Sequential Consistency (semua replika melihat urutan operasi yang sama) dibanding Eventual consistency (replika akan konsisten "pada akhirnya", boleh sementara berbeda),
Argumen dampak bisnis : Pada kasus "jumlah like" di media sosial, keterlambatan sinkronisasi selama beberapa detik dapat ditoleransi karena tidak berdampak secara finansial maupun hukum (eventual consistency memadai). Sebaliknya, pada e-wallet, saldo adalah representasi aset finansial riil. Jika replika server Bandung lambat menerima pembaruan dari server Jakarta (seperti pada kasus top-up gagal terbaca), transaksi pelanggan akan ditolak secara salah. Hal ini memicu frustrasi pengguna dan dapat menurunkan kepercayaan pada platform FoodGo, serta berpotensi menimbulkan kerugian bisnis akibat transaksi yang gagal diproses.

2. pendekatan yang paling efisien dan ramah pengguna adalah Read-Your-Writes Consistency.

- Cara Kerja Solusi:
Pelanggan yang baru saja melakukan top-up saldo melalui server Jakarta akan membaca data saldo terbaru mereka sendiri ketika melakukan checkout pesanan berikutnya di server manapun, meskipun replika latar belakang ke server lain belum sepenuhnya selesai menyebar.

- Implementasi Konseptual:
Setiap klien diberi version timestamp atau penanda sesi lokal. Ketika klien melakukan write (top-up), timestamp disimpan. Saat klien melakukan read (cek saldo/pesan makanan) di server lain, server tersebut akan memeriksa apakah data lokalnya sudah setidaknya setara dengan timestamp klien (server asal)? jika belum, server akan menunggu (fetch) data terbaru dari server asal terlebih dahulu agar data saldo klien sesuai.

- Kesimpulan akhir & alasan: Solusi Efektif (Client-Centric / Read-Your-Writes):
Dengan menggunakan pendekatan Read-Your-Writes, saat klien membawa token versi terbaru hasil top-up, server lokal yang belum sinkron akan otomatis menarik data terbaru (fetch) dari server asal terlebih dahulu. Hal ini memastikan saldo selalu valid bagi si pemilik akun, transaksi berhasil diproses, dan performa sistem secara keseluruhan tetap cepat. Hal ini berarti read your writes menjadi solusi untuk mengatasi proses pemindahan data secara efisien dibanding tanpa jaminan konsistensi.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: 
1. Skenario Naif (Pendekatan Tanpa Jaminan Konsistensi)
Pada skenario ini, replikasi data saldo berjalan di latar belakang dengan adanya delay jaringan. Ketika pengguna melakukan top-up di server Jakarta sebesar Rp. 50.000 lalu langsung melakukan pembacaan (checkout) di server Bandung sebelum replikasi selesai, terjadilah inkonsistensi data.
Dampak Sistem: Server Bandung masih membaca saldo lama (Rp0) karena data dari Jakarta belum sampai. Akibatnya, transaksi pesanan makanan pelanggan akan ditolak (false rejection).

2. Skenario Read-Your-Writes Consistency (Pendekatan Solusi)
Pada skenario ini, sistem menerapkan validasi berbasis versi/token klien. Ketika klien melakukan checkout di server Bandung dengan membawa token terbaru, server Bandung mendeteksi adanya ketertinggalan data dan langsung melakukan sinkronisasi paksa (fetch) ke server asal (Jakarta) sebelum memproses transaksi.
Dampak Sistem: Server Bandung berhasil memperbarui datanya secara instan dengan menarik informasi dari sumber kebenaran utama (source of truth), sehingga saldo pelanggan terbaca secara valid (Rp70.000) dan transaksi pesanan makanan berhasil diproses tanpa hambatan.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|17 November 2026| Gemini AI | Berikan kesimpulannya pada skenario ini| Berikut adalah kesimpulan ringkas mengenai skenario replikasi data saldo e-wallet FoodGo dan solusi konsistensinya: Akar Masalah (Replication Lag): Penyebaran saldo hasil top-up dari server asal (Jakarta) ke server regional lain (Bandung) membutuhkan waktu sejenak (background replication). Jika pelanggan langsung melakukan checkout sebelum proses replikasi selesai, server Bandung masih membaca saldo lama yang menyebabkan transaksi sah ditolak secara keliru (false rejection). Kebutuhan Bisnis: Karena menyangkut aset finansial dan kepercayaan pengguna, sistem e-wallet tidak cukup hanya mengandalkan Eventual Consistency. Sistem membutuhkan jaminan agar mutasi saldo krusial dapat langsung diakses oleh pengguna yang bersangkutan tanpa jeda. Solusi Efektif (Client-Centric / Read-Your-Writes): Alih-alih membebani seluruh jaringan dengan sinkronisasi ketat global yang lambat, digunakan pendekatan Read-Your-Writes. Melalui mekanisme ini, jika klien membawa token versi terbaru hasil top-up, server lokal yang belum sinkron akan otomatis menarik data terbaru (fetch) dari server asal terlebih dahulu. Hal ini memastikan saldo selalu valid bagi si pemilik akun, transaksi berhasil diproses, dan performa sistem secara keseluruhan tetap cepat serta andal.| Dengan menggunakan pendekatan Read-Your-Writes, saat klien membawa token versi terbaru hasil top-up, server lokal yang belum sinkron akan otomatis menarik data terbaru (fetch) dari server asal terlebih dahulu. Hal ini memastikan saldo selalu valid bagi si pemilik akun, transaksi berhasil diproses, dan performa sistem secara keseluruhan tetap cepat. Hal ini berarti read your writes menjadi solusi untuk mengatasi proses pemindahan data secara efisien dibanding tanpa jaminan konsistensi.|
