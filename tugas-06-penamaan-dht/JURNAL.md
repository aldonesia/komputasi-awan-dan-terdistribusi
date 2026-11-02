# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Sempat lupa menangani kondisi wrap around ring apabila nilai `key_hash` lebih besar daripada seluruh ID node yang terdaftar di dalam ring
- Cara memperbaikinya: dengan menambahkan mekanisme fallback yg mengembalikan elemen pertama dari daftar ID node yang sudah diurutkan (`sorted_node_ids[0]`) jika perulangan penelusuran node tidak menemukan ID yang memenuhi syarat $\get key\_hash$

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: Sebelum `node-medan-1` (id=123) bergabung, `kurir-001` (hash=50) dikelola oleh Node ID 136,setelah `node-medan-1` bergabung, sistem menjalankan proses migrasi data secara otomatis untuk `kurir-001` dan `kurir-002` dari successor lama ke node baru (id=123) karena posisinya kini menjadi penanggung jawab data tersebutd
- Hasil sebelum & sesudah node keluar: Sebelum `node-jakarta-1` (id=177) keluar, lookup data `kurir-001` dan `kurir-002` mengembalikan alamat IP dengan benar, setelah node tersebut keluar (`[LEAVE]`), hasil lookup tetap konsisten dan sukses mengembalikan IP kurir karena struktur ring dan pemetaan data tetap dipertahankan oleh node-node aktif yang tersisa

## Analisis Simulasi Chord DHT untuk Pemetaan IP Kurir FoodGo
 1. Analisis Keunggulan DHT/Chord Dibanding Flat Naming / DNS Konvensional
* **Menghindari Titik Gagal Tunggal (*Single Point of Failure* / SPOF):**
  Pada sistem *flat naming* tradisional (seperti tabel pusat ID $\to$ IP dalam satu database terpusat), apabila server utama mengalami gangguan atau *down*, seluruh sistem pelacakan dan manajemen kurir lumpuh total. Sebaliknya, arsitektur Chord DHT bersifat terdesentralisasi, di mana tanggung jawab penyimpanan data terdistribusi secara merata ke seluruh node yang aktif di dalam jaringan.
* **Penanganan IP Kurir yang Dinamis:** 
  IP seorang kurir sangat sering berubah (akibat berpindah jaringan seluler, Wi-Fi, atau terputusnya koneksi). DNS konvensional memiliki jeda waktu *TTL (Time to Live)* dan mekanisme *caching* hirarkis yang kurang responsif untuk pembaruan data secara *real-time*. Melalui *consistent hashing* pada Chord DHT, perubahan IP kurir dapat langsung dipetakan ulang dan disimpan secara akurat pada node *successor* yang bertanggung jawab dengan efisiensi pencarian berbiaya $O(\log N)$.

2. Tanggung jawab Node pada id kurir
  node-jakarta-1 $\rightarrow$ ID: 74node-jakarta-2 $\rightarrow$ ID: 154node-bandung-1 $\rightarrow$ ID: 227node-surabaya-1 $\rightarrow$ ID: 94node-medan-1 (yang bergabung kemudian) $\rightarrow$ ID: 181Urutan ring awal sebelum node tambahan masuk (diurutkan dari terkecil):74 (jakarta-1) $\rightarrow$ 94 (surabaya-1) $\rightarrow$ 154 (jakarta-2) $\rightarrow$ 227 (bandung-1)
  
3. Yang terjadi saat node keluar dari ring
  Ketika sebuah node meninggalkan ring (misalnya saat node-jakarta-1 keluar), seluruh data mapping ID Kurir dan IP yang sebelumnya dikelola oleh node tersebut tidak akan hilang.
  Berdasarkan aturan dasar arsitektur Chord DHT:
  Pengambil Alih Tanggung Jawab: Tanggung jawab atas kunci (keys) atau data Kurir yang tadinya dipegang oleh node yang keluar akan otomatis dialihkan ke node successor terdekat berikutnya (node dengan ID valid terdekat setelahnya di dalam ring).
  Mekanisme Migrasi: Program mendeteksi kunci-kunci yang penanggung jawab awalnya (find_successor) adalah node yang keluar, lalu memindahkan kepemilikan data tersebut ke node successor yang tersisa agar ketersediaan data (availability) tetap terjaga dan tidak terjadi data loss.
  Dukungan output porgram:
  Saat node-jakarta-1 dengan ID: 74 keluar dari ring, program secara otomatis mendeteksi bahwa kurir-001 (yang sebelumnya menjadi tanggung jawab node 74) harus dipindahkan. Data tersebut dimigrasikan ke node-surabaya-1 (ID: 94) yang bertindak sebagai successor baru di dalam ring. Ketika dilakukan fungsi ring.lookup("kurir-001") setelah node keluar, sistem tetap berhasil menemukan dan mengembalikan alamat IP kurir secara akurat berkat pengalihan tanggung jawab ke node successor-nya.


## 2. Visualisasi Ring Topology
Diagram berikut merepresentasikan topologi ring melingkar (berbasis *wrap-around*) dari simulasi node dan pemetaan ID hash:

graph TD
    J1["node-jakarta-1 (ID: 74)"] -->|"Successor"| S1["node-surabaya-1 (ID: 94)"]
    S1 -->|"Successor"| J2["node-jakarta-2 (ID: 154)"]
    J2 -->|"Successor"| M1["node-medan-1 (ID: 181)"]
    M1 -->|"Successor"| B1["node-bandung-1 (ID: 227)"]
    B1 -->|"Successor (Wrap-around)"| J1

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 16/10/2026 | Gemini | aku memiliki tugas komputasi awan terdistribusi dengan 3 anggota kelompok, bantu aku membagi jobdesk dan berikan penjelasan tugasnya | Memberikan rancangan lengkap logika fungsi `find_successor`, `join`, `leave`, `register_kurir`, dan `lookup` pada Chord DHT dan memberikan pembagian jobdesk anggota 2 dan 3| Kode dimasukkan ke dalam file `chord_simulation.py` dan running melalui terminal hingga menghasilkan output migrasi data yang sesuai dengan file 'output week6.png'|
| 02/11/2026 | Gemini AI | buatkan kode mermaidnya vertikal | graph TD J1["node-jakarta-1 (ID: 74)"] -->"Successor" S1["node-surabaya-1 (ID: 94)"] S1 -->"Successor" J2["node-jakarta-2 (ID: 154)"] J2 --> "Successor" M1["node-medan-1 (ID: 181)"] M1 -->"Successor" B1["node-bandung-1 (ID: 227)"]  B1 -->"Successor (Wrap-around)" J1 | Menjadi sebuah grafik ring topology sesuai dengan simulasi yang telah dibuat |