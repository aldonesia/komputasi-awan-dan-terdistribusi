# Analisis 
## Mengapa RPC cocok dengan skenario yang kalian pilih di kasus ini?
RPC (Remote Procedure Call) cocok untuk kasus FoodGo karena memungkinkan modul Pembayaran dan modul Pesanan berkomunikasi dan memanggil fungsi satu sama lain melalui jaringan. RPC memungkinkan modul Pesanan memanggil fungsi pada modul Pembayaran dan menunggu hasilnya.

- Sederhana & Langsung : Modul Pesanan bisa langsung manggil fungsi cek_saldo()dan proses_pembayaran()di modul Pembayaran kayak pemanggilan fungsi biasa.

- Serba Pasti (Sinkron) : Modul Pesanan akan menungguin kepastian (pembayaran sukses/gagal) sebelum melanjutkan proses pesanan, jadi tidak bakal ada pesanan terproses kalau saldo kurang.

- Aman & Terpisah : Data saldo cuma diolah sama modul Pembayaran, modul Pesanan tidak perlu akses database saldo secara langsung.
