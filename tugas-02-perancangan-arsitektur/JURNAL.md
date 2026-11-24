# Jurnal Proses — Tugas 2

## [24-09-2026]
- Opsi arsitektur yang dipertimbangkan: SOA dan Pub-Sub
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Butuh keduanya digabungkan karena memisahkan modul lebih baik menggunakan arsitektur SOA sedangkan antrean pesanan lebih baik menggunakan arsitektur Pub-Sub (sesuai dengan kesimpulan kami di tugas 1). Jadi, kami memutuskan untuk menggabungkan kedua arsitektur tersebut
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Belum mulai membuat diagram karena masih mendiskusikan solusi arsitektur

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| :--- | :--- | :--- | :--- | :--- |
| 28-09-2026 | GPT | kaya gimana sih model diagram untuk SOA, PubSub dan gimana sih cara menentukan jenis komunikasinya seperti (sinkron/asinkron, request-response/event) | AI memberikan gambaran berupa tulisan terkait gimana cara menentukan jenis komunikasinya dan diberikan penjelasan setiap jenis komunikasinya | setelah saya mendapatkan gambaran dari AI saya langsung membuat diagramnya di draw.io dan membayangkan alurnya seperti kita sedang memesan makanan di online |
| 24-09-2026 | Gemini | jika setelah menganalisis permasalahan per pitfall yang ditemukan di tugas 1, bisakah seluruh masalah langsung dijuruskan menjadi 1 masalah besar yang solusinya menjadi beberapa layanan seperti modul pesanan dll  | Bisa. Bahkan, merangkum masalah pitfall di Tugas 1 menjadi satu masalah utama (root cause) adalah cara terbaik dan paling elegan untuk menyusun narasi perancangan arsitektur di Tugas 2. | Saya hanya bertanya untuk pemahaman saya, sehingga saya bisa membuat kesimpulan analisis |
