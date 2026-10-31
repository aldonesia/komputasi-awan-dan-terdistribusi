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
Karena kurir FoodGo terus berpindah jaringan (misalnya dari Wi-Fi resto ke sinyal seluler), alamat IP mereka berubah sangat sering. Jika menggunakan tabel pusat (flat naming), rentetan update IP kurir yang masuk setiap menit akan memicu bottleneck dan mematikan server utama. Jika menggunakan DNS, pelanggan tidak bisa melacak posisi akurat karena sering kali diarahkan ke IP kurir yang sudah mati akibat cache DNS yang lambat diperbarui (TTL). Dengan DHT/Chord, setiap kali kurir berganti IP di jalan, alamat barunya langsung disimpan seketika (real-time) hanya pada node penanggung jawab spesifik di ring, memastikan pelanggan selalu menerima IP kurir yang terkini tanpa membebani dan membahayakan satu server pusat pun.

2. Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana.  

```mermaid
flowchart LR
    A["Bandung<br/>ID 40<br/>Kurir-002 (Hash 28)"]
    B["Jakarta-2<br/>ID 102<br/>Kurir-001 (Hash 50)"]
    C["Medan<br/>ID 123"]
    D["Surabaya<br/>ID 136<br/>Kurir-003 (Hash 132)"]
    E["Jakarta-1<br/>ID 177"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> A
```
  
3. Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.  
Pada simulasi kita mengeluarkan node node-jakarta-1 dengan ID 177 dari ring. Sebelum node tersebut keluar, ring memiliki 5 node. Setelah node-jakarta-1 keluar, jumlah node menjadi 4. Sistem kemudian memperbarui topologi ring dan menentukan kembali node yang bertanggung jawab atas setiap mapping. Dari hash Kurir yang digunakan, tidak ada mapping yang sebelumnya menjadi tanggung jawab node Jakarta-1. Oleh karena itu, tidak terjadi perpindahan tanggung jawab mapping Kurir pada skenario ini, dapat dilihat dari output:  
```
--- Sebuah node keluar ---
[LEAVE] Node 'node-jakarta-1' (id=177) keluar dari ring
[LOOKUP] kurir-001 ditemukan di node 102
kurir-001 -> 192.168.1.10
[LOOKUP] kurir-002 ditemukan di node 40
kurir-002 -> 192.168.1.11
PS C:\Kuliah\Sistem Terdist
```  

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
