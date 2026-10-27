# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Terjadi deadlock (re-entrant lock) ketika start_election() memanggil declare_leader() secara langsung di dalam blok with self.lock:. Hal ini menyebabkan Node 5 terkuci dan tidak bisa dihentikan menggunakan Ctrl+C. Solusinya adalah memisahkan evaluasi kondisi ke dalam variabel lokal is_leader di dalam lock, lalu memanggil declare_leader() di luar blok lock, dengan begitu node 5 tidak terkunci dan akhir nya program berjalan.

Bukti ketika node saling terkunci:

![bukti1](bukti/BUKTI_1.png)

Dalam kondisi itu, node tidak saling memilih siapa leader dan hanya memulai election tanpa henti. 

## Skenario 1: Start normal
- Leader yang terpilih: ...
- Log/observasi: ...

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: ...
- Berapa lama waktu sampai leader baru terdeteksi: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19-Oktober-2026| claude | Jelaskan secara mendalam bagaimana bully algoritma bekerja, dari penjelasannya, berikan analogi dari cara kerja bully algoritma, termasuk psuedo code dari bully algoritma dan apa contoh penerapannya di dunia nyata | memberikan penjelasan lengkap dari bully algoritma | menggunakan penjelasan itu untuk menjawab todo di node py |
