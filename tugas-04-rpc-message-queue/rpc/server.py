"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""
import os 
import time
from xmlrpc import server
from xmlrpc.server import SimpleXMLRPCServer

RPC_DELAY = float(os.environ.get("RPC_DELAY", "0"))

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    time.sleep(RPC_DELAY)
    # TODO 1: kembalikan saldo dari dict `saldo_user`.
    # Jika user_id tidak ada, putuskan sendiri perilakunya (mis. return 0 atau raise error)
    # dan jelaskan keputusan ini di README.md.
    if user_id not in saldo_user:
        raise ValueError(f"User '{user_id}' tidak ditemukan")
    return saldo_user[user_id]


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    time.sleep(RPC_DELAY)
    # TODO 2: validasi saldo cukup, kurangi saldo_user[user_id], dan kembalikan
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}
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
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    print("RPC server modul Pembayaran berjalan di port 8000...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server dihentikan.")
        server.server_close()


if __name__ == "__main__":
    main()  
