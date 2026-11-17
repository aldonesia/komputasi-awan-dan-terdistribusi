"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

import time
from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: kembalikan saldo dari dict `saldo_user`.
    # Jika user_id tidak ada, putuskan sendiri perilakunya (mis. return 0 atau raise error)
    # dan jelaskan keputusan ini di README.md.
    print(f"[Pembayaran] cek_saldo({user_id!r}) dipanggil")
    time.sleep(1)  # simulasi latensi proses agar efek menunggu terlihat
    if user_id not in saldo_user:
        raise ValueError(f"user_id '{user_id}' tidak ditemukan")
    return saldo_user[user_id]


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    # TODO 2: validasi saldo cukup, kurangi saldo_user[user_id], dan kembalikan
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}
    print(f"[Pembayaran] proses_pembayaran({user_id!r}, {jumlah}) dipanggil")
    time.sleep(3)
    if user_id not in saldo_user:
        return {"status": "gagal", "alasan": "user tidak ditemukan", "saldo_akhir": None}
    if jumlah <= 0:
        return {"status": "gagal", "alasan": "jumlah harus > 0", "saldo_akhir": saldo_user[user_id]}
    if saldo_user[user_id] < jumlah:
        return {"status": "gagal", "alasan": "saldo tidak cukup", "saldo_akhir": saldo_user[user_id]}
 
    saldo_user[user_id] -= jumlah
    return {"status": "sukses", "saldo_akhir": saldo_user[user_id]}


def main():
    # TODO 3: buat SimpleXMLRPCServer di localhost port 8000,
    # daftarkan fungsi cek_saldo & proses_pembayaran, lalu serve_forever().
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    main()
