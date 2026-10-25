"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import http.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000", allow_none=True)

    try: 
        print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
        start = time.time()
        # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
        #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
        saldo = proxy.cek_saldo("user1")
        durasi = time.time() - start
        print(f"   -> saldo user1: {saldo} (waktu tunggu: {durasi:.3f} detik)")

        print("Memanggil proses_pembayaran('user1', 20000) ...")
        # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
        start = time.time()
        hasil = proxy.proses_pembayaran("user1", 20000)
        durasi = time.time() - start
        print(f"   -> Hasil: {hasil} (waktu tunggu: {durasi:.3f} detik)")

    except ConnectionRefusedError:
        print("GAGAL: server RPC tidak aktif (koneksi ditolak). Jalankan rpc/server.py dulu.")
    except xmlrpc.client.Fault as e:
        print(f"GAGAL: server membalas error -> {e.faultString}")
    except (ConnectionError, xmlrpc.client.ProtocolError, OSError, http.client.RemoteDisconnected) as e:
        print(f"GAGAL: koneksi terputus di tengah request -> {type(e).__name__}: {e}")
    
if __name__ == "__main__":
    main()
