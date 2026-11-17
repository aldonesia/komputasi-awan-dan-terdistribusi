# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- **Argumen yang dipertimbangkan:**
  1. *Eventual Consistency* murni menawarkan latensi rendah dan ketersediaan tinggi, tetapi menyisakan celah waktu di mana saldo antar server replika (Jakarta dan Bandung) tidak sinkron. Pada sistem finansial seperti *e-wallet* FoodGo, jeda sinkronisasi ini memicu *inconsistent read* yang membuat transaksi pelanggan ditolak meski saldo sebenarnya cukup. Dampak bisnisnya jauh lebih kritis dibandingkan fitur non-transaksional seperti penghitung *like* media sosial.
  2. *Sequential Consistency* secara global menjamin seluruh replika melihat urutan operasi transaksi yang sama persis, tetapi membutuhkan sinkronisasi dan penguncian lintas wilayah pada setiap operasi tulis sehingga menurunkan kecepatan respons aplikasi.
- **Kesimpulan akhir & alasan:** Menggunakan kombinasi *Eventual Consistency* pada lapisan replikasi antar server yang dilengkapi dengan jaminan **Client-Centric Consistency (Read-Your-Writes)**. Pendekatan ini menjaga performa sistem tetap cepat tanpa penguncian global, sekaligus menjamin pelanggan yang baru melakukan *top-up* akan selalu membaca saldo terbarunya sendiri meskipun dialihkan ke server replika lain.

## Simulasi (jika dikerjakan)
- **Hasil skenario naif vs Read-Your-Writes:**
  - **Skenario Naif:** Setelah pelanggan melakukan *top-up* sebesar `50000` di server Jakarta dan langsung melakukan pembacaan ke server Bandung dalam jeda `0.5` detik (lebih cepat dari `REPLICATION_DELAY` sebesar `2.0` detik), server Bandung mengembalikan saldo lama sebesar `0.0` (*stale read*).
  - **Skenario Read-Your-Writes:** Setelah *top-up* kedua sebesar `20000` (total saldo menjadi `70000.0`, versi `2`), klien menyertakan parameter `versi_minimal` saat membaca saldo dari server Bandung. Server Bandung mendeteksi bahwa metadata `last_write_version` lokalnya (`1`) tertinggal dari versi klien (`2`), sehingga sistem melakukan *polling* dan menahan pembacaan hingga replikasi asinkron selesai. Hasilnya, saldo yang dikembalikan konsisten sebesar `70000.0`.

Bukti Menjalankan Simulasi:

![Simulasi](bukti/simulasi1.png)

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 16/11/2026 | Gemini | "Jelaskan konsep model konsistensi data (Sequential, Eventual, dan Client-Centric Consistency) serta penerapannya pada studi kasus nyata dan kebutuhan simulasi replikasi server e-wallet." | Menjelaskan perbedaan antara *data-centric consistency* (*Sequential* vs *Eventual*) dan *client-centric consistency* (*Read-Your-Writes*), dampak bisnis *stale read* pada sistem pembayaran dibanding media sosial, serta konsep pelacakan versi data antar replika dalam simulasi. | Menggunakan pemahaman konsep *Read-Your-Writes* dan mekanisme perbandingan versi data tersebut sebagai dasar penyusunan argumen analisis pemilihan model konsistensi dan logika pengecekan versi pada simulasi replikasi Jakarta–Bandung. |