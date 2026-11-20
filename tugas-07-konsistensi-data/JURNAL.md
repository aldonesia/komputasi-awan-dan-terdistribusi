# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: 
  - Eventual Consistency kurang tepat jika digunakan sendiri karena server Jakarta dan Bandung dapat memiliki data saldo yang berbeda sementara akibat keterlambatan replikasi.
  - Perbedaan saldo dapat menyebabkan transaksi pelanggan ditolak meskipun saldo sebenarnya mencukupi.
  - Saldo e-wallet berkaitan langsung dengan uang pelanggan sehingga membutuhkan konsistensi data yang lebih kuat dibandingkan data seperti jumlah like di media sosial.
  - Read-Your-Writes dapat diterapkan agar pelanggan selalu membaca saldo terbaru setelah melakukan top-up, meskipun berpindah server.
  - Transaksi pembayaran juga membutuhkan validasi saldo terbaru dan kontrol konkurensi untuk mencegah kesalahan transaksi.

- Kesimpulan akhir & alasan: FoodGo membutuhkan Strong Consistency untuk transaksi saldo, dengan menerapkan pendekatan Client-Centric Consistency, khususnya Read-Your-Writes. Pendekatan ini dipilih agar pelanggan dapat melihat saldo terbaru setelah melakukan top-up, meskipun replikasi antarserver belum selesai. Dengan demikian, risiko penolakan transaksi akibat membaca saldo lama dapat dikurangi dan kepercayaan pelanggan tetap terjaga.

## Simulasi

Simulasi (`src/replica_simulation.py`) memodelkan dua replika (Jakarta dan Bandung) dengan delay replikasi 2 detik. Top-up selalu ditulis ke Jakarta, lalu direplikasi ke Bandung setelah delay. Setiap penulisan memiliki nomor versi per pelanggan.

**Hasil skenario naif vs Read-Your-Writes:**

| Skenario | Operasi | Hasil | Keterangan |
|---|---|---|---|
| Naif | Top-up Rp50.000 di Jakarta, 0,5 detik kemudian baca saldo dari Bandung | 0 | Replikasi belum sampai, saldo lama terbaca (bug) |
| Naif | Top-up Rp20.000 (saldo seharusnya 70.000), baca dari Bandung | 50.000 | Bandung masih menyimpan versi 1 (stale) |
| Read-Your-Writes | Baca dari Bandung dengan `versi_minimal` = versi top-up terakhir | 70.000 | Versi Bandung (1) < versi client (2), sehingga dialihkan ke Jakarta dan saldo yang dibaca benar |
| Read-Your-Writes | Baca dari Bandung setelah replikasi selesai | 70.000 | Versi Bandung sudah 2, jadi dibaca langsung dari Bandung |

**Kesimpulan:** tanpa jaminan konsistensi, pelanggan bisa membaca saldo lama dari Bandung sehingga transaksi berisiko ditolak padahal saldo cukup. Dengan Read-Your-Writes, client membawa versi data terakhir yang ia tulis. Replika yang versinya lebih lama tidak melayani pembacaan itu, tetapi meneruskannya ke Jakarta, sehingga pelanggan selalu melihat saldo terbarunya. Bukti output ada di folder `bukti/`.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|17 Nov 2026| Gemini | Apa kelebihan dan kekurangan dari model konsistensi Eventual Consistency? | Eventual Consistency memiliki kelebihan dalam hal performa dan skalabilitas, tetapi memiliki kekurangan dalam hal konsistensi data yang tidak segera tercapai. | Menggunakan informasi ini untuk memahami kenapa Eventual Consistency tidak cocok untuk aplikasi FoodGo. |
| ... | ... | ... | ... | ... |
