# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Materi terkait:** *Architectural style* (*Layered*, SOA, *Peer-to-Peer*, *Publish-Subscribe*).

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok

1. Pilih **satu** gaya arsitektur utama: **Service-Oriented Architecture (SOA)** atau **Publish-Subscribe**. Boleh dikombinasikan (mis. SOA untuk service inti + Pub-Sub untuk notifikasi), tapi harus dijustifikasi kenapa kombinasi ini yang dipilih.
2. Gambarkan minimal 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway jika relevan).
3. Jelaskan alur satu skenario penuh secara end-to-end di diagram (misalnya: pelanggan buat pesanan → bayar → resto terima notifikasi → kurir ditugaskan) — tunjukkan komponen mana berkomunikasi dengan siapa, dan **jenis komunikasinya** (sinkron/asinkron, request-response/event).
4. Analisis tertulis: kenapa gaya ini mengatasi masalah *coupling* dari Tugas 1, dan apa trade-off-nya (mis. Pub-Sub menambah kompleksitas debugging karena alur tidak linear).


## Tugas 2 — Perancangan Arsitektur FoodGo


### 1. Gaya Arsitektur yang Dipilih
Sebelum menentukan arsitektur yang cocok, kami ingin membahas apa itu SOA dan Pub-Sub.

SOA (*Service-Oriented Architecture*) adalah gaya arsitektur yang memecah sistem menjadi beberapa layanan atau *service* terpisah yang saling memanggil lewat jaringan.

Sedangkan *Publish-Subscribe* (Pub-Sub) yaitu gaya komunikasi di mana pengirim (*publisher*) menyiarkan pesan ke saluran tertentu, dan pihak yang berminat (*subscriber*) menerimanya, tanpa keduanya saling mengenal.

Dari kedua definisi di atas, kami memilih *arsitektur kombinasi* yaitu **SOA untuk service inti dan Publish-Subscribe untuk notifikasi dan koordinasi, asinkron.** Adapun penjelasannya sebagai berikut.



| Bagian sistem | Gaya | Komunikasi | Alasan |
|---|---|---|---|
| Client → API Gateway → Service | SOA (REST) | Sinkron, *request-response* | Klien butuh jawaban langsung |
| Order → Katalog (cek menu/harga) | SOA | Sinkron, *request-response*, *timeout* | Validasi harus selesai sebelum menu valid |
| Order → Payment | SOA | Sinkron, *request-response*, *timeout* + *retry* + *idempotency key* | Hasil pembayaran harus pasti sebelum pesanan lanjut  |
| Order → Resto, Kurir, Notifikasi pelanggan | Publish-Subscribe | Asinkron, *event* | Order tidak perlu tahu siapa penerimanya dan tidak boleh gagal hanya karena penerima sedang down |

#### Justifikasi kenapa kami memilih arsitektur kombinasi

- Opsi 1: SOA: Jika Order memanggil Kurir dan Resto secara sinkron, Order akan tetap bergantung pada ke keduanya (*coupled*) sehingga jika salah satu dari keduanya sedang ada kendala, maka Order akan gagal. Contoh: saat service Kurir sedang *update* versi aplikasi atau *deploy* ulang, pesanan pelanggan ikut gagal. Jadi jika menggunakan solusi ini akan mengulang masalah monolit dalam bentuk lain.

- Opsi 2: Pub-Sub. Pembayaran butuh kepastian hasil sebelum pesanan dilanjutkan. Kalau dibuat *event* murni/asinkron, alur menjadi kacau dan sulit dikontrol tepat di titik yang paling sensitif (uang). Contoh: saat *user* menekan tombol bayar, *event* pembayaran terkirim. Namun misalkan *user* ingin membatalkan pembayaran dengan menekan tombol batalkan pembayaran, ada kemungkinan *event* pembatalan pembayaran lebih cepat diproses oleh sistem sehingga sistem/alurnya menjadi kacau dan bahkan uang *user* tetap terpotong.
- PIlihan kami: Kombinasi SOA+Pub-Sub. Alur yang butuh jawaban langsung memakai *request-response*, dan setiap panggilannya diberi *timeout* dan *retry* terbatas. Alur yang berupa "beri tahu pihak lain bahwa sesuatu terjadi" memakai *event* atau Pub-Sub.


## 2. Diagram Komponen
- Garis solid = komunikasi sinkron (request-response).
- Garis putus-putus = komunikasi asinkron (event via broker).

```mermaid
graph LR
  Client[Pelanggan] -->|HTTP request pesan| OrderSvc[Service Pesanan]
  OrderSvc -->|RPC sinkron| PaymentSvc[Service Pembayaran]
  OrderSvc -.->|publish event OrderCreated| Broker[(Message Broker)]
  Broker -.->|subscribe| NotifSvc[Service Notifikasi Kurir]
  Broker -.->|subscribe| RestoSvc[Service Katalog Resto]
```
## 3. Skenario *End-to-End*: Pelanggan Pesan → Bayar → Resto Menerima → Kurir Ditugaskan
 
```mermaid
sequenceDiagram
  autonumber
  actor P as Pelanggan
  participant GW as API Gateway
  participant O as Service Pesanan
  participant K as Service Katalog Resto
  participant Pay as Service Pembayaran
  participant B as Message Broker
  participant C as Service Kurir dan Notifikasi
  participant N as Service Notifikasi Pelanggan
 
  P->>GW: POST /orders (REST, sinkron)
  GW->>O: teruskan permintaan (sinkron)
  O->>K: GET /menu (validasi menu dan harga, sinkron)
  K-->>O: menu valid
  O->>Pay: POST /payments (sinkron)
  Pay-->>O: pembayaran sukses
  O-->>GW: 201 pesanan dibuat, status PAID
  GW-->>P: konfirmasi pesanan
 
  Note over O,B: Sejak titik ini komunikasi ASINKRON (event)
  O-->>B: publish OrderPaid
  B-->>K: OrderPaid (Resto menerima notifikasi pesanan)
  K-->>B: publish RestoAccepted (setelah resto konfirmasi)
  B-->>C: RestoAccepted
  C->>C: pilih kurir terdekat yang tersedia
  C-->>B: publish CourierAssigned
  B-->>N: CourierAssigned
  N-->>P: push notifikasi kurir sedang menuju resto
```
### Penjelasan
 
