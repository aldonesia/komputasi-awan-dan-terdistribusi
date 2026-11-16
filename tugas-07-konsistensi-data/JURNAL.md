# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
Argumen yang dipertimbangkan:
- Eventual Consistency: Mudah diimplementasikan dan performa tinggi secara global, tetapi memiliki jeda waktu sinkronisasi (replication delay). Kurang cocok untuk transaksi finansial sensitif seperti saldo e-wallet karena dapat menyebabkan stale read (transaksi gagal/saldo belum ter-update).

- Sequential Consistency: Menjamin semua replika melihat urutan operasi yang sama persis, tetapi membutuhkan koordinasi global yang memperlambat latensi dan menurunkan ketersediaan (availability).

- Client-Centric Consistency (Read-Your-Writes): Menjadi jalan tengah terbaik karena menjamin klien yang melakukan write (misalnya top-up di server Jakarta) akan selalu melihat data terbarunya sendiri meskipun membaca dari replika lain (server Bandung), menjaga pengalaman pengguna dan integritas transaksi tanpa mengorbankan performa sistem secara keseluruhan

- Kesimpulan akhir & alasan: Memilih Client-Centric Consistency (Read-Your-Writes) karena pada aplikasi e-wallet FoodGo, aspek kepuasan pengguna dan akurasi saldo pribadi jauh lebih krusial dibandingkan sinkronisasi global secara instan di seluruh node

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: Pada skenario naif, transaksi di server Bandung ditolak karena terjadi inconsistent read—replika Bandung masih membaca saldo lama akibat delay replikasi dari Jakarta meskipun saldo sebenarnya sudah mencukupi. Sebaliknya, pada skenario Read-Your-Writes, klien menyertakan version atau timestamp pembaruan terakhirnya saat mengakses server Bandung. Jika data lokal Bandung masih tertinggal, server akan menunggu proses replikasi selesai sebelum membaca saldo, sehingga pelanggan selalu melihat saldo terbarunya dan transaksi berhasil.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
