# Tugas 2: Perancangan Arsitektur Sistem FoodGo

**Kelompok:** [Kelompok 13]
**Anggota:** 
1. [Steven indamer]
2. [Delon Nicholas]

---

## 1. Pemilihan Gaya Arsitektur & Justifikasi

Untuk menyelesaikan masalah *tight-coupling* pada sistem monolitik FoodGo, kami memilih **kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub)**. 

**Justifikasi:**
* **SOA (Microservices):** Kami memecah monolit menjadi layanan terpisah (Pesanan, Pembayaran, Katalog, Kurir) agar tiap tim dapat melakukan *deploy* ulang tanpa menyebabkan *downtime* total. Interaksi yang membutuhkan respons instan dari pengguna (seperti melihat katalog dan membayar) ditangani secara sinkron (*request-response*).
* **Publish-Subscribe (Event-Driven):** Digunakan khusus untuk alur setelah pembayaran berhasil. Alur seperti notifikasi ke restoran dan pencarian kurir tidak perlu ditunggu oleh pengguna secara *real-time*. Dengan Pub-Sub melalui *Message Broker*, Service Pesanan tidak akan tertahan (*blocked*) jika Service Kurir sedang lambat atau *down*.

---

## 2. Diagram Arsitektur (End-to-End)

Diagram di bawah menunjukkan komponen utama beserta API Gateway dan Message Broker. 

```mermaid
graph LR
  Client[Pelanggan] -->|HTTP request pesan| OrderSvc[Service Pesanan]
  OrderSvc -->|RPC sinkron| PaymentSvc[Service Pembayaran]
  OrderSvc -->|publish event OrderCreated| Broker[(Message Broker)]
  Broker -->|subscribe| NotifSvc[Service Notifikasi Kurir]W
  Broker -->|subscribe| RestoSvc[Service Katalog Resto]
```

---

## 3. Penjelasan Alur Skenario Penuh (End-to-End)

## Penjelasan Alur Skenario End-to-End

Berikut adalah penjelasan alur satu skenario penuh mulai dari pelanggan membuat pesanan hingga resto dan kurir menerima notifikasi, berdasarkan diagram arsitektur di atas:

### 1. Pelanggan Membuat Pesanan
* **Komponen yang berkomunikasi:** `Client` (Pelanggan) $\rightarrow$ `OrderSvc` (Service Pesanan)
* **Pesan / Interaksi:** Pelanggan mengirimkan `HTTP request pesan` untuk membuat pesanan baru.
* **Jenis Komunikasi:** **Sinkron** (Pola *Request-Response*). Client menunggu balasan langsung dari Service Pesanan.

### 2. Pemrosesan Pembayaran
* **Komponen yang berkomunikasi:** `OrderSvc` (Service Pesanan) $\rightarrow$ `PaymentSvc` (Service Pembayaran)
* **Pesan / Interaksi:** Service Pesanan melakukan pemanggilan `RPC sinkron` ke Service Pembayaran untuk memvalidasi dan memotong saldo.
* **Jenis Komunikasi:** **Sinkron** (Pola *Request-Response*). Service Pesanan tertahan (*blocking*) sampai proses pembayaran selesai dan mengembalikan status.

### 3. Penerbitan Event Pesanan
* **Komponen yang berkomunikasi:** `OrderSvc` (Service Pesanan) $\rightarrow$ `Broker` (Message Broker)
* **Pesan / Interaksi:** Setelah pembayaran berhasil, Service Pesanan melakukan `publish event OrderCreated` ke Message Broker.
* **Jenis Komunikasi:** **Asinkron** (Pola *Event-Driven / Publish*). Service Pesanan tidak perlu menunggu proses lanjutan dari service lain (*non-blocking*).

### 4. Notifikasi ke Resto dan Kurir (Berjalan Paralel)
* **Komponen A:** `Broker` (Message Broker) $\rightarrow$ `RestoSvc` (Service Katalog Resto / Dapur)
  * **Pesan / Interaksi:** Service Katalog Resto melakukan `subscribe` ke Message Broker untuk menerima event `OrderCreated` agar restoran bisa mulai memasak.
  * **Jenis Komunikasi:** **Asinkron** (Pola *Event-Driven / Subscribe*).
* **Komponen B:** `Broker` (Message Broker) $\rightarrow$ `NotifSvc` (Service Notifikasi Kurir)
  * **Pesan / Interaksi:** Service Notifikasi Kurir melakukan `subscribe` ke Message Broker untuk menerima event `OrderCreated` agar sistem mulai menugaskan kurir terdekat.
  * **Jenis Komunikasi:** **Asinkron** (Pola *Event-Driven / Subscribe*).

---

### Tabel Ringkasan Komunikasi

