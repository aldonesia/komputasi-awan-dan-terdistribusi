# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Sempat mengalami error AttributeError: Node object has no attribute is_electing saat pertama kali menjalankan program karena variabel is_electing dan ok_received lupa belum didefinisikan pada fungsi __init__. sehingga program tidak bisa running dan terjadi error, masalah diselesaikan dengan mendefinisikan atribut tersebut serta menambahkan threading.Event() untuk menangani timeout pesan OK (vaylan)

## Skenario 1: Start normal
- Leader yang terpilih: Node 5
- Log/observasi: Pada saat node dinyalakan bertahap dari 1 sampai 5, node ber-ID lebih rendah sempat menyatakan diri sebagai leader sementara karena belum menerima respon dari ID yang lebih tinggi, namun setelah Node 5 dinyalakan, Node 5 berhasil membroadcast pesan COORDINATOR dan seluruh node (node 1-4) memperbarui leader mereka ke node 5 (vaylan)

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4
- Berapa lama waktu sampai leader baru terdeteksi: Sekitar 3-4 detik  (vaylan)

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 16/10/2026 | Gemini | Tolong bantu aku revisi kodenya dari foto yg ku berikan | Memberikan rancangan `start_election`, `declare_leader`, dan `monitor_leader` menggunakan `threading.Event` | Kode diimplementasikan langsung ke file program node.py|
| 16/10/2026 | Gemini | Waktu coba running terjadi "AttributeError: 'Node' object has no attribute 'is_electing'" bantu aku untuk fix error ini dan jelaskan penyebabnya kenapa| Menjelaskan penyebab error karena atribut `is_electing` belum didefinisikan di `__init__` | Menambahkan inisialisasi `self.is_electing = False` dan `self.ok_received = threading.Event()` pada konstruktor `__init__`. |
