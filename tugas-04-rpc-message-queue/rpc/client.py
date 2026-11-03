"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()

    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    saldo = proxy.cek_saldo("user1")
    end = time.time()

    print(f"Hasil saldo: {saldo}")
    print(f"Waktu tempuh (Round Trip): {end - start:.4f} detik\n")

    print("Memanggil proses_pembayaran('user1', 20000) ...")

    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    hasil_bayar = proxy.proses_pembayaran("user1", 20000)
    print(f"Hasil pembayaran: {hasil_bayar}")


if __name__ == "__main__":
    main()