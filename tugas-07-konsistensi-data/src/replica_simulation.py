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
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0


    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

    # Replikasi ke Bandung setelah delay
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version)
        )
        timer.start()

        print(f"[INFO] Replikasi ke Bandung tertunda {REPLICATION_DELAY} detik")


    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)


    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """Membaca saldo dengan mekanisme Read-Your-Writes."""
        replica = self.jakarta if server == "Jakarta" else self.bandung

        versi_terbaca = replica.last_write_version.get(user_id, 0)

        if versi_terbaca < versi_minimal:
            print("[INFO] Replica belum memiliki data terbaru, redirect ke Jakarta")
            return self.jakarta.read(user_id)

        return replica.read(user_id)



def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")

    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter

    # Membaca saldo dengan Read-Your-Writes
    saldo = system.baca_saldo_read_your_writes(
        user_id, "Bandung", versi_terakhir
    )

    print("Baca saldo Bandung (Read-Your-Writes):", saldo)
    print("-> Saldo tetap benar meskipun replikasi belum selesai.")


if __name__ == "__main__":
    main()
