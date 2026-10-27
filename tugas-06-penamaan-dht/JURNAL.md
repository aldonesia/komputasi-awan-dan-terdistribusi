# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui: Lupa menangani kondisi *wrap-around* ketika `key_hash` lebih besar dari seluruh ID node di ring, serta belum ada validasi kondisi saat ring masih kosong.
- Cara memperbaikinya: Mengurutkan seluruh ID node aktif dengan `sorted(self.nodes.keys())`, lalu mengambil node pertama yang bernilai `>= key_hash`. Jika tidak ada node yang memenuhi, fungsi mengembalikan node pertama (`sorted_node_ids[0]`) sebagai bentuk *wrap-around* melingkar.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung:...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|25-10-2026| Gemini | Jelaskan konsep Distributed Hash Table (DHT) dan algoritma Chord dalam studi kasus penamaan IP dinamis kurir FoodGo, kenapa DNS/flat naming tidak cocok, serta cara kerja fungsi lookup, join, dan leave | Menjelaskan analogi ring topology (m=8 bit), aturan successor (N >= k), serta alasan DNS konvensional gagal menangani IP dinamis akibat keterbatasan cache TTL. | Menggunakan konsep ring topology dan aturan successor tersebut sebagai kerangka analisis untuk README.md dan dasar logika alur fungsi find_successor() pada kode chord_simulation.py. |
