# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 18 September 2026
- Peserta: - Niko Rajani Syahputra Pane
           - Bezaliel Agung Trilaksana
- Poin diskusi: Membahas Pitfall mana yang di pilih
- Perbedaan pendapat (jika ada): Liel setuju dengan pifall "the network avaliable" by peter, tetapi Niko kurang setuju  dengan itu.
  
Bukti:
![Bukti Pertemuan Discord 18 september](bukti/18-09-2026.png)

 
## 20 September 2026
- Peserta = - Niko Rajani Syahputra Pane
            - Bezaliel Agung Trilaksana
- Poin Diskusi: Membahas Soal compare antar branch + diskusi pitfall ke-3
- Perbedaan Pendapat: Kami saling mencari tau bagaimana caranya compare antar branch.
  
Bukti:
![Bukti Pertemuan Discord 18 september](bukti/20-09-2026.png)
## 21 September 2026
- Peserta = - Niko Rajani Syahputra Pane
            - Bezaliel Agung Trilaksana
- Poin Diskusi: Membahas kesimpulan, review silang dan tahap akhir jurnaling. 
- Perbedaan Pendapat: -.
  
Bukti:
![Bukti Pertemuan Discord 18 september](bukti/21-09-2026.png)

## Review Silang

- Bezaliel Agung Trilaksana mengomentari analisis Niko Rajani Syahputra Pane: 

pitch 2  "Network is Reliabel":
- Pemecahan masalahnya udah bagus, namun harus tetap diberikan waktu timeout,sebab jika hanya dibuat fitur coba lagi, otomatis pengguna tidak tau jika semisalnya transaksi sebelumnya itu telah gagal dan tiba tiba diberikan pembayaran ulang. Tetapi untuk penjelasannya tersebut sudah benar.

pitch 3 "Single Point of Failure / Monolith" :
- saya sangat setuju dengan keputusan pilihan Niko dengan pilihan Single Point of Failure, sebab semua modul system tidak bisa dijalankan didalam 1 jalur saja. Kenapa begitu? sebab semua beban diberikan pada jalur tersebut, apalagi ada notifikasi kurir dan pesanan. Data tersebut sudah sangat besar atau berat untuk menanggani 1 jalur tersebut, karena itu diberikan solusi berbagai macam jalur untuk meringankan hal tersebut.

- Niko Rajani Syahputra Pane mengomentari analisis Bezaliel Agung Trilaksana:

Pitall 1 "latency is Zero": 

- Menurut saya, bukti skenario yang di sajikan sudah sangat tepat, karena mengambil data soal timeout yang berhubungan erat dengan kasus latenzy is zero.
  solusi yang di tawarkan juga cocok untuk masalah yang ada, seperti memberikan timeout dan memberikan cache agar tidak membebani RAM dan mempercepat memproses data data yang sering di gunakan.

## Referensi 

link 
- https://dilankam.medium.com/latency-is-zero-81f3f99a9136
- https://www.cisco.com/site/us/en/learn/topics/cloud-networking/what-is-low-latency.html
- https://ably.com/blog/8-fallacies-of-distributed-computing
- https://www.geeksforgeeks.org/system-design/fallacies-of-distributed-systems/
- https://www.ruangguru.com/rea/kamus/s/spof


## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |

|18 September 2026|Claude|"Anda sebagai teknisi di software development di salah satu startup yang sedang naik daun, anda disuruh untuk mempelajari beberapa istilah istilah peter tentang 8_ fallacy distributed computing_, Anda akan diskusi dengan saya untuk meningkatkan pemahaman anda mengenai 8 fallacy distributed computing dan menghubungkannya dnegan  pekerjaan anda yang mungkin akan di temui selama bekerja di startup tersebut" |Defenisi dan pemahaman mendalam mengenai maisng maisng pitfall 8 fallacy distributed by peter|Memanfaatkan ide itu untuk kemudian menelaah dan menghubungkan pitfall mana yang cocok dengan kasus Food Go|

| 20 September 2026 | Claude | "Defenisi Single Point of Failure dan beberapa contoh studi kasusnya| Defenisi & Studi kasus single point of failure | Memanfaatkan pengetahuan itu untuk mencoba dianalisis ke studi kasus Food GO |