| # | Dari → Ke | Jenis | Pola |
|---|---|---|---|
| 1 | Pelanggan → API *Gateway* → *Service* Pesanan | Sinkron | *Request-response* (REST, HTTP method POST) |
| 2 | *Service* Pesanan → *Service* Katalog | Sinkron | *Request-response* (GET) |
| 3 | *Service* Pesanan → *Service* Pembayaran | Sinkron | *Request-response* (POST) |
| 4 | *Service* Pesanan → Broker (`OrderPaid`) | Asinkron | *Event*, *publish* |
| 5 | Broker → Katalog Resto / Kurir | Asinkron | *Event*, *subscribe* |
| 6 | Katalog Resto → Broker (`RestoAccepted`) | Asinkron | *Event, publish* |
| 7 | Service Kurir → Broker (`CourierAssigned`) → Notifikasi Pelanggan | Asinkron | *Event, publish/subscribe* |

## 4. Analisis
- Kenapa Gaya Ini Mengatasi Masalah Coupling?
 
1. *Deploy* independen yang membuat tidak ada lagi *restart* sistem secara massal sehingga menyebabkan *downtime* total. Contoh: Tim kurir men-*deploy* ulang *Service* Kurir tanpa mengubah dan tidak menyebabkan Service Pesanan atau Katalog terganggu.
2. Isolasi kegagalan yang membuat sistem tetap berjalan dengan baik (namun butuh beberapa waktu untuk memprosesnya, setidaknya tidak mati total) walaupun ada satu modul yang mati. Jika *Service* Kurir mati, Order tetap menerima dan menyimpan pesanan. Event `OrderPaid` menunggu di broker dan diproses ketika Kurir hidup kembali. Pada monolit, satu modul mati/gagal akan menjatuhkan keseluruhan sistem.
3. *Coupling* longgar (*loose coupling*). Publisher tidak tahu siapa subscriber-nya. Menambah subscriber baru (misalkan layanan analitik atau promo) tidak mengubah kode Service Pesanan karena cukup membuat service baru dan mendaftarkannya (*subscribe*) ke *Message Broker* untuk mendengarkan *event* OrderCreated yang sudah ada sejak dulu.
4. Beban *publisher* ringan. Publisher cukup mengirim *event* ke channel broker (broadcast) dan tidak menunggu semua penerima memproses.
5. *Scaling* per kebutuhan. Saat jam makan siang, Service Pesanan dan Kurir bisa diperbanyak dengan membuat salinan program yang sedang berjalan tanpa ikut menggandakan Service Katalog.
6. Kesesuaian dengan kebutuhan *real-time*. Notifikasi ke resto dan kurir lewat *event* membuat latensi rendah, sehingga sistem dapat memenuhi sifat *real-time* (delay kecil).

- **Trade-off** 
 
| Trade-off | Penjelasan | Mitigasi |
|---|---|---|
| *Debugging* lebih sulit | Alur pesanan tidak lagi linear: satu pesanan melewati banyak service dan event. Sulit melacak "event ini di mana macetnya". | *Correlation ID* (order_id) di semua log dan event, *distributed tracing*, log terpusat |
| *Message broker* jadi bagian paling penting | Jika broker mati, alur event terhenti (*single point of failure*). | Broker dalam mode *cluster/replikasi, health check* |
| Konsistensi akhir (*eventual consistency*) | Status pesanan di *service* berbeda tidak langsung sama di detik yang sama. | Desain UI yang menampilkan status "diproses", model status yang jelas |
| Pesan ganda / gagal terkirim | *Event* bisa terkirim lebih dari sekali atau gagal diproses *subscriber*. | *Consumer idempotent*, *retry* dengan batas, *dead-letter queue* |
| Latensi jaringan pada panggilan sinkron | Panggilan Order → Payment/Katalog kini lewat jaringan, bukan pemanggilan fungsi lokal, sehingga rentan lambat atau putus (kembali ke *Fallacies of Distributed Computing*). | *Timeout*, *retry*, *circuit breaker* |
| Kompleksitas operasional | Banyak service, banyak database, broker, dan gateway yang harus di-deploy dan dipantau. | Container (Docker) dan orkestrasi (Docker Swarm/Kubernetes) untuk mengelola banyak container |
| Transaksi lintas service | Tidak ada satu transaksi database untuk "bayar + buat pesanan + kabari resto"; kegagalan di tengah alur harus dikompensasi. | Status pesanan eksplisit (PENDING, PAID, dst.), langkah kompensasi/refund |
| Overhead untuk tim kecil | Untuk aplikasi kecil, *microservice* bisa berlebihan dibanding monolit. | Migrasi bertahap dengan memecah modul yang paling sering berubah lebih dulu (misal Kurir dan Notifikasi) |


## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh memakai AI untuk brainstorming komponen apa saja yang umum ada di gaya arsitektur SOA/Pub-Sub; **tidak boleh** meminta AI menggambar diagram final atau menuliskan analisis trade-off yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Diagram Mermaid/draw.io yang "terlalu generik" (identik dengan contoh tutorial di internet tanpa penyesuaian ke kasus FoodGo) akan dinilai rendah pada komponen kelengkapan & kejelasan diagram.
