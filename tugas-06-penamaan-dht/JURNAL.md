# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): ...
- Cara memperbaikinya: ...

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: 
    - Sebelum, kurir-001 dipegang node-jakarta-2 (id=102):
    lookup(kurir-001): hash=50 -> node id=102
    kurir-001 -> 192.168.1.10
    Node baru bergabung dan mengambil alih kurir-001:
    [JOIN] Node 'node-semarang-1' (id=77) bergabung, alamat 10.0.0.5. Mengambil alih key: [('kurir-001', 50)]
    - Sesudah, kurir-001 dipegang node-semarang-1 (id=77):
    lookup(kurir-001): hash=50 -> node id=77
    kurir-001 -> 192.168.1.10
    IP kurir tetap 192.168.1.10; yang berubah hanya node penanggung jawabnya.

- Hasil sebelum & sesudah node keluar:
    - Sebelum, kurir-003 dipegang node-surabaya-1 (id=136):
    lookup(kurir-003): hash=132 -> node id=136
    kurir-003 -> 192.168.1.12
    Node keluar dan key diwariskan ke successor-nya:
    [LEAVE] Node 'node-surabaya-1' (id=136) keluar dari ring. Key yang ditransfer ke successor baru: [('kurir-003', 132, 177)]
    - Sesudah, kurir-003 dipegang node-jakarta-1 (id=177):
    lookup(kurir-003): hash=132 -> node id=177
    kurir-003 -> 192.168.1.12
    IP tetap 192.168.1.12 sehingga tidak ada data yang hilang. kurir-001 tidak terpengaruh dan tetap di node 77:
    lookup(kurir-001): hash=50 -> node id=77
    kurir-001 -> 192.168.1.10

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
