"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")
    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    saldo = proxy.cek_saldo("user1")
    print(f"  Saldo user1: {saldo}  (client menunggu {time.time() - start:.2f} detik)")
    
    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    start = time.time()
    hasil = proxy.proses_pembayaran("user1", 20000)
    print(f"  Hasil: {hasil}  (client menunggu {time.time() - start:.2f} detik)")

    print("Memanggil cek_saldo('user_percobaan') ... (user tidak ada)")
    try:
        proxy.cek_saldo("user_percobaan")
    except xmlrpc.client.Fault as e:
        print(f"  Server membalas error: {e.faultString}")
    
if __name__ == "__main__":
    main()
