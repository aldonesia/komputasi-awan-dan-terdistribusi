"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: hubungkan client ke server RPC.
    with xmlrpc.client.ServerProxy("http://localhost:8000") as proxy:
        try:
            print(
                "Memanggil cek_saldo('user1') ... "
                "menunggu respons sinkron",
                flush=True,
            )

            start = time.perf_counter()

            # TODO 2: panggil cek_saldo dan ukur waktu menunggu.
            saldo = proxy.cek_saldo("user1")

            elapsed = time.perf_counter() - start

            print(f"Saldo user1: Rp{saldo:,.0f}")
            print(f"Waktu menunggu respons: {elapsed:.2f} detik")

            print(
                "Memanggil proses_pembayaran('user1', 20000) ...",
                flush=True,
            )

            # TODO 3: panggil pembayaran dan tampilkan hasil.
            hasil = proxy.proses_pembayaran("user1", 20000)

            print(f"Status: {hasil['status']}")
            print(f"Saldo akhir: Rp{hasil['saldo_akhir']:,.0f}")
            print(f"Pesan: {hasil['pesan']}")

        except xmlrpc.client.Fault as error:
            print(f"Kesalahan dari server RPC: {error.faultString}")

        except xmlrpc.client.ProtocolError as error:
            print(f"Kesalahan HTTP: {error.errcode} {error.errmsg}")

        except OSError as error:
            print(f"Koneksi RPC gagal: {error}")
            print(
                "Pastikan server.py berjalan; "
                "koneksi mungkin terputus saat proses."
            )


if __name__ == "__main__":
    main()