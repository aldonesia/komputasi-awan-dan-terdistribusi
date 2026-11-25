# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [20/09/2026] [Diskusi secara langsung (Offline)]
- Peserta: [Bagas Bintang Saputro] | [103072400078]
           [Wahyu Puji Riski Purwanto] | [103072400050]
           [Andi Muh. Arief alfaizi ilham] | [103072400082]
- Poin diskusi: 1. Pada saat diskusi kami menemukan dan sepakati bahwa memakai 2 pitfall yang cocok yaitu "The Network Is Realible" dan "Latency Is Zero"
2. "The Network Is Realible" (Dippiliha dan disarankan oleh Bintang) karena pada sekenario secara eksplisit terdapat asumsi network is always realible, no need for retry.
3. "Latency Is Zero" (dipilih dan disarankan oleh wahyu) dipertimbangkan karena modul pesanan memanggil modul pembayaran tanpa mekanisme timeout sehingga sistem dapat menggantung menunggu tanpa batas waktu.
4. Selanjutnya kami menemukan poin di masalah desain sistem terdistribusi, yaitu Single Poin of Failure karena salah satu gejalanya mengatakan "berjalan di satu monolitik yang sama" (dipilih dan disarankan oleh arief)
- Perbedaan pendapat (jika ada): ...

## [Tanggal diskusi 2]
- ...

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20/09/2026 | ChatGPT | Saya sedang menganalisis studi kasus FoodGo dalam mata kuliah Komputasi Awan dan Terdistribusi. Saya memilih salah satu Fallacies of Distributed Computing, yaitu "Latency Is Zero". Dalam skenario FoodGo disebutkan bahwa aplikasi menjadi sangat lambat dan beberapa permintaan mengalami timeout. Selain itu, tidak ada timeout pada pemanggilan antar-service; modul pesanan memanggil modul pembayaran dan dapat menunggu tanpa batas waktu. Ketika trafik meningkat, server menjadi kewalahan dan terkadang mengalami crash. Bantu saya menganalisis masalah "Latency Is Zero" berdasarkan skenario tersebut. Jangan berikan jawaban langsung, coba jelaskan kenapa dan berikan sebuah analogi atau contoh yang mudah saya pahami sebagai mahasiswa atau pemula yang baru belajar tentang komputasi awan dan sistem terdistribusi. Jelaskan materi ini dan berikan juga contoh kasusnya. | AI menjelaskan bahwa Latency Is Zero adalah asumsi bahwa komunikasi antar-service selalu berlangsung cepat atau tanpa jeda. Pada FoodGo, modul pesanan menunggu respons dari modul pembayaran tanpa adanya timeout. Ketika trafik meningkat atau modul pembayaran lambat merespons, permintaan dapat menumpuk dan menambah beban server. AI juga memberikan analogi antrean kasir untuk mempermudah pemahaman. | Saya menggunakan AI untuk membantu memahami konsep Latency Is Zero. Dari penjelasan tersebut, saya memahami bahwa tidak adanya timeout dapat membuat proses terus menunggu dan membebani server. Solusi yang saya usulkan adalah menerapkan timeout agar proses tidak menunggu tanpa batas saat modul pembayaran terlambat merespons. |
|21/09/2026| Gemini | Fallacies of Distributed Computing (referensi: "the network is reliable", "latency is zero", "bandwidth is infinite", "the network is secure", "topology doesn't change", "there is one administrator", "transport cost is zero", "the network is homogeneous") DAN/ATAU masalah desain sistem terdistribusi lain yang relevan (mis. single point of failure karena arsitektur monolitik).jelaskan materi ini dan berikan juga contoh kasus nya | Berikut adalah paragraf naratif Anda yang sudah disisipkan istilah bahasa Inggrisnya (dicetak tebal) sesuai permintaan:AI menjelaskan bahwa membangun sistem terdistribusi dengan asumsi infrastruktur selalu sempurna adalah sebuah kesalahan fatal. Kesalahan ini berakar dari 8 Fallacies of Distributed Computing, di mana pengembang sering keliru menganggap jaringan selalu dapat diandalkan (The network is reliable) dan aman (The network is secure), latensi adalah nol (Latency is zero), serta bandwidth tidak terbatas (Bandwidth is infinite), padahal sistem mutlak membutuhkan mekanisme retry, enkripsi data, dan efisiensi pengiriman. Selain itu, asumsi bahwa topologi tidak berubah (Topology doesn't change), hanya ada satu administrator (There is one administrator), biaya transportasi data gratis (Transport cost is zero), dan jaringan bersifat homogen (The network is homogeneous) juga harus dihindari karena server cloud sangat dinamis, kebijakan pihak ketiga bisa berubah sepihak, dan perbedaan sistem membutuhkan format data universal seperti JSON.Lebih lanjut, AI juga menyoroti perlunya mengantisipasi dua kerentanan arsitektur utama: Single Point of Failure (SPOF) yang dapat melumpuhkan seluruh sistem secara total akibat satu komponen sentral yang mati, serta Cascading Failures yang memicu efek domino crash antar-layanan akibat tumpukan antrean. Kesimpulannya, AI menekankan keharusan menerapkan prinsip designing for failure—membangun arsitektur sejak awal dengan kesadaran penuh bahwa gangguan jaringan dan komponen pasti akan terjadi.masing masing juga ai memberikan studi kasus untuk memudahkan memahamai | setelah memahami penjelasan dan contoh kasus yang di berikan ai saya memahami bahwa salah satu masalah desain sistem terdistribusi "yaitu Single Point Of Failure" di karena kana salah satu gejala mirip dengan penjelasan dari ai yaitu 1 server yang sama(monolitik) jadi memudahkan saya untuk menganalisis|






| ... | ... | ... | ... | ... |
