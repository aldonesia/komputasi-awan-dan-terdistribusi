# Jurnal Proses — Tugas 2

## [Tanggal]
- Untuk opsi arsitektur awalnya kita mempertimbangkan untuk memilih keduanya tapi untuk sistem yang terlalu kompleks ini, kami memilih Pub-sub untuk seluruh arsitektur sistem kami, karena kita memperkirakan untuk system ini jika traffic penggunaannya meningkat akan memperparah server kami, dan juga kami mengadopsi dari atsitektur tokopedia yang menggunakan pub-sub
- Versi 2
````mermaid 
graph TD
    Client([Pelanggan / Mobile App])

    subgraph Entrypoint [API]
        Gateway[API Gateway]
    end

    subgraph Publisher
        P1[Pesanan]
        P2[Pembayaran]
    end

    subgraph Message_Broker [Message Broker - Kafka / RabbitMQ]
        TopicOrder{Topic: 'order-created'}
        TopicPayment{Topic: 'payment-success'}
    end

    subgraph Subscribers
        Q1[Modul Katalog Resto]
        Q2[Modul Notifikasi & Kurir]
    end

    %% Pemesanan
    Client -->|Memesan makanan via HTTP POST| Gateway
    Gateway -->|Mengirimkan request pesanan| P1

    %% Event Order Dibuat
    P1 -->|Mempublish 'order-created'| TopicOrder
    TopicOrder -->|Mengantarkan event ke pembayaran| P2

    %% Pembayaran
    Client -.->|Membayar dengan beberapa metode pembayaran| P2
    P2 -->|Mempublish 'payment-success'| TopicPayment

    %% Penyaluran Event ke Resto dan Kurir
    TopicPayment -->|Kirim ke modul resto agar dibuatkan makanan| Q1
    TopicPayment -->|Mencari driver & kirim notifikasi| Q2
````
Versi 1
````mermaid 
graph LR
    subgraph Publisher
        P1[Checkout / Order Service]
    end

    subgraph Message_Broker [Message Broker - Kafka / RabbitMQ]
        Topic{Topic: 'order-events'}
    end

    subgraph Subscribers
        S1[Warehouse Inventory Service]
        S2[Invoice & Billing Service]
        S3[Notification Service - WhatsApp/Email]
        S4[Analytics Stream Engine]
    end

    P1 -->|Publish: 'order_paid'| Topic
    Topic -->|Deliver event| S1
    Topic -->|Deliver event| S2
    Topic -->|Deliver event| S3
    Topic -->|Deliver event| S4
````
untuk versi pertama kita hanya menambahkan 1 message broker dan kami mengetahui bahwa notifikasi ke ojol juga harus dan pembayaran juga harus menambahkan message broker
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26/09/2026 | Gemini | Saya membuat rancangan diagram untuk menggambarkan interaksi modul Pesanan, Pembayaran, Kurir/Notifikasi, Katalog Resto, dan Message Broker. Rancangan awal saya menggunakan Mermaid dan memiliki alur Pesanan → Pembayaran → Message Broker → Katalog Resto. Apakah rancangan tersebut sudah sesuai dengan instruksi soal: menggambarkan minimal 4 komponen, menjelaskan satu skenario penuh end-to-end, dan jenis komunikasi? | AI menyarankan bahwa rancangan awal sudah memiliki konsep dasar yang benar, tetapi masih perlu diperbaiki. Modul Kurir/Notifikasi seharusnya menjadi komponen tersendiri dan bukan nama topic. Modul Katalog Resto dan Modul Kurir perlu menerima event `payment-success`. Diagram juga perlu membedakan komunikasi sinkron dan asinkron. | Saya menggunakan saran tersebut sebagai bahan brainstorming. Saya kemudian memperbaiki rancangan dengan menambahkan API Gateway, Modul Pesanan, Modul Pembayaran, Message Broker, Modul Katalog Resto, dan Modul Kurir/Notifikasi, menampilkan 4 modul wajib, serta memperjelas jenis komunikasinya (Sinkron/REST vs Asinkron/Event Pub-Sub). |
| 29/09/2026 | Gemini | Meminta bantuan brainstorming dengan peran Principal Software Architect untuk menganalisis pemecahan ketergantungan (Deployment & Fault Isolation) dan trade-off arsitektur Pub-Sub/Event-Driven pada sistem FoodGo, serta meminta 3 pertanyaan reflektif untuk panduan penulisan tugas. | AI menyusun kerangka logika (A -> B -> C) mengenai Spatial dan Temporal Decoupling, membedah trade-off teknis seperti *Eventual Consistency*, *Idempotency*, dan *Distributed Tracing*, serta memberikan 3 pertanyaan studi kasus kritis (Saga Pattern, UI/UX delay, duplikasi pesan). | Saya menjadikan kerangka tersebut sebagai *sounding board* untuk menyusun draf analisis pada laporan akhir (Tugas 4). Terminologi teknis saya gunakan sebagai referensi, dan saya menjawab 3 pertanyaan reflektif dari AI dengan argumen saya sendiri untuk memperdalam pembahasan sistem terdistribusi di laporan. |
