# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo _e-wallet_ pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1.  Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo _e-wallet_ jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).


Sistem e-wallet FoodGo tidak dapat hanya bergantung pada Eventual Consistency, melainkan memerlukan konsistensi urutan seperti Sequential Consistency atau kombinasi Eventual Consistency dengan jaminan Client-Centric Consistency (seperti Read-Your-Writes). Hal ini dikarenakan data finansial memiliki dampak bisnis yang sangat sensitif. Sebagai contoh, keterlambatan replikasi antar-server dapat menyebabkan false rejection, seperti pengguna di Jakarta yang gagal bertransaksi di server Bandung sesaat setelah melakukan top-up. Masalah ini memicu kerugian finansial, penurunan kepercayaan pengguna, hingga lonjakan aduan layanan pelanggan. Tanpa konsistensi urutan operasi di seluruh replika, risiko double spending juga dapat terjadi jika saldo yang sama dipakai bersamaan di lokasi berbeda sebelum sinkronisasi rampung—sebuah dampak yang jauh lebih kritis dibandingkan ketidakcocokan data sementara pada fitur non-kritis seperti jumlah like media sosial.



2.  Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. _Read-Your-Writes_: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
    
Pendekatan Client-Centric Consistency yang ideal untuk kasus ini adalah Read-Your-Writes Consistency serta opsi Monotonic Reads, yang memastikan pengguna yang baru melakukan top-up (write) dapat langsung membaca data saldo terbarunya meskipun mengakses replika server lain. Implementasinya memanfaatkan version token atau logical timestamp per pengguna, transaksi top-up di server Jakarta meningkatkan versi saldo dan meneruskan informasi versi_minimal ke sisi klien. Saat permintaan berikutnya masuk ke server Bandung, sistem akan membandingkan versi_lokal server dengan versi_minimal dari klien. Jika server Bandung tertinggal (versi_lokal < versi_minimal), sistem mencegah pembacaan data lama melalui beberapa strategi:

1. Mengalihkan (redirect) Query ke server Jakarta.
2. Menunggu sinkronisasi selesai (polling dengan timeout).
3. Menerapkan sticky session sementara pada load balancer agar kueri pengguna tetap mengarah ke server Jakarta hingga replikasi selesai.



3.  Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.
    <br>
    ```mermaid
    sequenceDiagram
    actor Pelanggan
    participant JKT as Server Jakarta
    participant Queue as Queue Replikasi
    participant BDG as Server Bandung

        Pelanggan->>JKT: Mengirim permintaan Top-Up<br/>Rp 50.000
        Note over JKT: Update & Respon<br/>memperbarui saldo lokal Rp 50.000
        JKT->>Queue: Mengirim event replikasi<br/>saldo (asinkron)
        JKT-->>Pelanggan: Success, TopUp<br/>Saldo Rp 50.000
        Note over Queue: Replikasi<br/>Replikasi tertunda / lambat (belum sampai ke Bandung)
        Pelanggan->>BDG: Pesan makanan & cek saldo
        Note over BDG: Titik Kegagalan<br/>Baca saldo lokal = Rp 0 (stale read)
        BDG-->>Pelanggan: Transaksi ditolak<br/>(saldo dianggap tidak cukup)
        Queue->>BDG: Update saldo Rp 50.000<br/>baru tiba (terlambat)
    ```
        Skenario Solusi

    ```mermaid
        sequenceDiagram
        actor Pelanggan
        participant JKT as Server Jakarta
        participant Queue as Queue Replikasi
        participant BDG as Server Bandung

        Pelanggan->>JKT: Mengirim permintaan Top-Up<br/>Rp 50.000
        Note over JKT: Update & Respon<br/>memperbarui saldo lokal Rp<br/>50.000 (Versi 1)
        JKT-->>Pelanggan: Success, TopUp<br/>Saldo Rp 50.000 (Versi 1)
        JKT->>Queue: Mengirim event replikasi<br/>saldo (Versi 1) Secara asinkron
        Note over Queue: Replikasi<br/>Replikasi tertunda / lambat (Server<br/>Bandung masih di versi_lokal = 0)
        Pelanggan->>BDG: Pesan makanan & cek saldo<br/>(Versi 1)
        Note over BDG: Titik Perbaikan<br/>Membandingkan versi_lokal (0) <<br/>versi_minimal (1) sehingga pembacaan<br/>saldo lama ditahan/dicegah.
        BDG->>JKT: Meneruskan (redirect)<br/>query cek saldo (versi >= 1)
        JKT-->>BDG: Mengembalikan saldo<br/>terbaru Rp 50.000 (versi = 1)
        BDG-->>Pelanggan: Transaksi berhasil<br/>(saldo Rp 50.000 cukup)
        Queue->>BDG: Replikasi versi = 1 tiba<br/>untuk menyinkronkan<br/>data lokal Bandung
    
    ```

    <br>
### Skenario Tambahan
Skenario dari perkembangana kami adalah dengan membutuhkan Sequential Consistency, Dalam skenario perebutan pesanan ojek online, sebuah pesanan berstatus available diakses hampir bersamaan oleh Pengemudi A melalui server Jakarta dan Pengemudi B melalui server Bandung. Jika sistem hanya menerapkan Eventual Consistency, latensi replikasi dapat menyebabkan server Bandung tetap menampilkan status pesanan lama (available) walau Pengemudi A telah mengambilnya di server Jakarta. Akibatnya, kedua pengemudi menerima konfirmasi berhasil untuk pesanan yang sama. Penerapan Read-Your-Writes saja tidak cukup menyelesaikan masalah ini karena konflik dipicu oleh dua pengguna berbeda yang melakukan operasi pembaruan (write) secara konkuren pada satu data yang sama. Oleh karena itu, skenario ini memerlukan Sequential Consistency agar seluruh replika menyepakati urutan eksekusi operasi secara identik (pesanan dikunci menjadi taken untuk pengemudi pertama, lalu klaim pengemudi kedua otomatis ditolak). Dari perspektif bisnis, konsistensi urutan ini krusial guna menghindari double assignment yang berujung pada kedatangan dua mitra di lokasi jemputan yang sama, pemborosan waktu dan biaya operasional, pembatalan sistem secara paksa, serta penurunan kepercayaan mitra maupun pelanggan.

### Diskusi pemilihan model konsistensi
Berdasarkan analisis perbandingan, Eventual Consistency unggul dalam hal latensi dan ketersediaan antar-wilayah, sedangkan Sequential Consistency menjamin keseragaman urutan operasi antar-replika dengan konsekuensi penambahan waktu sinkronisasi. Untuk data sensitif seperti saldo e-wallet, penggunaan Eventual Consistency murni terbukti terlalu berisiko karena keterlambatan replikasi dapat menyebabkan false rejection, double spending, dan rusaknya reputasi bisnis. Sebagai solusinya, sistem membutuhkan konsistensi urutan transaksi yang ketat atau integrasi replikasi asinkron dengan jaminan Read-Your-Writes (Client-Centric Consistency). Mekanisme ini memanfaatkan verifikasi versi data pengguna dan pengalihan pembacaan (redirect) ke server utama saat replika tertinggal, sehingga integritas data saldo tetap terjaga tanpa mengorbankan performa read secara global.

### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:

1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen                              | Bobot | Kriteria                                                          |
| ------------------------------------- | ----- | ----------------------------------------------------------------- |
| Ketepatan pemilihan model konsistensi | 30%   | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi      |
| Kualitas sequence diagram             | 30%   | Menunjukkan jelas titik kegagalan & titik perbaikan               |
| Usulan solusi client-centric          | 25%   | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok          | 15%   | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan)    |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
