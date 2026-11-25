# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu: Kelompok mempertimbangkan Public Cloud, Hybrid Cloud, dan Private Cloud. Public Cloud ditolak karena infrastruktur tidak sepenuhnya berada di bawah kendali negara, sedangkan Hybrid Cloud memiliki kompleksitas sinkronisasi antar-segmen. Kelompok memilih Private Cloud karena kerahasiaan data kependudukan (NIK, alamat, biometrik) dan kepatuhan UU PDP menjadi prioritas utama.

## Diskusi service model per komponen
* **IaaS (Database Utama):** Digunakan untuk menyimpan data sensitif (NIK, alamat, identitas, dan data biometrik) agar pemerintah memiliki kendali penuh atas server, sistem operasi, *storage*, jaringan, serta pembatasan akses sesuai kebijakan keamanan internal.
* **PaaS (Aplikasi Backend & API Integrasi):** Digunakan untuk aplikasi backend, API verifikasi identitas, dan layanan integrasi instansi (Dukcapil daerah, kepolisian, dan bank) guna mempermudah pengembangan serta pemeliharaan tanpa mengelola seluruh infrastruktur dasar.
* **SaaS (Aplikasi Pendukung):** Tidak dijadikan model utama karena pemerintah membutuhkan kontrol lebih besar terhadap pemrosesan data sensitif; hanya dimanfaatkan untuk aplikasi pendukung yang tidak mengelola data kependudukan sensitif.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
