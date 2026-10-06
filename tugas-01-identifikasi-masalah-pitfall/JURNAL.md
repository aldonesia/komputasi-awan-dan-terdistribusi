# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [9/19/2026 - Sesi 1]
- Peserta: [Moch. Yusuf Hendrawan E P, Ighfir Maulana]
- Poin diskusi: Penentuan pitfall yang sesuai pada study case
- Perbedaan pendapat (jika ada): 

  - `Ighfir` berpedapat bahwa pada study case FoodGo, bahwa pitfall yang paling sesuai adalah:
    - *Network is always reliable*
    - *Latency is zero*
    - *Single Point of Failure*

  - Disisi Lain `Andy` berpendapat bahwa pitfall yang paling sesuai adalah:
     - *Network is always reliable*
     - *Latency is zero*
     - *Transport Cost is zero*

## [9/19/2026 - Sesi 2]
- Peserta: [Moch. Yusuf Hendrawan E P, Ighfir Maulana, Faiz Agit Zahiri]
- Poin diskusi: Penentuan pitfall yang sesuai pada study case
- Perbedaan pendapat (jika ada): 

  - `Andy` Memutuskan untuk mengubah pendapat nya setelah mendengarkan penjelasan dari `Ighfir` mengenai pitfall ketiga:
        - Dari *Transport Cost is zero* -> *Single Point of Failure*

  - `Faiz` bertanya kenapa pitfall *Bandwith is infinite* tidak ikut masuk. Saat ditanya buktinya, `Faiz` menjelaskan adanya lonjakan traffic pada network saat masa promo.

  - `Ighfir` berasumsi bahwa jawaban `Faiz` bisa saja masuk karena jika saja tim menganggap kalau bandwith itu infinite, maka tim hanya perlu menyewa satu server dan menghandle banyak service.

## [9/21/2026 - Sesi 3]
- Peserta: [Moch. Yusuf Hendrawan E P, Faiz Agit Zahiri]
- Poin diskusi: Memperdebatkan Masalah Timeout
- Perbedaan pendapat (jika ada): 

    - `Andy` bertanya salah satu pertanyaan pada `Faiz` mengenai asumsi yang dikeluarkan dari kode.
    - `Faiz` menjelaskan kalau tim mereka sendirilah yang menulis kalau *'Network is reliable'*.
    - `Andy` menganggap kalau jawaban tersebut kontradiksi dikarenakan sistem mengalami beberapa timeout saat terjadi lonjakan traffic.
    - Keduanya menganggap kesimpulan kalau `Sistem` tidak menyadari kalau dirinya sendiri sedang mengalami error.

## [9/22/2026 - Sesi 4]
- Peserta: [Moch. Yusuf Hendrawan E P, Ighfir Maulana, Faiz Agit Zahiri]
- Poin diskusi: Review Diskusi silang + Pemasukkan Prompt
- Perbedaan pendapat (jika ada): 


> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19/09/2026 | Gemini 3.6 Flash Mendalam | kamu adalah seorang dosen dan praktisi komputasi awan dan terdistribusi dengan pengalaman industri selama 10 tahun. kamu memiliki kemampuan untuk menjelaskan konsep teknis yang kompleks dengan bahasa yang mudah dipahami oleh mahasiswa atau praktisi junior. Tugasmu adalah menjelaskan 8 Fallacies of Distributed Computing dan masalah desain sistem terdistribusi lainnya (seperti single point of failure pada arsitektur monolitik). Penjelasan harus mencakup definisi, alasan mengapa hal tersebut dianggap sebagai kesalahan (fallacy), dan contoh kasus nyata di industri. Output harus disusun dalam format berikut: 1. Pendahuluan singkat (maksimal 100 kata). 2. Tabel perbandingan untuk 8 Fallacies of Distributed Computing dengan kolom: Nama Fallacy, Penjelasan Singkat, dan Contoh Kasus Nyata. 3. Penjelasan mendalam mengenai masalah desain sistem terdistribusi lainnya (minimal 3 masalah). 4. Kesimpulan (maksimal 50 kata). Gunakan bahasa Indonesia yang profesional namun komunikatif. Hindari jargon yang tidak dijelaskan. Pastikan setiap contoh kasus relevan dengan arsitektur sistem modern. - Penjelasan mencakup tepat 8 Fallacies of Distributed Computing. - Terdapat tabel perbandingan dengan 3 kolom yang ditentukan. - Minimal 3 masalah desain sistem terdistribusi tambahan dijelaskan. - Panjang pendahuluan maksimal 100 kata dan kesimpulan maksimal 50 kata. - Bahasa yang digunakan adalah bahasa Indonesia. | *the network is reliable* = Menganggap koneksi antarlayanan tidak pernah terputus atau mengalami kegagalan pengiriman data. *latency is zero* = Mengasumsikan pemanggilan fungsi melalui jaringan memiliki kecepatan yang sama dengan pemanggilan di memori lokal. *bandwidth is infinite* = Menganggap kapasitas pipa transfer data antarserver selalu cukup untuk menampung seluruh muatan data. *the network is secure* = Mengasumsikan lalu lintas data di dalam jaringan internal atau pusat data lokal sudah pasti terisolasi dan bebas ancaman. *topology doesn't change* = Menganggap struktur jaringan, alamat protokol internet, dan rute server bersifat statis dan tidak akan pernah berpindah. *there is one administrator* = Mengasumsikan seluruh infrastruktur terdistribusi dikelola oleh satu pihak dengan aturan kebijakan yang seragam. *transport cost is zero* = Mengabaikan konsumsi daya komputasi, pemrosesan serialisasi data, dan biaya beban transfer data dari penyedia awan. *the network is homogeneous* = Mengasumsikan seluruh perangkat, sistem operasi, dan protokol di dalam jaringan menggunakan standar perangkat keras dan lunak yang identik. *single point of failure* = Apabila mengalami kerusakan/henti fungsi, akan langsung menyebabkan keseluruhan sistem tidak dapat beroperasi secara total. *The Problem of Duplicate Entries and Data Inconsistencies* = Kegagalan di salah satu *database* akan mengakibatkan ketidaksesuaian status data. *Domino Effects and the Demand Surge Phenomenon* = Kegagalan berantai adalah kondisi di mana keterlambatan atau kegagalan pada satu komponen kecil memicu beban berlebih secara beruntun pada komponen pendukung lainnya.| Seperti yang sudah kami jelaskan sebelumnya, dalam pengirimannya, data "melewati" server, yang mana dalam satu aplikasi seperti FoodGo memiliki beberapa *service*. Padahal pada suatu aplikasi, data akan berpindah berurutan dari *service* satu ke *service* yang lain. Dengan kata lain, kalau suatu *service* sedang bermasalah/terhambat, maka datanya juga tertunda/terhambat sehingga menyebabkan latensi. Terlebih lagi jika terjadi kesalahan dalam memanajemen aplikasi salah satunya salah dalam menentukan arsitekturnya. |
|09/22/2026|Claude|dalam fallacies pada bandwidth is infinite pastinya ada bagian dari beberapa faktor yang mempengaruhi pada saat traffic. Misal 'network is reliable' dengan packet loss dan 'latency is zero' dengan latency nya. kira kira apa saja bagian dari faktor yang paling mempengaruhi di bandwidth is infinite|kalau "network is reliable" berkaitan erat dengan packet loss dan "latency is zero" dengan RTT/delay, maka "bandwidth is infinite" paling erat kaitannya dengan congestion, overhead protokol, dan bandwidth-delay product — karena ketiganya langsung menjelaskan kenapa throughput yang benar-benar bisa dipakai aplikasi selalu lebih kecil dari bandwidth yang tertulis di spesifikasi.|Karena dari bandwidth itu sendiri adalah shared resource, bukan dedicated atau bisa dimaksudkan dengan satu link yang dipakai bergantian / bersama oleh banyak proses, request, ataupun user. termasuk startup FoodGo itu sendiri akan selalu berubah - ubah pada bagian kapasitas yang tersedia tergantung siapa yang sedang memakai startup FoodGo secara bersamaan|
|9/22/2026|Claude|Konteks kasus (FoodGo — startup food delivery yang crash saat traffic tinggi karena kode punya asumsi "#network is always reliable, no need for retry" dan tidak ada timeout antar service pesanan-pembayaran). Aku BUKAN minta kamu menulis analisis final. Tolong bantu aku sebatas: 1. Brainstorm beberapa sudut pandang/angle yang bisa aku pakai untuk menjelaskan KENAPA asumsi "network is reliable" itu keliru secara teknis (mis. penyebab kegagalan jaringan apa saja yang relevan) — cukup poin-poin singkat, bukan paragraf jadi. 2. Bantu aku susun OUTLINE/struktur berpikir untuk menjawab tiap bagian di template (bukti di skenario, kenapa keliru, dampak konkret, solusi desain, trade-off) — dalam bentuk pertanyaan pemandu yang perlu aku jawab sendiri, bukan jawabannya langsung. 3. Kasih beberapa referensi/istilah teknis yang relevan untuk aku pelajari lebih lanjut (boleh sebut sumber seperti materi jaringan dasar, packet loss, retry/backoff, circuit breaker dll), tapi biar aku yang cari dan tulis penjelasannya sendiri. Tolong JANGAN menulis kalimat analisis siap-tempel, jangan mengaitkan langsung ke kalimat skenario dengan gaya final, dan jangan menuliskan solusi+trade-off dalam bentuk paragraf utuh — cukup dalam bentuk poin pemandu/pertanyaan supaya aku yang menyusun tulisan akhirnya sendiri (sesuai kebijakan Level 2: AI Assisted Idea Generation & Structuring di mata kuliah ini). Sumber materi yang bisa kamu rujuk untuk ideation: ppt: slides.01 - TELU.pptx; https://markmanson.net/logical-fallacies; https://www.ir.com/guides/what-is-network-packet-loss; https://mycarrier.telkom.co.id/id/article/studi-kasus-sukses-mengelola-jaringan-dengan-netmo | AI memberi poin-poin penyebab kegagalan jaringan (packet loss, congestion, hardware/software failure), daftar pertanyaan pemandu per bagian template (bukti skenario, kenapa keliru, dampak, solusi, trade-off), dan daftar istilah/referensi teknis untuk dipelajari lebih lanjut (retry/backoff, circuit breaker, idempotency key, dll).|Mengimplementasikan fitur retry / 'coba lagi' dengan *exponential backoff* dan *jitter* saat request ke modul pembayaran gagal, lalu jumlah percobaanya akan dibatasi dengan *idempotency key* agar proses tidak bertambah banyak.Cara kerja: Setiap kali Request gagal, sistem akan mencoba untuk mengirimkan ulang secara otomatis dengan jeda waktu yang bertambah di tiap percobaan. Selain itu, jeda waktu juga diberikan variasi agar request dari banyak user yang mencoba di waktu bersamaan tidak dapat ikut mencoba ulang di waktu yang sama sehingga tidak membanjiri server. Contoh pada Apps: Kita bisa melihat pada aplikasi discord desktop dimana saat reconnect akan muncul pesan '1s.... 2s... 5s...' dan seterusnya.|