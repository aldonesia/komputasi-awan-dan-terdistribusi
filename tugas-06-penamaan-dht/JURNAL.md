# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): saat mencari *successor*, fungsi hanya melakukan pengecekan iteratid apakah `key_id <= node.id`. Kesalahan terjadi ketika nilai `key_id` ternyata lebih besar dari ID node terbesar di dalam jaringan. Karena tidak ada pengecekan kondisi *wrap-around* (kembali ke awal cincin), fungsi berujung tidak menemukan node apa pun dan mengembalikan nilai `None`, yang menyebabkan *error* saat mencoba menyimpan data.
- Cara memperbaikinya: Menambahkan logika *fallback* atau *wrap-around* di bagian akhir fungsi `find_successor`. Jika perulangan selesai dan tidak ada *node* yang memenuhi syarat `key_id <= node.id`, maka fungsi secara otomatis akan menunjuk ke *node* pertama di jaringan (`self.nodes[0]`) sebagai *successor* yang benar.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: ...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
