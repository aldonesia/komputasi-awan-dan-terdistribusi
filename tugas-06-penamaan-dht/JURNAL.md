# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring):elum menangani kondisi wrap-around ketika tidak ada ID node yang lebih besar atau sama dengan hash data yang dicari.
- Cara memperbaikinya: Mengurutkan ID node menggunakan sorted(), mencari node pertama yang ID-nya lebih besar atau sama dengan hash data, lalu mengembalikan node dengan ID terkecil jika tidak ditemukan (wrap-around ke awal ring).

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung:Sebelum node Medan (ID 123) bergabung, data kurir-test-13 tersimpan di node 136. Setelah node Medan bergabung, data berpindah ke node 123 karena node tersebut menjadi successor baru untuk hash kurir 111.
- Hasil sebelum & sesudah node keluar: Sebelum node Surabaya (ID 136) keluar, data kurir-003 tersimpan di node 136. Setelah node Surabaya keluar, data berpindah ke node 177 sebagai successor baru. Data kurir tetap dapat ditemukan melalui proses lookup.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26-10-2026 | ChatGPT | Berikan ide untuk memahami cara kerja find_successor() pada Chord DHT, terutama dalam menentukan node tujuan dan menangani wrap-around. | Mendapatkan gambaran tentang pencarian successor berdasarkan urutan ID node. | Saya mempelajari konsepnya dan menyesuaikan pemahaman dengan kode program yang digunakan. |
| 25-10-2026 | ChatGPT | Apa saja yang perlu diperhatikan saat menguji node join dan leave pada simulasi Chord DHT? | Mendapatkan ide untuk membandingkan penanggung jawab data sebelum dan sesudah perubahan node. | Saya menjalankan simulasi dan mencatat perubahan berdasarkan output terminal. |
| 25-10-2026 | ChatGPT | Bantu saya memahami penyebab fungsi join() tidak terdeteksi pada class ChordRing dan hal apa yang perlu diperiksa. | Mendapatkan arahan untuk memeriksa struktur class, indentasi, dan pesan error Python. | Saya memeriksa kode di VS Code, memperbaiki bagian yang bermasalah, lalu menjalankan ulang program untuk menguji hasilnya. | 