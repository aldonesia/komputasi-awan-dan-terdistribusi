"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai Python standard library - tidak perlu install dependency.
"""

from xmlrpc.server import SimpleXMLRPCServer
import math
import time

# Simulasi database saldo pengguna.
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo pengguna."""
    # TODO 1: ambil saldo dari saldo_user.
    if user_id not in saldo_user:
        raise ValueError("Pengguna tidak ditemukan.")

    print(
        f"Menerima cek_saldo untuk {user_id}; "
        "memproses selama 2 detik...",
        flush=True,
    )

    # Jeda untuk demonstrasi komunikasi sinkron.
    time.sleep(2)

    return saldo_user[user_id]


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Periksa saldo dan proses pembayaran."""
    # TODO 2: validasi pembayaran dan kembalikan hasil.
    if user_id not in saldo_user:
        return {
            "status": "gagal",
            "saldo_akhir": 0,
            "pesan": "Pengguna tidak ditemukan.",
        }

    if (
        isinstance(jumlah, bool)
        or not isinstance(jumlah, (int, float))
        or not math.isfinite(jumlah)
        or jumlah <= 0
    ):
        return {
            "status": "gagal",
            "saldo_akhir": saldo_user[user_id],
            "pesan": "Jumlah pembayaran harus angka positif dan terbatas.",
        }

    if saldo_user[user_id] < jumlah:
        return {
            "status": "gagal",
            "saldo_akhir": saldo_user[user_id],
            "pesan": "Saldo tidak cukup.",
        }

    saldo_user[user_id] -= jumlah

    print(
        f"Pembayaran {user_id} sebesar {jumlah} berhasil.",
        flush=True,
    )

    return {
        "status": "sukses",
        "saldo_akhir": saldo_user[user_id],
        "pesan": "Pembayaran berhasil.",
    }


def main():
    # TODO 3: buat server, daftarkan fungsi, lalu jalankan.
    with SimpleXMLRPCServer(("localhost", 8000)) as server:
        server.register_function(cek_saldo, "cek_saldo")
        server.register_function(
            proses_pembayaran,
            "proses_pembayaran",
        )

        print(
            "RPC server modul Pembayaran berjalan di port 8000...",
            flush=True,
        )

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nRPC server dihentikan.", flush=True)


if __name__ == "__main__":
    main()