# Jurnal Proses — Tugas 5

## Implementasi Bully

- **Kendala saat mengisi TODO 1–4:** Memahami alur komunikasi antarnode, mekanisme pengiriman pesan ELECTION dan OK, serta cara menentukan leader berdasarkan ID node. Selain itu, perlu memastikan bahwa node dapat mendeteksi ketika leader berhenti dan memulai pemilihan leader baru.
- **Solusi:** Memahami alur Bully Algorithm dan menguji implementasi secara bertahap menggunakan lima proses node dengan port yang berbeda.

## Skenario 1: Start normal

- **Leader yang terpilih:** Node 5 (ID 5).
- **Log/observasi:** Lima node dijalankan pada port 5001–5005. Node dengan ID tertinggi, yaitu Node 5, terpilih sebagai leader. Node lain menerima informasi coordinator sehingga mengetahui leader yang sedang aktif. Hasil pengujian juga didokumentasikan melalui tangkapan layar dan log setiap node di folder `bukti/`.

## Skenario 2: Leader dimatikan

- **Leader baru yang terpilih:** Node 4 (ID 4).
- **Berapa lama waktu sampai leader baru terdeteksi:** Belum dicatat secara pasti. Waktu ini perlu diukur dari saat Node 5 dihentikan sampai log menunjukkan Node 4 terpilih sebagai leader. Catat hasil pengukuran aktual dalam detik.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| [20/10/2026] | Gemini | Meminta penjelasan konsep Bully Algorithm dan gambaran umum tahapan pengerjaan tugas. | Memahami bahwa node dengan ID tertinggi yang masih aktif berpeluang menjadi leader dan bahwa kegagalan leader dapat memicu pemilihan ulang. | Menggunakan pemahaman konsep untuk mempelajari instruksi dan mengembangkan implementasi secara mandiri. |
| [20/10/2026] | Claude | Meminta panduan umum pengujian lima node. | Menyiapkan pengujian kondisi normal dan kondisi ketika leader dihentikan, serta menyimpan log dan tangkapan layar sebagai bukti. | Menjalankan program sendiri, mengamati hasil aktual, dan mendokumentasikan hasil pengujian berdasarkan keluaran program. |

