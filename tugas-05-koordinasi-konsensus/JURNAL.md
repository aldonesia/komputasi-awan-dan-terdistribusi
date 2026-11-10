# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:
1. ada beberapa pesan yang muncul dalam satu waktu karena adanya beberapa *thread* mencoba *print* log dalam satu waktu, sehingga kami memutuskan untuk membuat objek kunci agar hanya ada satu *thread* yang  menge-*print* log dalam satu waktu.
2. kami sempat bingung bagaimana alur yang bisa dijadikan bukti karena ketiadaan format waktu pada code awal kami. sehingga kami menambahkan stempel waktu di setiap pesan log.

## Skenario 1: Start normal
- Leader yang terpilih: node 5
- Log/observasi: 
  - Node 5 memulai election ke peer lebih tinggi `{}` (karena tidak ada peer dengan ID lebih besar), sehingga langsung menyatakan diri `LEADER` dan mem-broadcast `COORDINATOR`.
  - Node 1-4 saling mengirim `ELECTION` ke node yang memiliki ID lebih besar dan menerima `OK` dari node-node di atasnya, lalu berhenti mencalonkan diri.
  - Setelah menerima `COORDINATOR` dari node 5, semua node 1-4 mencatat `Leader sekarang: node 5`.
  - Node 5 dua kali menjadi leader karena menerima `ELECTION` dari node 1-4 setelah ia sudah terpilih, lalu ia membalas dan memulai election lagi. Akibatnya `COORDINATOR` dikirim dua kali (redundan), tetapi hasil akhirnya tetap konsisten.
  - Jumlah pesan untuk 5 node: `ELECTION` = 10, `OK` = 10, `COORDINATOR` = 8 (total 28 pesan).
  - Bukti: `bukti/skenario1_node1.txt` sampai `bukti/skenario1_node5.txt`.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: node 4
- Berapa lama waktu sampai leader baru terdeteksi:
  - Kematian node 5 terdeteksi pertama kali oleh node 1 pada **17:20:43** (`Leader node 5 tidak merespons, memulai election`). Deteksi bisa terlambat hingga 3 detik dari saat node 5 mati karena `monitor_leader` melakukan ping tiap 3 detik.
  - Node 4 menyatakan diri leader pada **17:20:48** (±5 detik setelah deteksi pertama), karena ia menunggu `ELECTION_TIMEOUT` 2 detik tanpa `OK` dari node 5 dan pengiriman pesan ke node mati memakan waktu.
  - Seluruh node mengakui node 4 sebagai leader paling lambat pada **17:20:51** (node 3), yaitu **±8 detik** setelah deteksi pertama. Selisih antar node terjadi karena `declare_leader` mengirim `COORDINATOR` ke peer satu per satu secara berurutan.
  - Selama ±8 detik tersebut sistem tidak memiliki leader yang valid.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19/10/2026 | Claude AI | Saya ingin berdiskusi dulu sebelum menulis kode. Beberapa hal yang sedang saya pikirkan: 1. Di declare_leader(), menurut kamu apa saja yang perlu terjadi saat sebuah node menyatakan diri sebagai leader? Saya merasa pesan COORDINATOR harus dikirim ke semua peer, bukan hanya yang id-nya lebih tinggi. Apakah pemikiran itu benar, dan apa yang sebaiknya terjadi kalau ada peer yang sudah mati? 2. Untuk monitor_leader(), bagaimana cara terbaik mendeteksi leader yang mati? Saya kepikiran mengirim PING secara periodik. Menurutmu apa saja kondisi yang harus dilewati supaya monitor tidak bermasalah, misalnya saat belum ada leader, saat node sendiri adalah leader, atau saat election sedang berlangsung?3. Apakah ada risiko race condition atau konflik antara monitor_leader() dan start_election() yang perlu saya waspadai? 4. Coba lihat juga kode TODO 1 dan 2 yang sudah saya tulis. Apakah ada bagian yang kurang tepat atau berpotensi menimbulkan bug?  | Node dengan id lebih tinggi bisa saja baru hidup lagi dan belum tahu siapa leader-nya. Node dengan id lebih rendah perlu tahu siapa leader barunya agar monitor_leader() mereka mem-ping node yang benar. Belum ada leader (leader_id is None): tidak ada yang bisa di-ping. Node sendiri adalah leader: mem-ping diri sendiri tidak ada gunanya. Election sedang berjalan (electing == True): jangan ikut campur. Port leader tidak ada di peers: pengaman agar tidak crash. Dua election bersamaan. monitor_leader() dan on_message (saat menerima ELECTION) bisa sama-sama memanggil start_election(). Ini sudah kamu tangani dengan flag electing dan lock, jadi sudah aman. Membaca leader_id dan electing tanpa lock di monitor bisa menghasilkan nilai setengah usang. Solusinya, baca keduanya sekaligus dalam satu blok with self.lock. Reset yang menimpa data baru. Setelah PING gagal, bisa saja COORDINATOR baru masuk dan mengisi leader_id. Maka reset hanya dilakukan jika leader_id masih sama dengan leader lama. Event got_ok / got_coordinator yang di-clear() di awal tiap putaran berpotensi menghapus sinyal yang datang sepersekian detik sebelumnya. Dampaknya kecil, karena paling buruk election diulang setelah timeout. | Intinya, benar bahwa COORDINATOR harus dikirim ke semua peer, bukan cuma yang id-nya lebih tinggi. Node yang id-nya lebih rendah perlu tahu siapa leader barunya, dan node yang baru hidup lagi juga belum tahu apa-apa. Kalau ada peer yang mati, cukup dicatat di log saja, karena send_message() sudah mengembalikan False saat gagal.Untuk monitor_leader(), PING periodik memang pendekatan yang pas. Cukup lewati pengecekan kalau belum ada leader, kalau node sendiri yang jadi leader, atau kalau election sedang berjalan. Kalau PING gagal, reset leader_id lalu panggil start_election(). Soal race condition, flag electing dan lock yang sudah kamu buat sebenarnya sudah cukup menjaga supaya tidak ada dua election jalan bersamaan. Tinggal pastikan leader_id dan electing dibaca sekaligus dalam satu blok lock, dan reset leader hanya dilakukan kalau nilainya masih leader lama. Kode TODO 1 dan 2 kamu sudah bagus. Ada satu bug nyata: print("Leader sekarang: ...") di on_message posisinya di luar if/elif, jadi muncul untuk semua jenis pesan dengan id yang salah. Pindahkan ke dalam cabang COORDINATOR. Selain itu, hapus sisa print “TODO” di akhir on_message dan akhir start_election. Untuk mengujinya, jalankan 5 node dan tunggu node 5 jadi leader. Matikan node 5, dan dalam sekitar 3 detik node 4 akan mengambil alih. Nyalakan lagi node 5, dan ia akan menang election lalu mengambil posisi leader kembali. |
