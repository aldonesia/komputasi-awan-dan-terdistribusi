# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Materi terkait:** Flat Naming, Structured Naming (DNS), Distributed Hash Table (DHT)/Chord.

## Studi Kasus

Pelanggan FoodGo kesulitan menemukan alamat IP server kurir yang **dinamis** (kurir berpindah lokasi/jaringan, IP-nya sering berubah). FoodGo butuh cara memetakan **ID Kurir** (identitas tetap) ke **alamat IP terkininya** tanpa server pusat tunggal yang jadi bottleneck/single point of failure.

## Tugas Kelompok

Implementasikan **simulasi Chord DHT** sederhana (single-process, tidak perlu jaringan sungguhan — cukup simulasi struktur data & algoritma di satu program Python) yang memetakan ID Kurir ke alamat IP mereka.

Konsep yang harus terlihat jalan dalam simulasi kalian:
1. **Consistent hashing**: ID Kurir dan ID Node di-hash ke ruang angka yang sama (mis. 0–255 untuk kesederhanaan, `m=8` bit).
2. **Ring topology**: node-node diurutkan melingkar berdasarkan hasil hash-nya.
3. **Lookup**: fungsi `lookup(kurir_id)` yang menemukan node mana yang bertanggung jawab menyimpan mapping ID Kurir tersebut → alamat IP-nya (aturan Chord: node dengan ID hash **terkecil yang lebih besar atau sama dengan** hash key, disebut *successor*).
4. **Perubahan topologi**: simulasikan minimal satu node baru bergabung (`join`) atau satu node keluar (`leave`), tunjukkan bagaimana mapping berpindah tanggung jawab ke node lain.

Skeleton disediakan di `src/chord_simulation.py` dengan fungsi hashing dan struktur ring sudah ada — bagian `lookup()`, `join()`, dan `leave()` sengaja dikosongkan.

### Cara Menjalankan

```bash
python3 src/chord_simulation.py
```

## Tugas Analisis (`README.md`)

1. Jelaskan **kenapa DHT/Chord** lebih cocok untuk kasus ini dibanding **flat naming sederhana** (mis. tabel pusat ID→IP) atau **DNS konvensional** — kaitkan dengan sifat "IP kurir sering berubah" dan kebutuhan tanpa titik gagal tunggal.
2. Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana.
3. Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.

## Jawab Tugas Analisis
1. Perbandingan DHT/Chord dengan Metode Penamaan Lain

Pada studi kasus FoodGo, sistem perlu menemukan alamat IP kurir berdasarkan ID Kurir yang bersifat tetap. Permasalahan muncul karena alamat IP kurir dapat berubah ketika kurir berpindah lokasi atau jaringan. Oleh karena itu, diperlukan mekanisme penamaan yang dapat menghubungkan ID Kurir dengan alamat IP terbaru.

Terdapat beberapa pendekatan yang dapat digunakan:

A. Flat Naming

Flat naming menggunakan tabel pusat untuk menyimpan hubungan antara ID Kurir dan alamat IP. Pendekatan ini cukup sederhana, tetapi memiliki ketergantungan pada satu server pusat. Apabila server mengalami gangguan, proses pencarian alamat IP dapat ikut terganggu. Selain itu, server pusat berpotensi menjadi bottleneck ketika jumlah permintaan meningkat.

B. DNS Konvensional

DNS (Domain Name System) digunakan untuk menerjemahkan nama domain menjadi alamat IP. DNS memiliki mekanisme caching dan redundansi untuk meningkatkan ketersediaan layanan. Namun, DNS menggunakan struktur hierarkis dan tidak secara langsung menerapkan pembagian tanggung jawab penyimpanan key seperti pada Chord DHT.

C. Distributed Hash Table (DHT) / Chord

DHT merupakan mekanisme penyimpanan data terdistribusi yang memungkinkan beberapa node berbagi tanggung jawab dalam menyimpan dan menemukan data. Pada algoritma Chord, consistent hashing digunakan untuk menentukan posisi ID node dan ID Kurir dalam ruang identifier yang sama.

Setiap mapping ID Kurir akan ditempatkan pada node yang menjadi successor dari hash ID Kurir tersebut. Ketika terdapat node baru yang bergabung atau node keluar, pembagian tanggung jawab penyimpanan dapat disesuaikan berdasarkan posisi node pada ring.

Alasan penggunaan Chord DHT pada FoodGo:

- Tidak bergantung pada satu server pusat untuk melakukan pencarian data.
- Mapping ID Kurir dapat diperbarui ketika alamat IP kurir berubah.
- Penyimpanan data didistribusikan ke beberapa node.
- Perubahan jumlah node dapat ditangani melalui mekanisme join dan leave.
- Dengan karakteristik tersebut, Chord DHT dapat menjadi pendekatan yang sesuai untuk kebutuhan penamaan terdistribusi pada FoodGo.

2. Ring Topology
  ```mermaid
graph TD
    N40((Node 40<br>bandung-1)) --> N102((Node 102<br>jakarta-2))
    N102 --> N123((Node 123<br>medan-1))
    N123 --> N136((Node 136<br>surabaya-1))
    N136 --> N177((Node 177<br>jakarta-1))
    N177 --> N40
    
    K28[kurir-002<br>Hash: 28] -.->|Disimpan di| N40
    K50[kurir-001<br>Hash: 50] -.->|Disimpan di| N102
    K132[kurir-003<br>Hash: 132] -.->|Disimpan di| N136

## Struktur Submission

```
tugas-06-penamaan-dht/
├── README.md      # Analisis + diagram ring
├── JURNAL.md
├── src/
│   └── chord_simulation.py
└── bukti/          # Output program (screenshot/log) untuk skenario join & leave
```

## Rubrik Penilaian (Tugas 6)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi lookup/join/leave benar | 35% | Consistent hashing & successor lookup sesuai aturan Chord |
| Bukti perubahan topologi (join/leave) | 25% | Output menunjukkan mapping berpindah dengan benar |
| Analisis kenapa DHT vs flat naming/DNS | 25% | Argumen spesifik ke kasus IP kurir dinamis, bukan definisi umum |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistent hashing/Chord ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/chord_simulation.py` (`find_successor`, `join`, `leave`, dst). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menelusuri manual (langkah demi langkah) bagaimana `lookup()` menemukan successor untuk salah satu ID Kurir contoh yang dipakai di `chord_simulation.py` — bukan cuma menempelkan output program.
