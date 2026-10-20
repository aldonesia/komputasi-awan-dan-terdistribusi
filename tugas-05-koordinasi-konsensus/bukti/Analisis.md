Analisis Logika Sistem Bully Algorithm
1. Alur Kerja Pesan (on_message)
ELECTION: Ketika menerima sinyal ini dari node dengan ID lebih rendah, node akan langsung merespons dengan pesan "OK" agar node pengirim tahu ada node ber-ID lebih tinggi yang aktif. Node kemudian memicu proses pemilihannya sendiri melalui thread terpisah.

OK: Berfungsi sebagai konfirmasi bahwa node ber-ID lebih tinggi telah menerima permintaan dan sedang mengambil alih proses pemilihan. Sinyal ini melepaskan pemblokiran pada ok_event.

COORDINATOR: Berfungsi memperbarui variabel status self.leader_id agar seluruh node dalam jaringan mengakui pemenang pemilihan sebagai leader baru.

2. Mekanisme Pemilihan Leader (start_election & declare_leader)
Filtering Peer: Node menyaring seluruh peer untuk menemukan node yang memiliki ID lebih besar (higher_peers).

Kondisi Tanpa Peer Tinggi: Jika tidak ada peer dengan ID yang lebih besar, node secara otomatis memanggil declare_leader() tanpa perlu menunggu timeout.

Pengiriman & Penantian: Node menyebarkan pesan "ELECTION" ke seluruh peer ber-ID tinggi, lalu menunggu respons "OK" selama durasi timeout. Jika tidak ada respons, node menyatakan dirinya sebagai leader baru dan menyebarkan pesan "COORDINATOR" ke seluruh peer.

3. Pemantauan Kesehatan Leader (monitor_leader)
Loop periodik berjalan setiap 3 detik untuk memeriksa keberadaan leader.

Pengecekan dilakukan dengan mengirim pesan "PING" melalui TCP connection. Jika panggilan socket mengembalikan nilai False (koneksi terputus/gagal), node secara otomatis memicu proses pemilihan baru.
