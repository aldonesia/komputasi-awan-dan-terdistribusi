# Jurnal Proses — Tugas 6

## Implementasi `find_successor`

- Kesalahan pertama yang ditemui: ring harus melingkar; pencarian key yang lebih besar dari semua ID node perlu kembali ke node ber-ID terkecil.
- Cara memperbaikinya: urutkan ID node, pilih ID pertama yang `>= key_hash`, dan gunakan ID minimum bila tidak ada kandidat. Ring kosong menghasilkan `LookupError`.

## Skenario join/leave

- Sebelum join: kurir-002 (hash 28) menjadi tanggung jawab node-bandung-1 (ID 40).
- Sesudah `node-medan-67` (ID 35) bergabung: kurir-002 berpindah tanggung jawab ke node ID 35.
- Sebelum leave: kurir-001 (hash 50) ditangani node-jakarta-2 (ID 102).
- Sesudah node tersebut keluar: successor baru node-surabaya-1 (ID 136) mengambil alih; lookup masih memperoleh IP `192.168.1.10`.

| Tanggal | Tool AI | Pertanyaan untuk AI | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-11-02 | ChatGPT | Bagaimana aturan successor Chord menentukan node penyimpan dari hash key, termasuk saat terjadi wrap-around? | Urutkan ID node; ambil ID terkecil yang tidak kurang dari hash key. Jika key melewati ID terbesar, kembali ke ID terkecil. | - |
| 2026-11-02 | ChatGPT | Key mana yang berpindah tanggung jawab ketika node baru masuk atau node lama keluar dari ring? | Bandingkan successor sebelum dan sesudah perubahan topologi untuk setiap key yang terdaftar. | `join()` dan `leave()` mencetak record yang berubah pemilik; skenario konkret ditulis berdasarkan output simulasi. |
