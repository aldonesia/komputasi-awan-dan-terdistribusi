"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

from xmlrpc.server import SimpleXMLRPCServer
import time

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: kembalikan saldo dari dict `saldo_user`.
    
    # Saya menambahkan jeda simulasi komputasi agar bukti blocking 
    # di sisi client nantinya terlihat jelas pada kalkulasi waktu tempuh.
    time.sleep(1.5)
    
    if user_id in saldo_user:
        return float(saldo_user[user_id])
    
    # Mengembalikan 0 jauh lebih aman secara arsitektur daripada melempar error.
    # Jika kita melempar exception, client harus memiliki mekanisme try-catch.
    # Nilai 0.0 menandakan identitas valid namun hampa, sehingga program client tidak crash.
    return 0.0


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    # TODO 2: validasi saldo cukup, kurangi saldo_user[user_id], dan kembalikan
    # dict berisi minimal {"status": "sukses"/"gagal", "saldo_akhir": ...}
    
    if user_id not in saldo_user:
        return {"status": "gagal", "pesan": "User tidak ditemukan", "saldo_akhir": 0.0}
    
    if saldo_user[user_id] >= jumlah:
        saldo_user[user_id] -= jumlah
        return {"status": "sukses", "saldo_akhir": float(saldo_user[user_id])}
    
    return {"status": "gagal", "pesan": "Saldo tidak mencukupi", "saldo_akhir": float(saldo_user[user_id])}


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