# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo

**Materi terkait:** Architectural style (Layered, SOA, Peer-to-Peer, Publish-Subscribe).

## Studi Kasus

Melanjutkan Tugas 1: FoodGo butuh sistem yang **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui/deploy ulang. Saat ini semua modul (pesanan, pembayaran, notifikasi kurir, katalog resto) berjalan sebagai satu aplikasi monolitik — sekali deploy, semua modul ikut restart dan berisiko downtime total.

## Tugas Kelompok

1. Pilih **satu** gaya arsitektur utama: **Service-Oriented Architecture (SOA)** atau **Publish-Subscribe**. Boleh dikombinasikan (mis. SOA untuk service inti + Pub-Sub untuk notifikasi), tapi harus dijustifikasi kenapa kombinasi ini yang dipilih.
2. Gambarkan minimal 4 komponen berikut dan interaksinya: modul Pesanan, modul Pembayaran, modul Kurir/Notifikasi, modul Katalog Resto (dan message broker/API gateway jika relevan).
3. Jelaskan alur satu skenario penuh secara end-to-end di diagram (misalnya: pelanggan buat pesanan → bayar → resto terima notifikasi → kurir ditugaskan) — tunjukkan komponen mana berkomunikasi dengan siapa, dan **jenis komunikasinya** (sinkron/asinkron, request-response/event).
4. Analisis tertulis: kenapa gaya ini mengatasi masalah *coupling* dari Tugas 1, dan apa trade-off-nya (mis. Pub-Sub menambah kompleksitas debugging karena alur tidak linear).

## Cara Membuat Diagram (Gratis, Cukup Laptop)

Tidak perlu software berbayar. Dua opsi:

**Opsi A — Mermaid di dalam Markdown (disarankan).** Ditulis sebagai teks biasa di `README.md`, otomatis dirender jadi diagram oleh GitHub — tidak perlu install apa pun.

````markdown
```mermaid
graph LR
  Client[Pelanggan] -->|HTTP request pesan| OrderSvc[Service Pesanan]
  OrderSvc -->|RPC sinkron| PaymentSvc[Service Pembayaran]
  OrderSvc -->|publish event OrderCreated| Broker[(Message Broker)]
  Broker -->|subscribe| NotifSvc[Service Notifikasi Kurir]
  Broker -->|subscribe| RestoSvc[Service Katalog Resto]
```
````