| Langkah | Pengirim | Penerima | Pesan / Interaksi | Jenis Komunikasi | Pola Interaksi |
|---|---|---|---|---|---|
| **1** | `Client` | `OrderSvc` | HTTP request pesan | **Sinkron** | Request-Response |
| **2** | `OrderSvc` | `PaymentSvc` | RPC sinkron | **Sinkron** | Request-Response |
| **3** | `OrderSvc` | `Broker` | publish event `OrderCreated` | **Asinkron** | Event (Publish) |
| **4a** | `Broker` | `RestoSvc` | subscribe event | **Asinkron** | Event (Subscribe) |
| **4b** | `Broker` | `NotifSvc` | subscribe event | **Asinkron** | Event (Subscribe) |

---

## 4. Analisis Tertulis: Mengatasi Coupling & Trade-Off Arsitektur

### A. Mengapa Gaya Arsitektur Ini Mengatasi Masalah Coupling (Tugas 1)

Pada Tugas 1, FoodGo menggunakan arsitektur monolitik di mana semua modul berjalan dalam satu proses dan saling memanggil secara sinkron tanpa batas waktu (*no timeout*). Hal ini menyebabkan *tight coupling* dan *Single Point of Failure* (SPOF). 

Penerapan kombinasi **SOA (Microservices) + Publish-Subscribe** mengatasi masalah tersebut melalui:

1. **Isolasi Kegagalan (Fault Isolation):**
   * **Masalah Tugas 1:** Modul pesanan tertahan (*blocked*) menunggu modul pembayaran/kurir yang lambat, sehingga *thread pool* habis dan server *crash*.
   * **Solusi Arsitektur Baru:** Pemrosesan lanjut setelah pembayaran dilakukan secara asinkron via Message Broker. Jika `NotifSvc` (Service Kurir) atau `RestoSvc` (Service Resto) mengalami masalah atau *down*, `OrderSvc` (Service Pesanan) tetap dapat menerima dan menyelesaikan transaksi pembayaran dari pelanggan tanpa tertahan. Pesan `OrderCreated` akan tersimpan aman di dalam Message Broker sampai service tujuan aktif kembali.

2. **Independensi Deployment & Skalabilitas:**
   * **Masalah Tugas 1:** Perubahan kecil pada modul kurir mengharuskan seluruh aplikasi monolit di-*deploy* ulang dan menyebabkan *downtime* total.
   * **Solusi Arsitektur Baru:** Modul dipisah menjadi *service* terpisah yang berkomunikasi lewat antarmuka terdefinisi (API/Events). Tim Kurir dapat memperbarui atau melakukan *re-deploy* pada `NotifSvc` kapan saja tanpa perlu menghentikan `OrderSvc` atau `PaymentSvc`.

3. **Pemisahan Beban Kerja (Decoupled Workload):**
   * **Masalah Tugas 1:** Lonjakan trafik pesanan saat jam makan siang membuat seluruh proses monolitik kehabisan sumber daya CPU/Memori.
   * **Solusi Arsitektur Baru:** Setiap *service* dapat di-scale secara terpisah sesuai kebutuhan. Saat trafik melonjak, kita hanya perlu menduplikasi (*scale out*) `OrderSvc` tanpa perlu memboroskan sumber daya untuk memperbesar *instance* `PaymentSvc`.

---

### B. Analisis Trade-Off dan Kompleksitas Baru

Meskipun arsitektur ini berhasil menyelesaikan masalah *coupling*, penerapan SOA dan Pub-Sub membawa beberapa tantangan dan kompleksitas baru bagi tim engineering FoodGo:

1. **Kompleksitas Debugging dan Tracing (Alur Tidak Linear):**
   * **Tantangan:** Pada sistem monolitik, alur eksekusi bersifat linear dan berada dalam satu *call stack* log server. Pada pola Pub-Sub, setelah event `OrderCreated` dikirim ke Broker, alur eksekusi terpecah secara asinkron ke berbagai service. Jika pesanan tidak sampai ke restoran, tim sulit menentukan apakah masalah ada pada pemancar event, Message Broker, atau penerima event.
   * **Mitigasi:** Tim harus menerapkan **Distributed Tracing** (misal: Jaeger / Zipkin) dan menyertakan *Correlation ID* pada setiap event untuk melacak perjalanan satu transaksi di berbagai service.

2. **Konsistensi Data Seketika Hilang (*Eventual Consistency*):**
   * **Tantangan:** Data tidak lagi konsisten secara instan (*immediate consistency*). Ada jeda waktu (*latency*) antara saat pembayaran selesai dikonfirmasi dengan saat restoran menerima notifikasi pesanan.
   * **Mitigasi:** Tim harus merancang penanganan skenario kegagalan (*edge cases*), misalnya dengan menerapkan **Dead Letter Queue (DLQ)** pada Message Broker untuk menampung event yang gagal diproses oleh konsumen.

3. **Overhead Operasional & Infrastruktur Tambahan:**
   * **Tantangan:** Menambahkan komponen baru seperti Message Broker (misal: RabbitMQ) dan pemisahan service meningkatkan biaya operasional, kompleksitas pemeliharaan server, dan konfigurasi jaringan.
   * **Mitigasi:** Menggunakan *Managed Message Broker Service* di cloud untuk mengurangi beban pemeliharaan infrastruktur secara mandiri oleh tim internal.







