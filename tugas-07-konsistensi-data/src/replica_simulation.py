import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server
POLL_INTERVAL = 0.1      # detik, jeda polling saat menunggu replikasi
MAX_WAIT = 1.0           # detik, batas tunggu sebelum redirect ke Jakarta


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}
        self._lock = threading.Lock()

    def write(self, user_id: str, saldo_baru: float, version: int):
        with self._lock:
            # Abaikan update yang lebih lama dari data yang sudah dimiliki replika
            if version <= self.last_write_version.get(user_id, 0):
                return
            self.saldo[user_id] = saldo_baru
            self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        with self._lock:
            return self.saldo.get(user_id, 0.0)

    def versi(self, user_id: str) -> int:
        with self._lock:
            return self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def _get_replica(self, server: str) -> Replica:
        return self.jakarta if server == "Jakarta" else self.bandung

    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1 (selesai): replikasi ke Bandung TERTUNDA
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version),
        )
        timer.start()
        print(f"[Sistem] Replikasi ke Bandung akan tertunda {REPLICATION_DELAY} detik")
        return version

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        return self._get_replica(server).read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """TODO 2 (selesai): Read-Your-Writes.

        Jika versi data di replika yang dituju < versi_minimal (versi yang sudah
        pernah dilihat/ditulis client), tunggu sebentar (polling) sampai replika
        mengejar. Jika batas tunggu habis, redirect pembacaan ke Jakarta yang
        sudah punya versi tersebut.
        """
        replica = self._get_replica(server)
        batas = time.time() + MAX_WAIT

        while replica.versi(user_id) < versi_minimal:
            if time.time() >= batas:
                print(f"[{replica.name}] Versi {replica.versi(user_id)} < {versi_minimal}, "
                      f"REDIRECT baca ke Jakarta")
                return self.jakarta.read(user_id)
            time.sleep(POLL_INTERVAL)

        return replica.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("Tanpa Read-Your-Writes")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)")

    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n Dengan Read-Your-Writes ")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter

    # TODO 3 (selesai): dipanggil segera setelah top_up (< REPLICATION_DELAY detik)
    hasil = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir)
    print("Baca saldo dari Bandung (Read-Your-Writes):", hasil)
    print("-> Benar: 70000" if hasil == 70000 else "-> SALAH, seharusnya 70000")

    # Beri waktu timer replikasi selesai sebelum program keluar
    time.sleep(REPLICATION_DELAY + 0.5)


if __name__ == "__main__":
    main()