**Opsi B — draw.io / diagrams.net** (gratis, jalan di browser tanpa akun, atau app desktop offline di [app.diagrams.net](https://app.diagrams.net/)). Ekspor sebagai `.png` dan simpan di folder `diagram/`.

## Struktur Submission

```
tugas-02-perancangan-arsitektur/
├── README.md          # Analisis + diagram Mermaid (jika Opsi A) atau referensi ke diagram/
├── JURNAL.md
└── diagram/            # File .png/.drawio jika pakai Opsi B
```

## Rubrik Penilaian (Tugas 2)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan gaya arsitektur | 20% | Justifikasi SOA/Pub-Sub sesuai kebutuhan *decoupling* di skenario |
| Kelengkapan & kejelasan diagram | 30% | Semua komponen kunci ada, jenis komunikasi (sinkron/asinkron) jelas ditandai |
| Analisis trade-off | 30% | Bukan hanya kelebihan — kekurangan/kompleksitas baru juga dibahas |
| Proses & kontribusi kelompok | 20% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh memakai AI untuk brainstorming komponen apa saja yang umum ada di gaya arsitektur SOA/Pub-Sub; **tidak boleh** meminta AI menggambar diagram final atau menuliskan analisis trade-off yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Diagram Mermaid/draw.io yang "terlalu generik" (identik dengan contoh tutorial di internet tanpa penyesuaian ke kasus FoodGo) akan dinilai rendah pada komponen kelengkapan & kejelasan diagram.

## Jawaban Tugas Kelompok

1. Gaya Arsitektur

Kami memilih menggunakan kombinasi **Service-Oriented Architecture (SOA)** dan **Publish-Subscribe**. SOA digunakan untuk memisahkan sistem FoodGo menjadi beberapa service berdasarkan fungsinya, seperti Pesanan, Pembayaran, Katalog Resto, serta Kurir dan Notifikasi. Dengan pemisahan tersebut, setiap service dapat dikembangkan dan dikelola secara lebih independen.

Sementara itu, **Publish-Subscribe** digunakan untuk menangani komunikasi berbasis event, seperti ketika pesanan berhasil dibuat atau pembayaran berhasil dilakukan. Event tersebut dapat dikirim melalui message broker dan diterima oleh service yang membutuhkan, sehingga antar-service tidak terlalu bergantung secara langsung. Kombinasi keduanya dipilih karena dapat membantu FoodGo mengurangi ketergantungan antar modul sekaligus membuat sistem lebih fleksibel untuk dikembangkan.

2. 
```mermaid
graph LR
  Client[Pelanggan] -->|HTTP request| OrderSvc[Service Pesanan]

  OrderSvc -->|Sync: request pembayaran| PaymentSvc[Service Pembayaran]
  PaymentSvc -->|Sync: payment response| OrderSvc

  OrderSvc -->|Async: publish OrderPaid| Broker[(Message Broker)]

  Broker -->|Async: subscribe OrderPaid| RestoSvc[Service Katalog Resto]
  Broker -->|Async: subscribe OrderPaid| CourierSvc[Service Kurir / Notifikasi]

  RestoSvc -->|Konfirmasi pesanan| Broker
  CourierSvc -->|Penugasan kurir| Broker
  ```

  3. ### Alur end-to-end
    1. Pelanggan membuat pesanan
       Pelanggan mengirim request ke Service Pesanan menggunakan komunikasi sinkron/request. Service Pesanan menerima data pesanan dan memprosesnya.
    2. Service Pesanan meminta pembayaran
       Service Pesanan berkomunikasi dengan Service Pembayaran secara sinkron dengan pola request-response. Service Pesanan mengirim permintaan pembayaran, kemudian Service Pembayaran mengembalikan respons apakah
       pembayaran berhasil atau gagal.
    3. Pembayaran berhasil > event dipublikasikan
       Setelah pembayaran berhasil, Service Pesanan mempublikasikan event OrderPaid ke Message Broker. Komunikasi ini bersifat asinkron/event, sehingga Service Pesanan tidak perlu menunggu setiap service penerima
       menyelesaikan prosesnya.
    4. Katalog/Resto menerima event
       Service Katalog Resto melakukan subscribe terhadap event yang relevan melalui Message Broker. Ketika OrderPaid diterima, informasi tersebut dapat digunakan untuk proses penerimaan pesanan di sisi resto. Ini
       merupakan komunikasi asinkron berbasis event.
    5. Kurir/Notifikasi menerima event
       Service Kurir/Notifikasi juga melakukan subscribe melalui Message Broker. Setelah menerima event, service tersebut dapat memproses informasi pesanan untuk kebutuhan notifikasi atau proses penugasan kurir. 
       Komunikasinya juga asinkron/event.
    Secara keseluruhan, komunikasi antara Pelanggan–Pesanan dan Pesanan–Pembayaran menggunakan pola sinkron, sedangkan komunikasi setelah pembayaran menggunakan event secara asinkron melalui Message Broker.

  4. ### Analisis Arsitektur

Penggunaan SOA dan Publish-Subscribe dapat mengurangi coupling pada FoodGo karena proses pesanan, pembayaran, katalog restoran, dan kurir dipisahkan menjadi beberapa service. Contohnya, setelah pelanggan melakukan pembayaran, Service Pesanan mengirim event `OrderPaid` melalui Message Broker. Event tersebut kemudian dapat diterima oleh Service Katalog Resto dan Service Kurir/Notifikasi tanpa Service Pesanan harus berkomunikasi langsung dengan keduanya. Dengan begitu, perubahan pada satu service tidak terlalu berdampak pada alur FoodGo secara keseluruhan.

Trade-off-nya, sistem menjadi lebih kompleks karena harus mengelola beberapa service dan Message Broker. Selain itu, debugging lebih sulit karena komunikasi asynchronous membuat alurnya tidak selalu berjalan secara langsung. Misalnya, jika event `OrderPaid` gagal diproses, perlu dicek service dan komunikasi mana yang mengalami masalah.

