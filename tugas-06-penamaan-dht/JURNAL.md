# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Saat awal implementasi, terdapat kemungkinan pencarian tidak menemukan node ketika hash key lebih besar daripada ID node terbesar dalam ring, hal ini terjadi karena belum memperhitungkan mekanisme wrap-around.
- Cara memperbaikinya: Melakukan pengurutan berdasarkan ID node, lalu mencari node pertama yang memiliki ID lebih besar atau sama dengan hash key. Jika tidak ditemukan, fungsi me-return node dengan ID terkecil agar pencarian kembali ke awal ring.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: Sebelum node Medan bergabung, ring memiliki 4 node. Setelah node-medan-1 dengan ID 123 bergabung, jumlah node menjadi 5. Pada data Kurir yang digunakan, tidak ada mapping yang berpindah tanggung jawab karena tidak ada hash Kurir yang masuk ke rentang tanggung jawab node baru tersebut.
- Hasil sebelum & sesudah node keluar: Node node-jakarta-1 dengan ID 177 dikeluarkan dari ring. Setelah node keluar, ring memiliki 4 node. Tidak ada mapping Kurir yang perlu dipindahkan karena sebelumnya tidak ada Kurir yang menjadi tanggung jawab node Jakarta-1. Seluruh mapping tetap dapat ditemukan melalui proses lookup.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
