# Jurnal Proses — Tugas 1


## [21-09-2026]
- Peserta: Ida Ayu Putri S. B. dan I Wayan Juanesa R. P.
- Poin diskusi: 
    - Nentuin pitfall yang mana aja dulu
    - Tugek nemu pitfall the network is reliable dan latency is zero
    - Di bagian yang "# network is always reliable, no need for retry" langsung ketahuan kalau ada yang salah, karena pada soal dikatakan adanya kendala pada aplikasi tapi ini malah dibilang selalu berjalan dengan balik
    - Pada bagian "tidak ada timeout sama sekali pada pemanggilan antar service" juga langsung ketahuan bahwa ada yang salah di latency nya
    - Ryan menemukan 2 pitfal lain yaitu "Single Point of Failure" dan "Always-On Assumption"
    - pada soal terlihat "satu server yang menangani semua modul(...)kewalahan" disini juga sudah dibilang satu server menangani semua modul sehingga menemukan pitfal Single Point of Failure
    - untuk bagian "Server backend kadang *crash* total dan perlu di-restart manual." setelah saya brainstroming ke AI mengenai kemungkinan pitfal yang cocok dan saya menemukan pitfal Always-On Assumption
- Perbedaan pendapat (jika ada): ...

## [22-09-2026]
- Peserta: Ida Ayu Putri S. B. dan I Wayan Juanesa R. P.
- Poin diskusi: 
    - Belajar cara githubnya karena masih bingung dan ada sedikit error
    - Pastiin lagi semua analisisnya udah bener, cek lagi solusi yang kita kasi udah sesuai sama ketentuan yang diminta

## Review Silang
- [Ryan] mengomentari analisis [Tugek]: Dari yang sudah saya liat hasil dari analisis punya tugek, sudah sesuai dengan hasil diskusi kita di awal tidak adanya yang melenceng secara tiba-tiba dan di buat dengan sebaik mungkin
- [Tugek] mengomentari analisis [Ryan]: Kalau saya lihat, semua permasalahan yang ditemukan ryan sudah sesuai dan juga solusinya sudah seperti ketentuan yang ada pada soal

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang Diberikan | Ringkasan Saran / Ide AI | Bagaimana Diolah Jadi Tulisan / Kode Sendiri |
| :--- | :--- | :--- | :--- | :--- |
| 20-09-2026 | Gemini | Jelaskan maksud dari semua pitfall ini, karena saya masih asing dan belum terlalu paham: "the network is reliable", "latency is zero", "bandwidth is infinite", "the network is secure", "topology doesn't change", "there is one administrator", "transport cost is zero", "the network is homogeneous". | Menjelaskan 8 *Fallacies of Distributed Computing*:<br>1. *The network is reliable* (Jaringan selalu andal)<br>2. *Latency is zero* (Waktu tunggu jaringan nol)<br>3. *Bandwidth is infinite* (Kapasitas jaringan tanpa batas)<br>4. *The network is secure* (Jaringan pasti aman)<br>5. *Topology doesn't change* (Struktur jaringan tidak berubah)<br>6. *There is one administrator* (Hanya ada satu admin)<br>7. *Transport cost is zero* (Biaya kirim data gratis)<br>8. *The network is homogeneous* (Semua perangkat/sistem seragam) | Dijadikan landasan pemahaman awal untuk menganalisis dan menemukan kasus Pitfall 1 dan Pitfall 2 pada skenario. |
| 21-09-2026 | ChatGPT | Apa itu pitfall? | Pitfall adalah asumsi atau kondisi yang awalnya dianggap aman/benar, tetapi ternyata dapat menyebabkan masalah saat terjadi kondisi tertentu di sistem. | Digunakan untuk memahami konsep dasar *pitfall* sebelum memulai analisis tugas. |
| 21-09-2026 | ChatGPT | Bantu saya melakukan brainstorming untuk mengidentifikasi potensi pitfall dari: "Server backend kadang *crash* total dan perlu di-restart manual. Kenapa begitu?" | Menjelaskan kesalahan asumsi bahwa server akan selalu aktif (*Always-On Assumption*). Saat terjadi *crash*, sistem tidak punya mekanisme pemulihan otomatis sehingga bergantung pada *restart* manual. | Dirumuskan menjadi analisis Pitfall 3: Sistem tidak boleh mengasumsikan server selalu aktif dan tidak boleh bergantung pada *restart* manual oleh manusia. |
| 21-09-2026 | ChatGPT | Jika satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama, apa solusi dan *trade-off* yang cocok? | **Solusi:** Memisahkan modul paling berat menjadi beberapa *service* dan menggunakan *queue* untuk proses asinkron.<br>**Trade-off:** Kompleksitas pengelolaan dan komunikasi antarservice meningkat, tetapi beban server terbagi dan lebih tahan lonjakan trafik. | Dirumuskan menjadi analisis Pitfall 4:<br>**Solusi:** Menambahkan penanganan server/service cadangan dan menggunakan sistem antrean (*queue*) agar pemrosesan berjalan bertahap.<br>**Trade-off:** Waktu tunggu antrean lebih lama dan biaya operasional meningkat. |
| 22-09-2026 | Gemini | Saya ingin adanya solusi pemisahan layanan, dengan tujuan agar fokus aplikasi dapat terpecah sesuai dengan layanan masing masing dan menghindari crash, dari solusi yang saya inginkan kira kira arsitektur apa yang paling cocok? | Merekomendasikan **Microservices Architecture berbasis Event-Driven (Pub-Sub)** atau kombinasi **SOA dengan Pub-Sub** untuk memisahkan tanggung jawab (*separation of concerns*) dan mengisolasi kegagalan (*fault isolation*). | Diolah menjadi paragraf Kesimpulan Kelompok yang menghubungkan analisis *pitfall* Tugas 1 dengan perancangan arsitektur di Tugas 2. |
