# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): saat mencari *successor*, fungsi hanya melakukan pengecekan iteratid apakah `key_id <= node.id`. Kesalahan terjadi ketika nilai `key_id` ternyata lebih besar dari ID node terbesar di dalam jaringan. Karena tidak ada pengecekan kondisi *wrap-around* (kembali ke awal cincin), fungsi berujung tidak menemukan node apa pun dan mengembalikan nilai `None`, yang menyebabkan *error* saat mencoba menyimpan data.
- Cara memperbaikinya: Menambahkan logika *fallback* atau *wrap-around* di bagian akhir fungsi `find_successor`. Jika perulangan selesai dan tidak ada *node* yang memenuhi syarat `key_id <= node.id`, maka fungsi secara otomatis akan menunjuk ke *node* pertama di jaringan (`self.nodes[0]`) sebagai *successor* yang benar.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: 
  Sebelum: terdapat empat node dalam ring dengan ID 40, 102, 136, dan 177.
  Sesudah: node node-medan-1 dengan ID 123 berhasil bergabung sehingga terdapat lima node.
  Hasil lookup: alamat IP kurir tetap dapat ditemukan, yaitu 192.168.1.10 untuk kurir-001.

- Hasil sebelum & sesudah node keluar:
  Sebelum: terdapat lima node dalam ring.
  Sesudah: node node-jakarta-1 dengan ID 177 keluar sehingga tersisa empat node.
  Hasil lookup: kurir-001 dan kurir-002 masih dapat ditemukan menggunakan alamat IP yang sama.
  Catatan: mekanisme pengalihan data masih perlu diperbaiki karena program belum memvalidasi kepemilikan data sebelum node keluar.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
