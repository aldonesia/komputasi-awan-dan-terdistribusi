# Jurnal Proses — Tugas 6

## Implementasi find_successor

- **Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring):** Pada percobaan awal, pencarian *successor* hanya menggunakan filter daftar node dengan kondisi `node_id >= key_hash` tanpa menangani kondisi ketika nilai `key_hash` milik kurir lebih besar daripada `node_id` terbesar yang ada di dalam ring (misalnya `key_hash` bernilai 240 sedangkan node terbesar di ring memiliki hash 210). Akibatnya, fungsi mengembalikan nilai `None` atau memicu `IndexError` karena gagal melakukan *wrap-around* ke titik 0 pada ruang identifier melingkar ($0 \dots 255$). Selain itu, urutan *key* pada `self.nodes.keys()` sesuai urutan masuk (*insertion order*), sehingga jika tidak diurutkan terlebih dahulu dengan `sorted()`, fungsi bisa mengambil node pertama yang masuk yang kebetulan nilainya `>= key_hash`, bukan node dengan nilai hash **terkecil** yang `>= key_hash`.
- **Cara memperbaikinya:** Mengurutkan seluruh daftar identifier node yang aktif terlebih dahulu menggunakan `sorted_node_ids = sorted(self.nodes.keys())`, lalu melakukan iterasi berurutan untuk mencari `node_id` pertama yang memenuhi `node_id >= key_hash`. Jika hingga akhir daftar tidak ditemukan node yang memenuhi syarat tersebut, fungsi melakukan *wrap-around* melingkar dengan mengembalikan elemen pertama dari daftar terurut (`sorted_node_ids[0]`), yaitu node dengan nilai hash paling kecil di dalam ring.

## Skenario join/leave

- **Hasil sebelum & sesudah node baru bergabung:**
  - **Sebelum node baru bergabung:** Seluruh `key_hash` milik kurir yang berada pada rentang antara *predecessor* dan *successor* lama ditangani sepenuhnya oleh *successor* lama tersebut. Saat `lookup()` dijalankan, resolusi IP kurir mengarah ke node *successor* lama.
  - **Sesudah node baru bergabung (`join`):** Node baru masuk ke ruang identifier ring pada posisi `node_id = hash_id(node_name)`. Dengan mengecualikan `node_id` baru sementara waktu untuk mendeteksi `old_successor`, sistem memindai `self.data` dan memigrasikan tanggung jawab setiap *key* yang kini memiliki `find_successor(key_hash) == node_id` dari `old_successor` ke node baru. Saat `lookup()` dipanggil kembali setelah `join`, *key* yang berada di belakang atau tepat pada posisi hash node baru kini dilayani oleh node baru tersebut tanpa mengubah atau menghilangkan data IP kurir.
- **Hasil sebelum & sesudah node keluar:**
  - **Sebelum node keluar:** Node yang aktif memegang sejumlah *key* kurir yang nilai hash-nya memiliki `find_successor(key_hash) == node_id`.
  - **Sesudah node keluar (`leave`):** Sebelum `node_id` dihapus dari `self.nodes`, sistem mendata seluruh `key_hash` yang sedang menjadi tanggung jawab node tersebut. Begitu `node_id` dihapus dari `self.nodes`, pemanggilan `find_successor(key_hash)` untuk setiap *key* tadi secara otomatis mengalihkan tanggung jawab ke *successor* berikutnya searah jarum jam di dalam ring (termasuk *wrap-around* ke node terkecil apabila node yang keluar adalah node dengan hash terbesar). Saat `lookup()` diuji kembali, seluruh ID kurir tetap berhasil ditemukan dan mengembalikan alamat IP yang valid melalui node *successor* yang baru.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di `../RUBRIK-UMUM.md`. Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 3 November 2026 | Gemini | "Jelaskan cara kerja logika wrap-around dan migrasi key saat node join/leave pada simulasi Chord DHT ruang 8-bit" | AI menjelaskan konsep ruang identifier melingkar $0 \dots 2^m-1$, di mana pencarian successor mengurutkan ID node dan kembali ke indeks ke-0 jika key melebihi ID node maksimum, serta cara mengecek perubahan kepemilikan key saat topologi ring berubah. | Mengimplementasikan sendiri logika `sorted(self.nodes.keys())` dan *fallback* `sorted_node_ids[0]` pada fungsi `find_successor()`, menyusun mekanisme pengecualian sementara `node_id` pada `join()` serta pencatatan `keys_held` pada `leave()`, lalu menuliskan hasil pengamatan ke dalam jurnal. |
