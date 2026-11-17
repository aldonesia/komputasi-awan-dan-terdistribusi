# Studi Kasus FoodGo — Konsistensi Saldo E-Wallet

## Bagian 1 — Analisis

### 1. Sequential Consistency atau Eventual Consistency?

**Kesimpulan: kasus saldo e-wallet membutuhkan Sequential Consistency (untuk operasi pada data saldo). Eventual Consistency saja tidak cukup.**

Argumen berbasis dampak bisnis:

| Aspek | Dampak jika saldo hanya Eventual Consistency |
|---|---|
| **Kepercayaan pelanggan** | Pelanggan baru saja top-up (uangnya sudah terpotong dari rekening), tetapi pesanan ditolak karena "saldo tidak cukup". Ini terlihat seperti uang hilang dan sangat merusak kepercayaan. |
| **Kehilangan pendapatan** | Setiap transaksi yang ditolak karena data basi adalah penjualan yang gagal, dan pelanggan bisa pindah ke kompetitor. |
| **Beban operasional** | Lonjakan komplain ke customer service, proses refund/investigasi manual, dan reputasi buruk di app store. |
| **Risiko finansial (lebih berbahaya)** | Replikasi lambat bisa terjadi ke arah sebaliknya: saldo sudah dipakai di Jakarta, tetapi Bandung masih melihat saldo lama, sehingga pelanggan bisa membayar dua kali dengan saldo yang sama (*double spending*) dan saldo menjadi negatif. |
| **Kepatuhan** | Data keuangan harus dapat diaudit dan urutan transaksinya harus jelas. |

Pembanding: pada kasus "jumlah like" di media sosial, angka yang tertinggal beberapa detik tidak merugikan siapa pun, sehingga Eventual Consistency sudah cukup. Pada saldo, **kesalahan membaca berarti kesalahan keputusan uang**.

Mengapa **Sequential Consistency** (bukan sekadar eventual): semua replika harus melihat urutan operasi yang sama pada saldo (misalnya `top-up +50.000` lalu `bayar -35.000`). Dengan begitu tidak ada replika yang memproses `bayar` seolah-olah `top-up` belum terjadi.

Trade-off (CAP/latensi): menjaga urutan yang sama lintas kota menambah latensi karena tulis saldo harus dikoordinasikan (misalnya lewat primary per akun atau quorum). Untuk saldo, harga ini layak dibayar (pilih **C** dibanding **A** saat terjadi partisi). Untuk data non-kritis seperti rating, rekomendasi, dan jumlah pesanan, FoodGo tetap boleh memakai Eventual Consistency agar cepat dan tersedia.

### 2. Pendekatan Client-Centric Consistency yang relevan

Jika Eventual Consistency tidak cukup, kombinasi jaminan sisi klien yang diusulkan:

- **Read-Your-Writes (utama)**: pelanggan yang baru top-up selalu melihat saldo terbarunya sendiri, walaupun replika Bandung belum sinkron.
- **Monotonic Reads (pendukung)**: setelah pelanggan melihat saldo versi N, pembacaan berikutnya tidak boleh menampilkan versi yang lebih lama dari N (saldo tidak "mundur" saat berpindah server).

Cara implementasi (sederhana):

1. Setiap write saldo menghasilkan **versi/timestamp (version token)** yang dikembalikan ke klien.
2. Klien menyertakan token itu pada setiap request berikutnya (*session token*).
3. Server yang menerima request hanya melayani jika replikanya sudah mencapai versi tersebut. Jika belum, server **menunggu replikasi** sebentar atau **meneruskan (forward) pembacaan ke server yang sudah punya data** (misalnya Jakarta).

Catatan: Read-Your-Writes memperbaiki bug pada skenario ini. Untuk mencegah double spending antar-sesi, operasi **debit** tetap harus melewati penulisan yang berurutan (satu primary per akun), sesuai jawaban nomor 1.

### 3. Sequence Diagram

#### a. Tanpa jaminan konsistensi (bug terjadi)

```mermaid
sequenceDiagram
    actor C as Pelanggan
    participant J as Server Jakarta
    participant B as Server Bandung
    participant R as Proses Replikasi

    C->>J: Top-up Rp100.000 (WRITE)
    J->>J: Saldo = Rp100.000 (sebelumnya Rp0)
    J-->>C: Top-up berhasil
    J-)R: Kirim update saldo (asinkron, lambat)

    Note over C,B: Beberapa detik kemudian, aplikasi tersambung ke Bandung

    C->>B: Pesan makanan Rp60.000 (READ saldo)
    B->>B: Baca saldo lokal = Rp0 (belum ter-update)
    B-->>C: DITOLAK: saldo tidak cukup (BUG)

    R--)B: Update saldo Rp100.000 tiba (terlambat)
    B->>B: Saldo = Rp100.000
```

#### b. Dengan solusi Read-Your-Writes (bug teratasi)

```mermaid
sequenceDiagram
    actor C as Pelanggan
    participant J as Server Jakarta
    participant B as Server Bandung
    participant R as Proses Replikasi

    C->>J: Top-up Rp100.000 (WRITE)
    J->>J: Saldo = Rp100.000, versi = v7
    J-->>C: Berhasil + session token (versi v7)
    J-)R: Kirim update saldo v7 (asinkron)

    Note over C,B: Aplikasi tersambung ke Bandung

    C->>B: Pesan makanan Rp60.000 + token (min. versi v7)
    B->>B: Cek versi lokal = v6 < v7 (replika belum cukup baru)

    alt Replikasi sudah tiba dalam batas waktu tunggu
        R--)B: Update saldo v7
        B->>B: Versi lokal = v7, saldo = Rp100.000
    else Replikasi masih tertunda
        B->>J: Teruskan READ saldo (versi >= v7)
        J-->>B: Saldo = Rp100.000 (v7)
    end

    B->>B: Saldo cukup, proses debit Rp60.000, versi = v8
    B-->>C: Pesanan DITERIMA, sisa saldo Rp40.000 + token v8
```

