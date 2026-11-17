# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).
2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.


### jawaban — Analisis
1.Sistem e-wallet FoodGo tidak harus menggunakan Sequential Consistency pada semua server.Model Eventual Consistency lebih masuk akal karena memungkinkan replikasi data antar server (Jakarta dan Bandung) berjalan secara asinkron tanpa memblokir sistem utama, sehingga performa tetap optimal.
Tetapi, dilihat dari dampak bisnisnya, kasus saldo e-wallet sangat sensitif dan jauh berbeda dengan sekadar "jumlah like" di media sosial. Mengandalkan Eventual Consistency saja berisiko menimbulkan stale read (membaca saldo lama). Jika pelanggan berpindah server dalam hitungan detik setelah top-up, transaksi pembelian bisa ditolak karena saldo di server tujuan belum ter-update, yang berakibat fatal pada kepercayaan pengguna dan kerugian bisnis.


2.Karena Eventual Consistency murni tidak cukup, kami mengusulkan penerapan Client-Centric Consistency menggunakan model Read-Your-Writes.
Pendekatan ini memastikan pelanggan selalu melihat saldo terbarunya sendiri. Klien akan melacak versi data dari transaksi terakhirnya. Jika klien mengakses server yang versi datanya masih tertinggal (stale), sistem akan menahan respons (polling) hingga replikasi selesai dan versinya sesuai, barulah saldo ditampilkan.

3.

#### A. Skenario Tanpa Jaminan Konsistensi (Terjadi Bug)

```mermaid
sequenceDiagram
    participant C as Pelanggan (Client)
    participant J as Server Jakarta
    participant B as Server Bandung

    C->>J: 1. Top-up Saldo (mis. Rp50.000)
    J-->>C: 2. Transaksi Sukses & Saldo tersimpan (Versi 1)
    
    note over J,B: Proses replikasi berjalan lambat (Tertunda 2 detik)
    J-x B: 3. Replikasi data tertunda
    
    C->>B: 4. Pesan makanan (Baca saldo dari Bandung)
    B-->>C: 5. Mengembalikan saldo Rp0 (Stale Read)
    
    note over C: BUG: Saldo terbaca Rp0. Transaksi ditolak!
    
    note over J,B: Beberapa saat kemudian...
    B-->>B: 6. Replikasi dari Jakarta akhirnya masuk

```

#### B. Skenario Dengan Solusi (Read-Your-Writes)

```mermaid
sequenceDiagram
    participant C as Pelanggan (Client)
    participant J as Server Jakarta
    participant B as Server Bandung

    note over C,B: Saldo Awal: Rp50.000 (Versi 1)
    
    C->>J: 1. Top-up Tambahan (Rp20.000)
    note over J: Saldo menjadi Rp70.000 (Versi 2)
    J-->>C: 2. Transaksi Sukses (Client menyimpan target minimal: Versi >= 2)
    
    note over J,B: Proses replikasi berjalan lambat (Tertunda 2 detik)
    J-x B: 3. Replikasi data tertunda
    
    C->>B: 4. Pesan makanan (Meminta data dengan syarat Versi >= 2)
    
    note over B: Sistem mendeteksi Bandung masih Versi 1 (Stale)
    note over B: Sistem menahan proses (Polling / Menunggu sinkronisasi)
    
    note over J,B: Replikasi akhirnya tiba dari Jakarta
    B-->>B: 5. Bandung menerima update (Saldo = Rp70.000, Versi = 2)
    
    note over B: Versi terpenuhi. Data aman dibaca.
    B-->>C: 6. Mengembalikan saldo Rp70.000 (Read-Your-Writes)
    
    note over C: SOLUSI: Saldo terbaca akurat. Transaksi berhasil diproses!
    ```
---
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

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.
