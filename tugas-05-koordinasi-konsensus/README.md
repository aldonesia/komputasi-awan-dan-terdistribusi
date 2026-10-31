# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.


## Diskusi Kelompok

## 1. Mengapa Sistem Terdistribusi Memerlukan Leader? (Konteks FoodGo)
Dalam arsitektur terdistribusi **FoodGo**, terdapat banyak *node* (server/worker) yang memproses pesanan pelanggan, ketersediaan stok restoran, dan alokasi kurir secara bersamaan. Tanpa adanya satu *Leader* (koordinator terpusat):
- **Masalah Urutan Pesanan (*Order Sequencing*):** Jika dua pelanggan memesan menu terakhir di restoran yang sama melalui dua *node* berbeda pada waktu hampir bersamaan, kedua *node* bisa memvalidasi pesanan tersebut secara independen dan menyebabkan *race condition* atau *double-booking* (stok menjadi minus).
- **Peran Leader:** Leader bertindak sebagai *sequencer* tunggal yang memberikan nomor urut global (*total ordering*) atau menjadi pemegang otoritas kunci (*distributed lock coordinator*) sebelum transaksi pesanan disahkan ke *database* replika.

## 2. Analisis Trade-off: Bully Algorithm vs. Raft
Mengapa memilih Bully Algorithm pada simulasi ini, dan bagaimana perbandingannya dengan algoritma konsensus modern seperti **Raft**?

| Aspek | Bully Algorithm | Raft Consensus |
| :--- | :--- | :--- |
| **Prinsip Pemilihan** | Deterministik berdasarkan **ID tertinggi** yang masih aktif. | Berdasarkan **kelengkapan log transaksi** (*up-to-date log*) dan suara mayoritas (*quorum* $N/2 + 1$). |
| **Kompleksitas Pesan** | Kasus terburuk mencapai $O(N^2)$ pesan ketika node ber-ID terendah memicu *election*. | Lebih efisien, $O(N)$ pesan per pemilihan melalui mekanisme `RequestVote`. |
| **Kelemahan Utama** | Rentan terhadap *flapping* (jika node ID tertinggi sering mati-nyala, ia terus-menerus merebut posisi leader) dan risiko *split-brain* jika jaringan terpartisi. | Implementasi jauh lebih kompleks (harus mengelola *term*, *log replication*, dan *commit index*). |
| **Kesesuaian di FoodGo** | Cocok untuk koordinasi ringan di klaster lokal yang jaringannya stabil dan setiap node memiliki akses penyimpanan bersama (*shared state*). | Wajib digunakan jika setiap node menyimpan salinan *log* pesanan lokal dan membutuhkan jaminan konsistensi data yang ketat (*strong consistency*) saat terjadi partisi jaringan. |

## 3. Hasil Pengujian Skenario

### Skenario 1: Start Normal
Saat kelima node (ID 1 s.d. 5) dinyalakan secara bersamaan:
- Setiap node memulai *election* dan mengirimkan pesan `ELECTION` ke node dengan ID lebih tinggi.
- Node 2, 3, 4, dan 5 membalas `OK` kepada pengirim ber-ID lebih rendah, sehingga node ber-ID lebih rendah menghentikan pencalonan dirinya.
- **Node 5** tidak menerima balasan `OK` karena memiliki ID tertinggi, sehingga terpilih menjadi Leader dan mengirimkan pesan `COORDINATOR` ke Node 1, 2, 3, dan 4.

### Skenario 2: Leader Mati (Re-election)
Saat proses **Node 5** dihentikan (`Ctrl+C`):
- Mekanisme *heartbeat* (`PING`) pada node lain mendeteksi bahwa Leader (Node 5) tidak lagi merespons.
- Node yang mendeteksi kegagalan segera memicu *election* baru.
- **Node 4** merespons dengan `OK` kepada node ber-ID 1, 2, dan 3, lalu mengirim `ELECTION` ke Node 5.
- Karena Node 5 sudah mati (tidak merespons hingga batas waktu *timeout* habis), **Node 4** mengambil alih peran sebagai Leader baru dan mem-broadcast `COORDINATOR` ke Node 1, 2, dan 3.
