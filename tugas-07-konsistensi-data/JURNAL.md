# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: 
  - Eventual Consistency kurang tepat jika digunakan sendiri karena server Jakarta dan Bandung dapat memiliki data saldo yang berbeda sementara akibat keterlambatan replikasi.
  - Perbedaan saldo dapat menyebabkan transaksi pelanggan ditolak meskipun saldo sebenarnya mencukupi.
  - Saldo e-wallet berkaitan langsung dengan uang pelanggan sehingga membutuhkan konsistensi data yang lebih kuat dibandingkan data seperti jumlah like di media sosial.
  - Read-Your-Writes dapat diterapkan agar pelanggan selalu membaca saldo terbaru setelah melakukan top-up, meskipun berpindah server.
  - Transaksi pembayaran juga membutuhkan validasi saldo terbaru dan kontrol konkurensi untuk mencegah kesalahan transaksi.

- Kesimpulan akhir & alasan: FoodGo membutuhkan Strong Consistency untuk transaksi saldo, dengan menerapkan pendekatan Client-Centric Consistency, khususnya Read-Your-Writes. Pendekatan ini dipilih agar pelanggan dapat melihat saldo terbaru setelah melakukan top-up, meskipun replikasi antarserver belum selesai. Dengan demikian, risiko penolakan transaksi akibat membaca saldo lama dapat dikurangi dan kepercayaan pelanggan tetap terjaga.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|17 Nov 2026| Gemini | Apa kelebihan dan kekurangan dari model konsistensi Eventual Consistency? | Eventual Consistency memiliki kelebihan dalam hal performa dan skalabilitas, tetapi memiliki kekurangan dalam hal konsistensi data yang tidak segera tercapai. | Menggunakan informasi ini untuk memahami kenapa Eventual Consistency tidak cocok untuk aplikasi FoodGo. |
| ... | ... | ... | ... | ... |
