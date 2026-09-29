# Jurnal Proses — Tugas 2

## Informasi Kelompok
- **Anggota 1:** Naufal Fudhail (103072400013)
- **Anggota 2:** Diandra Nanditya Mulkis (103072400075)
- **Anggota 3:** Samuel Nelson Wabiser (103072400111)

## 28 September 2026
- **Opsi arsitektur yang dipertimbangkan:** Kami mempertimbangkan antara menggunakan murni SOA (semua service berkomunikasi via REST API sinkron) atau memadukannya dengan arsitektur *Event-Driven* (Publish-Subscribe) melalui bantuan Message Broker.
- **Kenapa akhirnya pilih Kombinasi SOA dan Pub-Sub:** Jika hanya memakai SOA murni, ketika modul Kurir mati atau lambat, modul Pesanan harus menunggunya (*blocking*) sehingga pelanggan akan merasa aplikasi *lag*. Kami memutuskan untuk menggunakan SOA hanya untuk transaksi pembayaran (yang butuh respon instan), dan Pub-Sub untuk notifikasi ke resto dan pencarian kurir.
- **Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):** Pada diagram awal (versi 1), kami membuat Modul Pesanan mengirim *request* HTTP langsung ke Modul Resto dan Modul Kurir secara berurutan. Di versi 2, kami menyisipkan `Message Broker` di tengahnya. Perubahan ini dilakukan agar Modul Pesanan tidak perlu menunggu respon dari Resto dan Kurir, melainkan hanya perlu "melempar" event ke Broker dan selesai. Hal ini sepenuhnya menghilangkan *coupling* antar layanan operasional.

## 29 September 2026
- Menyelesaikan *draft* analisis *trade-off* untuk `README.md`.
- Melakukan pengecekan akhir terhadap sintaks diagram Mermaid agar dapat di-*render* dengan baik di GitHub.

## Log Penggunaan AI (Level 2 - Bantuan Brainstorming)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 28 Sept 2026 | Gemini | Apa saja komponen umum yang biasanya ada jika sebuah aplikasi pesan antar makanan dipisah menjadi arsitektur SOA dan Pub-Sub? | AI menyarankan pemisahan menjadi API Gateway, Service Pesanan, Service Pembayaran (SOA), serta penggunaan Message Broker (Kafka/RabbitMQ) untuk menghubungkan Service Resto dan Kurir (Pub-Sub). | Kami berdiskusi dan menyetujui struktur ini karena logis. Kami mendesain sendiri hubungan antar komponennya ke dalam diagram Mermaid, memastikan label komunikasi (sinkron/asinkron) sesuai pemahaman kelompok. |
| 28 Sept 2026 | Gemini | Apa trade-off umum dari menggunakan Message Broker dalam sistem e-commerce? | AI menyebutkan masalah kompleksitas *debugging*, *eventual consistency*, dan beban pemeliharaan infrastruktur (*overhead*). | Saran ini kami gunakan sebagai kerangka. Kami kemudian merumuskan ulang analisis *trade-off* tersebut dengan bahasa sendiri, dan mengaitkannya secara spesifik dengan konteks *troubleshooting* skenario FoodGo di `README.md`. AI tidak menuliskan analisis akhir kami. |
## Log Penggunaan AI (Level 2)