---

## Bagian 2 — Skenario Tambahan: Aplikasi Ojek Online ("OjekGo")

### Deskripsi skenario

OjekGo menjalankan dua server regional, **Server A (Surabaya)** dan **Server B (Malang)**, dengan replikasi antar server yang berjalan lambat. Seorang penumpang memesan ojek. Order yang sama ditampilkan ke beberapa driver di sekitar lokasi penjemputan, yang aplikasinya bisa tersambung ke server yang berbeda.

Kasus nyata: **Driver 1** menekan "Terima Order" lewat Server A. Dalam hitungan detik, **Driver 2** (tersambung ke Server B) juga melihat order itu masih berstatus "tersedia" karena replikasi belum sampai, lalu menekan "Terima Order". Akibatnya satu order diterima dua driver: penumpang bingung, salah satu driver datang percuma, dan pendapatan serta reputasi aplikasi dirugikan.

Data di aplikasi ini punya tingkat sensitivitas berbeda, sehingga model konsistensinya pun tidak sama:

| Data | Sensitivitas | Model konsistensi yang tepat | Alasan |
|---|---|---|---|
| **Penugasan driver ke order** (siapa yang menerima order) | Tinggi | **Sequential Consistency** (semua replika melihat urutan "terima order" yang sama, yang pertama menang) | Satu order hanya boleh dimiliki satu driver. Jika urutan operasi berbeda antar replika, terjadi *double assignment*. |
| **Status order di layar penumpang** (mencari driver → driver ditemukan → dalam perjalanan → selesai) | Menengah | **Client-Centric: Monotonic Reads** | Status tidak boleh "mundur" bagi penumpang, misalnya sudah melihat "driver ditemukan" lalu pindah server dan melihat "mencari driver" lagi. |
| **Riwayat/order yang baru saja dibuat penumpang** | Menengah | **Client-Centric: Read-Your-Writes** | Penumpang yang baru memesan harus langsung melihat ordernya di aplikasi, walaupun replika lain belum sinkron. |
| **Posisi driver di peta** (titik yang bergerak) | Rendah | **Eventual Consistency** | Lokasi berubah tiap detik dan selalu ditimpa data baru. Tertinggal 1–3 detik tidak berbahaya dan mengutamakan kecepatan dan ketersediaan. |
| **Rating dan jumlah order selesai driver** | Rendah | **Eventual Consistency** | Selisih sementara tidak berdampak ke transaksi. |

### Model konsistensi utama yang dipilih: Sequential Consistency untuk penugasan driver

**Argumen berbasis dampak bisnis:**

- **Kepuasan penumpang:** dua driver menuju titik yang sama membuat penumpang bingung dan membatalkan order.
- **Kepuasan dan penghasilan driver:** driver yang kalah "balapan" sudah menempuh perjalanan dan menolak order lain, sehingga waktu dan bensinnya terbuang. Driver bisa keluar dari platform.
- **Biaya operasional:** dibutuhkan kompensasi/insentif dan penanganan komplain manual.
- **Eventual Consistency tidak cukup**, karena pada fase "replika belum sinkron" itulah bug terjadi, dan konflik tidak bisa diperbaiki setelah kedua driver sudah berangkat.

**Trade-off:** operasi "terima order" harus dikoordinasikan (misalnya lewat satu *primary* per order atau *compare-and-set* dengan versi), sehingga latensinya sedikit lebih tinggi. Hal ini dapat diterima karena operasi ini hanya terjadi sekali per order, sedangkan data lokasi yang sangat sering berubah tidak ikut dikoordinasikan.

### Sequence diagram

#### a. Tanpa jaminan konsistensi (bug: satu order diterima dua driver)

```mermaid
sequenceDiagram
    actor D1 as Driver 1
    participant A as Server A (Surabaya)
    participant B as Server B (Malang)
    participant R as Proses Replikasi
    actor D2 as Driver 2

    D1->>A: Terima Order #123 (WRITE)
    A->>A: Order #123 = milik Driver 1
    A-->>D1: Order diterima
    A-)R: Replikasi status order (asinkron, lambat)

    D2->>B: Terima Order #123 (WRITE)
    B->>B: Status lokal masih "tersedia"
    B->>B: Order #123 = milik Driver 2
    B-->>D2: Order diterima (BUG)

    R--)B: Update "milik Driver 1" tiba (terlambat)
    Note over A,B: Konflik: dua driver mengira order #123 miliknya
```

#### b. Dengan Sequential Consistency (bug teratasi)

```mermaid
sequenceDiagram
    actor D1 as Driver 1
    participant A as Server A (Surabaya)
    participant P as Primary order #123
    participant B as Server B (Malang)
    actor D2 as Driver 2

    D1->>A: Terima Order #123
    A->>P: Klaim order #123 (compare-and-set, versi v1)
    P->>P: Urutan #1: milik Driver 1, versi = v2
    P-->>A: Berhasil
    A-->>D1: Order diterima

    D2->>B: Terima Order #123
    B->>P: Klaim order #123 (versi v1)
    P->>P: Urutan #2: versi sudah v2, ditolak
    P-->>B: Gagal, order sudah diambil Driver 1
    B-->>D2: Order sudah diambil driver lain

    P--)A: Replikasi urutan operasi yang sama (v2)
    P--)B: Replikasi urutan operasi yang sama (v2)
```
