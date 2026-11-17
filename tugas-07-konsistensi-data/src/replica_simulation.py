"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        # abaikan update lama yang datang terlambat (jangan menimpa versi lebih baru)
        if version <= self.last_write_version.get(user_id, 0):
            return
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru:.0f} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)

    def version(self, user_id: str) -> int:
        return self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float) -> int:
        """Top-up selalu ditulis dulu ke server Jakarta. Mengembalikan versi data
        (token yang disimpan client untuk Read-Your-Writes)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # Replikasi ke Bandung tertunda REPLICATION_DELAY detik
        threading.Timer(
            REPLICATION_DELAY, self.bandung.write, args=(user_id, saldo_baru, version)
        ).start()
        print(f"[Replikasi] Jakarta -> Bandung dijadwalkan {REPLICATION_DELAY} detik lagi")
        return version

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """Read-Your-Writes: kalau versi data di replika tujuan < versi_minimal
        (versi yang sudah pernah dilihat/ditulis client), minta saldo terbaru
        ke Jakarta (sesuai sequence diagram B), bukan membaca data lama."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        if replica.version(user_id) >= versi_minimal:
            return replica.read(user_id)
        print(f"[{replica.name}] versi {replica.version(user_id)} < {versi_minimal} "
              f"(stale) -> redirect ke Jakarta")
        return self.jakarta.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    saldo = system.baca_saldo_naif(user_id, "Bandung")
    print("Baca saldo dari Bandung (naif):", saldo)
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya 0 (BUG)")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")
    versi_terakhir = system.top_up(user_id, 20000)
    time.sleep(0.5)
    print("Baca saldo dari Bandung (naif)  :", system.baca_saldo_naif(user_id, "Bandung"),
          "<- stale")
    saldo = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir)
    print("Baca saldo dari Bandung (RYW)   :", saldo, "<- benar (70000)")

    time.sleep(REPLICATION_DELAY)
    print("\nSetelah replikasi selesai:")
    saldo = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir)
    print("Baca saldo dari Bandung (RYW)   :", saldo, "(Bandung sudah sinkron)")


if __name__ == "__main__":
    main()