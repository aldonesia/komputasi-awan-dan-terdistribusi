# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:  

Keunggulan Eventual Consistency pada latensi rendah dan ketersediaan antar-wilayah vs risikonya jika dipakai murni pada data sensitif seperti saldo e-wallet (false rejection, double spending, turunnya kepercayaan/reputasi bisnis), Keunggulan Sequential Consistency dalam menjamin keseragaman urutan operasi antar-replika vs konsekuensinya berupa penambahan waktu sinkronisasi/latensi. 
- Kesimpulan akhir & alasan:

Berdasarkan pertimbangan tersebut, kami menyimpulkan bahwa Eventual Consistency saja tidak memadai untuk transaksi finansial sehingga sistem membutuhkan konsistensi urutan yang ketat atau kombinasi replikasi asinkron dengan jaminan Client-Centric Consistency (Read-Your-Writes). Pendekatan ini dipilih karena mekanisme verifikasi versi data pengguna (versi_minimal) disertai pengalihan (redirect) ke server Jakarta ketika replika Bandung tertinggal mampu menjaga integritas saldo pelanggan tanpa harus mengorbankan performa pembacaan secara global.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: 

Hasil pengujian membuktikan kelemahan pendekatan naif dibanding metode Read-Your-Writes. Saat top-up sebesar 50.000,0 dilakukan di server Jakarta (versi 1) dengan simulasi jeda replikasi 2,0 detik, server Bandung yang dibaca secara naif masih mengembalikan nilai 0,0 dan baru terbarui setelah replikasi tuntas. Keunggulan solusi terlihat pada eksperimen kedua saat top-up bertambah 20.000,0 (versi 2, total 70.000,0). Pembacaan naif di server Bandung sebelum sinkronisasi hanya mendeteksi saldo lama 50.000,0. Namun, fungsi baca_saldo_read_your_writes secara responsif mengetahui bahwa data di server Bandung belum mutakhir, lalu mengalihkan akses baca ke server Jakarta. Hasilnya, pengguna mendapatkan saldo akurat 70.000,0 secara seketika tanpa harus menunggu proses replikasi di server Bandung selesai.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 28/11/2026 | Google AI | Brainstorming alur *sequence diagram*  | Memberi kerangka urutan partisipan |  Menggambar dan menganalisis sketsa kedua diagram sendiri di draw.io, lalu menerjemahkan dan memperbaikinya ke sintak Mermaid `sequenceDiagram` di `README.md`. |
