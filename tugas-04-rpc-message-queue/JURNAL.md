# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- saya mengerjakan jalur A (RPC) untuk mensimulasikan komunikasi sinkron antara modul pesanan dan modul pembayaran. Operasi seperti pengecekan saldo dan pemotongan saldo memerlukan respons instan (blocking / request-response) agar transaksi dapat dipastikan valid seketika sebelum pesanan dilanjutkan. (Vaylan)
- Diqri: Mengerjakan Jalur B, menguji grafik antrian untuk memastikan pesanan consumer tetap diproses dalam keadaan offline dan publisher menyala karena antrean tersimpan pada database.

## Kendala teknis
- Pada saat running jalur A (RPC) tidak ada kendala sama sekali

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: *Bagian ini dikerjakan dan didokumentasikan oleh anggota kelompok yang mengambil Jalur B.*

- Analisis: 
Pola Message Queue (MQ) lebih efektif dibanding RPC, karena mampu memisahkan suatu hubungan agar bisa berjalan secara mandiri/asinkron dan memberikan ketahanan (fault tolerance) yang tinggi, sehingga pesanan tetap aman di dalam antrean meskipun modul kurir sedang down dan lonjakan transaksi dapat diatasi melalui manajemen beban (load leveling). Sebaliknya, jika skenario tersebut dipaksakan menggunakan RPC yang bersifat synchronous, sistem akan mengalami tight coupling fatal di mana modul pembayaran ikut lambat atau mengalami timeout saat server kurir bermasalah, yang berujung pada buruknya pengalaman pengguna serta risiko kegagalan transaksi secara keseluruhan. Contoh case: penggunaan RPC (Remote Procedure Call) untuk memproses permintaan real-time inventory check atau pemotongan stok bahan baku secara langsung saat pembayaran pesanan dilakukan. Jika modul gudang atau database inventaris sedang mengalami lonjakan beban atau down, RPC akan memaksa proses pembayaran pelanggan tertahan (blocking), karena menunggu respons sinkron dari server gudang, yang berakibat pada kegagalan transaksi secara keseluruhan (cascade failure), padahal pelanggan hanya ingin menyelesaikan pembayaran pesanan mereka.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 12 Oktober 2026 | Gemini | jelaskan aku mengenai RPC pada modul berikut dan berikan aku alur pengerjaan untuk jalur A dan apakah bisa mengerjakan RPC tanpa library eksternal untuk modul pembayaran dan pesanan?| AI memberikan kerangka kode implementasi SimpleXMLRPCServer untuk mendaftarkan fungsi cek_saldo serta proses_pembayaran di server, dan penggunaan xmlrpc.client.ServerProxy di sisi client. | Saya memodifikasi logika validasi saldo di server.py agar mengembalikan dictionary status transaksi, lalu mengintegrasikannya ke client.py untuk menguji waktu respons sinkron. |
|13 Oktober 2026 | Gemini | C:\msys64\ucrt64\bin\python.exe C:\Users\ahmad diqri w\AppData\Local\Microsoft\WindowsApps\python.exe C:\Users\ahmad diqri w\AppData\Local\Python\bin\python.exe |Hasil where.exe python Anda sangat memperjelas situasinya! Ada tiga jalur Python di komputer Anda, dan penyebab utama venv tidak ngefek adalah karena PowerShell Anda selama ini menggunakan stub bawaan Windows Store (...\WindowsApps\python.exe), yang tidak memiliki kemampuan untuk membuat virtual environment secara normal. Kita akan menggunakan Python asli yang sebenarnya dari direktori lokal Anda (C:\Users\ahmad diqri w\AppData\Local\Python\bin\python.exe) yang sudah terdeteksi di baris ketiga.| Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process .\venv\Scripts\Activate.ps1 kemudian python -m pip install --upgrade pip python -m pip install pika |