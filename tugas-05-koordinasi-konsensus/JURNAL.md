## Jurnal Proses — Tugas 5
## Implementasi Bully
- **Kendala saat mengisi TODO 1-4:**
  1. **Menunggu balasan `OK` tanpa memblokir server.** `start_election()` harus berhenti menunggu, sedangkan balasan `OK` datang lewat `on_message` di thread lain. Solusinya `threading.Event()` (`ok_received`): `on_message` memanggil `set()` saat `OK` tiba, dan `start_election()` memakai `wait(timeout=ELECTION_TIMEOUT)`. Karena `start_election()` bisa memblokir, pemanggilannya dari `on_message` dilakukan di thread baru supaya handler socket tetap bisa menerima pesan lain.
  2. **Election ganda di node yang sama.** Satu node bisa menerima beberapa pesan `ELECTION` hampir bersamaan, sehingga election berjalan berkali-kali. Saya menambah flag `election_running` (dijaga `lock`) agar hanya satu election aktif per node.
  3. **Node menunggu pengumuman setelah menerima `OK`.** Menerima `OK` hanya berarti ada node lebih tinggi yang hidup. Saya menambah event `coordinator_received` dan timeout `COORDINATOR_TIMEOUT` supaya node mengulang election bila pengumuman `COORDINATOR` tidak datang.
  4. **`COORDINATOR` dari node ber-ID lebih kecil.** Node ber-ID lebih besar menolak pesan itu dan menjalankan election sendiri, karena node yang lebih tinggi seharusnya menjadi leader.
5.	**Kendala menjalankan program.** Tombol Run di VS Code menjalankan node.py tanpa argumen sehingga error --id, --port, --peers required. Perintah python juga tidak dikenali di PowerShell, jadi saya memakai path lengkap python3.15.exe dan menjalankan 5 node di 5 terminal terpisah.
Skenario 1: Start normal
- **Leader yang terpilih:** Node 5 (port 5005)
- **Log/observasi:** Node 1 sampai 5 dijalankan di 1 terminal. Node ber-ID kecil mengirim `ELECTION` ke node di atasnya dan dibalas `OK`, lalu node yang lebih tinggi menjalankan election sendiri. Node 5 tidak punya peer ber-ID lebih tinggi sehingga langsung menyatakan diri leader dan mengirim `COORDINATOR` ke semua node. Pada akhirnya Node 1 sampai 4 menampilkan "Leader sekarang: Node 5". Karena beberapa node memicu election bersamaan, log memuat banyak pesan `ELECTION`, `OK`, dan `COORDINATOR`. Setelah stabil, tidak ada election baru
## Skenario 2: Leader dimatikan
- **Leader baru yang terpilih:** Node 4 (port 5004)
- **Berapa lama waktu sampai leader baru terdeteksi:** Sekitar 3 detik setelah Node 5 dihentikan dengan `Ctrl+C`, mengikuti interval `time.sleep(3)` di `monitor_leader`. Setelah `PING` ke Node 5 gagal, node lain memicu election. Node 4 langsung menjadi leader karena satu-satunya peer di atasnya (Node 5) tidak bisa dihubungi, sehingga tidak ada waktu tunggu `OK`. Lalu Node 4 mengirim `COORDINATOR`, dan Node 1 sampai 3 menampilkan "Leader sekarang: Node 4". Pesan `COORDINATOR` dari Node 4 bisa muncul beberapa kali karena beberapa node mendeteksi kematian leader bersamaan.
- 
Log Penggunaan AI (Level 2)


| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20/10/2026 | Claude | "berikan rancangan logika event-driven untuk sinkronisasi balasan OK pada Bully Algorithm di Python" | AI menyarankan `threading.Event` yang di-`set()` oleh handler `OK` dan ditunggu `start_election()` dengan `wait(timeout)`, plus nomor ronde untuk mengabaikan `OK` basi dan lock agar tidak ada election ganda | Konsep Event dan pencegahan election ganda dipakai. Nomor ronde tidak dipakai karena kerangka `node.py` tidak membawa nomor ronde di pesan |

