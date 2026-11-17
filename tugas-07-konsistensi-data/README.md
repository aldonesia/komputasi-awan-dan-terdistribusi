# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).
2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

## JAWABAN

### 1. Model konsistensi yang dipilih

Kasus saldo e-wallet FoodGo **tidak cukup kalau hanya memakai Eventual Consistency**. Dengan Eventual Consistency, data di Jakarta dan Bandung memang akan sama pada akhirnya, tetapi selama replikasi belum selesai Bandung masih bisa menampilkan saldo lama. Akibatnya pelanggan yang baru top-up bisa ditolak saat memesan makanan, padahal saldonya cukup.

Dampak bisnisnya:
- Pelanggan kesal dan mengira uangnya hilang, lalu bisa pindah ke aplikasi lain.
- Jumlah komplain ke customer service bertambah.
- Karena menyangkut uang, kesalahan angka saldo lebih serius daripada data biasa.

Bandingkan dengan jumlah like di media sosial. Kalau like telat tampil beberapa detik, tidak ada yang dirugikan, jadi Eventual Consistency sudah cukup. Saldo berbeda karena itu uang asli dan sistem memakai angka itu untuk menerima atau menolak transaksi.

Di sisi lain, Sequential Consistency untuk semua data terlalu berat. Semua server harus saling menunggu supaya urutan operasinya sama, sehingga sistem jadi lebih lambat. Data seperti menu dan rating tidak perlu seketat itu.

**Kesimpulan:** replikasi tetap Eventual Consistency, tetapi untuk saldo ditambah jaminan Client-Centric Consistency, yaitu Read-Your-Writes.

### 2. Solusi Client-Centric: Read-Your-Writes

Read-Your-Writes artinya pelanggan yang baru menulis data harus bisa melihat hasil tulisannya sendiri. Cara kerjanya:

1. Setiap perubahan saldo diberi nomor versi (1, 2, 3, dst).
2. Setelah top-up berhasil, aplikasi pelanggan menyimpan nomor versi terakhirnya.
3. Saat pelanggan membaca saldo, aplikasi mengirim nomor versi itu ke server.
4. Server mengecek apakah versi datanya sudah sama atau lebih baru dari nomor tersebut.
   - Kalau sudah, saldo langsung ditampilkan.
   - Kalau belum (misalnya Bandung masih ketinggalan), server menunggu sebentar atau mengambil data dari Jakarta.

Dengan begitu pelanggan tidak akan melihat saldo lama setelah top-up, walaupun replikasi ke Bandung masih berjalan.

### 3. Sequence Diagram

**a. Tanpa jaminan konsistensi (bug terjadi)**

```mermaid
sequenceDiagram
    actor P as Pelanggan
    participant J as Server Jakarta
    participant B as Server Bandung

    P->>J: Top-up Rp50.000
    J->>J: Saldo jadi 50.000
    J-->>P: Top-up berhasil
    J--)B: Replikasi saldo (lambat)

    P->>B: Pesan makanan Rp30.000
    Note over B: Replikasi belum sampai, saldo masih 0
    B-->>P: Ditolak, saldo tidak cukup (BUG)
```

Titik kegagalan: Bandung menjawab memakai data lama karena replikasi dari Jakarta belum sampai.

**b. Dengan Read-Your-Writes (bug teratasi)**

```mermaid
sequenceDiagram
    actor P as Pelanggan
    participant J as Server Jakarta
    participant B as Server Bandung

    P->>J: Top-up Rp50.000
    J->>J: Saldo jadi 50.000 (versi 1)
    J-->>P: Berhasil, versi = 1
    J--)B: Replikasi saldo (lambat)

    P->>B: Pesan makanan (kirim versi_minimal = 1)
    Note over B: Cek versi: punya Bandung 0 < 1, ketinggalan
    B->>J: Ambil saldo terbaru
    J-->>B: Saldo 50.000 (versi 1)
    B-->>P: Saldo cukup, pesanan berhasil
```

Titik perbaikan: Bandung mengecek versi terlebih dahulu dan mengambil data dari Jakarta kalau ia ketinggalan.

### 4. Skenario tambahan: aplikasi ojek online

Driver menekan tombol "Selesai" di server Surabaya, tetapi penumpang melihat status lewat server Malang. Karena replikasi lambat, penumpang masih melihat status "dalam perjalanan" padahal perjalanan sudah selesai.

Model yang tepat dibedakan per data:
- **Posisi driver di peta:** cukup **Eventual Consistency**. Posisi yang telat 1-2 detik tidak merugikan siapa pun dan akan segera diperbarui.
- **Status perjalanan dan tarif:** perlu konsistensi yang lebih kuat (**Sequential Consistency** untuk urutan statusnya), karena menyangkut biaya yang ditagih. Status tidak boleh kembali dari "selesai" ke "dalam perjalanan".

Kesimpulannya, model konsistensi dipilih berdasarkan seberapa besar dampak bisnis kalau datanya telat atau salah.

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
