# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: 
Eventual Consistency: Performanya paling cepet dan ringan, tapi bahaya buat data keuangan karena ada jeda waktu (replication lag). Jadi, saldo user bisa kelihatan belum update kalau dia pindah server atau transaksi di wilayah lain dalam hitungan detik.
Sequential Consistency: Sangat aman karena semua server dipaksa sinkron urutannya secara ketat secara global, tapi bikin aplikasi jadi lemot dan berat karena harus nunggu semua replika selesai kerja bareng.
Client-Centric Consistency (Read-Your-Writes): Jalan tengah yang paling masuk akal. Fokusnya cuma mastiin kalau user yang baru aja melakukan aksi write (misal: top-up saldo), dia wajib langsung dapet hasil terbaru itu pas read (belanja) di server mana pun, tanpa perlu bikin seluruh sistem global jadi lemot.

- Kesimpulan akhir & alasan: Client-Centric Consistency dengan mekanisme Read-Your-Writes
Alasan: Model ini paling pas karena memberikan keseimbangan yang ideal antara kecepatan akses (performance) dan keamanan data keuangan (correctness). Pengguna bisa top-up di satu kota dan langsung belanja di kota lain dengan mulus tanpa takut transaksinya ditolak gara-gara saldo telat sinkron, sementara sistem tetap efisien tanpa beban latensi yang berlebihan.

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 17-11-2026 | GEMINI | "Bagaimana cara kerja mekanisme Read-Your-Writes dalam Client-Centric Consistency untuk mengatasi stale read?" | Mekanisme Read-Your-Writes bekerja dengan cara memberikan token nomor versi kepada klien saat melakukan perubahan (seperti top-up) di suatu server, yang kemudian wajib dibawa oleh klien saat mengakses server lain; jika server tujuan mendapati data lokalnya masih tertinggal (basi), server tersebut akan menunda proses dan menarik data terbaru dari server asal hingga versinya sesuai dengan token klien, sehingga masalah stale read dapat dicegah dan pengguna selalu melihat hasil pembaruannya sendiri dengan akurat. | - |
| 17-11-2026 | GEMINI | "Tolong jelaskan konsep dasar penggunaan versioning atau timestamp pada server replika untuk mendeteksi data yang tertinggal." | Konsep dasar penggunaan versioning atau timestamp pada server replika adalah dengan menyematkan tanda pengenal unik yang terus meningkat pada setiap perubahan data sebagai "nomor edisi", di mana setiap server replika turut mencatat versi atau waktu pembaruan terakhir yang mereka miliki sehingga sistem dapat membandingkannya untuk mendeteksi apakah data lokal masih tertinggal (stale), dan jika kedaluwarsa, server dapat segera melakukan sinkronisasi sebelum memproses permintaan selanjutnya. | - |
