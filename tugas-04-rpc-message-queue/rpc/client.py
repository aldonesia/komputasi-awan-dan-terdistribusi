from tracemalloc import start
from weakref import proxy
import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000") # ganti dengan xmlrpc.client.ServerProxy(...)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    try:
        hasil_saldo = proxy.cek_saldo("user1")
        waktu_tempuh = time.time() - start
        print(f"Hasil: Saldo Rp{hasil_saldo} | Diselesaikan dalam waktu: {waktu_tempuh:.4f} detik")

        print("Memanggil proses_pembayaran('user1', 20000) ...")
        # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
        hasil_bayar = proxy.proses_pembayaran("user1", 20000)
        print(f"Hasil eksekusi pembayaran: {hasil_bayar}")
    except ConnectionRefusedError:
        print("Gagal terhubung ke server. Pastikan server.py sudah dijalankan di terminal lain.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
if __name__ == "__main__":
    main()