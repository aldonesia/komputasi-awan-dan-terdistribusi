# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 22 September 2026
- **Peserta:** Naufal Fudhail, Diandra Nanditya Mulkis, Samuel Nelson Wabiser
- **Poin diskusi:** 
  - Ngumpul bahas kasus FoodGo. Kelihatan banget ada masalah di komen `# network is always reliable, no need for retry`. Ini fix jadi poin pertama buat dikerjain Naufal.
  - Diandra nemuin masalah di modul pesanan yang nungguin pembayaran tanpa batas waktu. Kita sepakat ini masuk *fallacy "latency is zero"*.
  - Bahas soal server yang *crash* pas jam makan siang. Ini jelas gara-gara semua modul dijalanin di satu proses yang sama (monolitik), jadi pas satu berat, semua ikut mati.
  - Pembagian tugas untuk di README: Naufal (Pitfall 1), Diandra (Pitfall 2), Samuel (Pitfall 3 & Kesimpulan).
- **Kebuntuan/Perubahan pikiran:** Tadi sempet debat sedikit buat bedain fungsi *retry* sama *timeout* karena mirip-mirip. Setelah diskusi ulang baca referensi, akhirnya sepakat kalau *retry* itu buat ngakalin *request* yang gagal/putus di jalan, sedangkan *timeout* itu buat mutusin koneksi kalau *service* lain kelamaan ngerespons biar server nggak *hang*.

## Review Silang
- Diandra ngecek bagian Naufal: Penjelasan soal *cascading failure* masuk akal, gara-gara *retry* serentak servernya malah bisa down.
- Naufal ngecek bagian Samuel: Tambahin info soal ribetnya ngurus *microservices*, soalnya tim kecil pasti kewalahan ngurus banyak *container*.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di `../RUBRIK-UMUM.md`. Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 22 September 2026 | Gemini | Meminta bantuan brainstorming 3 pitfall dan struktur kerangka jawaban untuk studi kasus FoodGo. | AI memberikan penjabaran untuk asumsi "network is reliable", "latency is zero", dan "single point of failure", beserta ide solusi (exponential backoff, circuit breaker, microservices) dan trade-off-nya. | Tim menyusun ulang argumen AI dengan gaya bahasa sendiri, memotong bagian yang tidak perlu, menghubungkan penjelasan secara spesifik dengan gejala di skenario FoodGo, dan membagi tugas penulisan akhir ke tiap anggota. |
