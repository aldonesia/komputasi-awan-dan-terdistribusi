# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: kelompok kami tidak ada kendala selama mengisi TODO 1-4

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: Setelah kelima node dijalankan, node 5 terpilih sebagai leader karena memiliki ID paling tinggi. Node 5 mengirim pesan COORDINATOR kepada node lainnya. Node 1, 2, 3, dan 4 kemudian menampilkan bahwa leader saat ini adalah node 5.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: 4
- Berapa lama waktu sampai leader baru terdeteksi:
1. Waktu sampai leader baru terdeteksi, proses pemulihan ulang mulai terlihat sekitar 18:45:07. Waktu pastinya hingga seluruh node mengenali leader baru belum dapat dipastikan dari screenshot.

2. Log/Observasi: Setelah node 5 dihentikan, node 4 mendeteksi bahwa leader tidak merespon dan memulai pemilihan ulang. Node 4 kemudian mengirim pesan ELECTION dan menerima respon dari node lain. Karena node 4 merupakan node dengan ID tertinggi yang masih aktif, node 4 terpilih sebagai leader baru dan mengirim pesan COORDINATOR kepada node lain.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20 Oktober 2026 | ChatGPT | Berdasarkan tugas komputasi saya, jelaskan apa itu Bully Algorithm, bagaimana sistem dan cara kerjanya, serta berikan contoh yang mudah dipahami pemula. | AI menjelaskan bahwa node aktif dengan ID tertinggi dipilih sebagai leader. Contoh yang diberikan adalah pemilihan ketua kelompok dan pergantian leader dari Node 5 ke Node 4 ketika Node 5 mati. AI juga menjelaskan fungsi pesan ELECTION, OK, dan COORDINATOR sebagai gambaran alur pemilihan. | Penjelasan digunakan sebagai bahan pemahaman awal. Saya berencana menjadikannya panduan untuk melengkapi logika algoritma dan mengamati pergantian leader saat pengujian lima node. |
| ... | ... | ... | ... | ... |
