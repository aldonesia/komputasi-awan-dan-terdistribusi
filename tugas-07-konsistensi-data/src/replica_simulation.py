"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server
RYW_MAX_WAIT = 3.0       # detik, batas tunggu mode "poll" sebelum fallback redirect ke Jakarta
RYW_POLL_INTERVAL = 0.1  # detik, jeda antar pengecekan versi pada mode "poll"
 
_T0 = time.monotonic()
_print_lock = threading.Lock()

def log(msg: str = ""):
    """Print thread-safe dengan penanda waktu relatif (t = detik sejak program mulai).
    Lock mencegah baris dari thread Timer dan thread utama saling bertabrakan."""
    with _print_lock:
        if msg.startswith("\n") or msg == "":
            print(msg)
        else:
            print(f"[t={time.monotonic() - _T0:5.2f}s] {msg}")

class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}
        self._lock = threading.Lock()  # write (thread utama) dan replicate (thread Timer) bisa bersamaan
 
    def _apply(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
 
    def write(self, user_id: str, saldo_baru: float, version: int):
        with self._lock:
            self._apply(user_id, saldo_baru, version)
        log(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru:.0f} (versi {version})")
 
    def replicate(self, user_id: str, saldo_baru: float, version: int):
        """Dipanggil oleh proses replikasi. Update yang lebih lama dari yang sudah
        dimiliki diabaikan, supaya replikasi yang tiba terlambat/tidak berurutan
        tidak menimpa data yang lebih baru."""
        with self._lock:
            if version <= self.last_write_version.get(user_id, 0):
                applied = False
            else:
                self._apply(user_id, saldo_baru, version)
                applied = True
        if applied:
            log(f"[{self.name}] REPLIKASI diterima: saldo {user_id} = {saldo_baru:.0f} (versi {version})")
        else:
            log(f"[{self.name}] REPLIKASI versi {version} diabaikan (sudah punya versi >= itu)")
 
    def read(self, user_id: str) -> float:
        with self._lock:
            return self.saldo.get(user_id, 0.0)
 
    def snapshot(self, user_id: str) -> tuple[float, int]:
        """Baca saldo dan versinya secara atomik, supaya pengecekan versi dan nilai yang dibaca konsisten."""
        with self._lock:
            return self.saldo.get(user_id, 0.0), self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")   # primary: semua penulisan masuk ke sini
        self.bandung = Replica("Bandung")   # replika: menerima salinan secara tertunda
        self.version_counter = 0
        self._lock = threading.Lock()
        self._timers: list[threading.Timer] = []
 
    def _pilih(self, server: str) -> Replica:
        return self.jakarta if server == "Jakarta" else self.bandung
 
    def top_up(self, user_id: str, jumlah: float) -> int:
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan).
        Mengembalikan nomor versi penulisan ini (dipakai client sebagai token Read-Your-Writes)."""
        with self._lock:
            self.version_counter += 1
            version = self.version_counter
            saldo_baru = self.jakarta.read(user_id) + jumlah
            self.jakarta.write(user_id, saldo_baru, version)
 
        # TODO 1: replikasi ke Bandung TERTUNDA (simulasikan dengan
        # threading.Timer(REPLICATION_DELAY, ...) yang memanggil
        # self.bandung.write(user_id, saldo_baru, version) setelah delay.
        timer = threading.Timer(
            REPLICATION_DELAY, self.bandung.replicate, args=(user_id, saldo_baru, version)
        )
        timer.start()
        self._timers.append(timer)
        log(f"[Replikasi] Jakarta -> Bandung (versi {version}) tertunda {REPLICATION_DELAY} detik")
        return version
 
    def wait_replication(self):
        """Tunggu semua replikasi yang tertunda selesai (dipakai di akhir demo)."""
        for timer in self._timers:
            timer.join()
 
    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self._pilih(server)
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """TODO 2: implementasikan Read-Your-Writes -
        jika replika yang dituju versi datanya < versi_minimal (client pernah
        melihat versi lebih baru sebelumnya), tunggu/redirect ke replika yang
        sudah punya versi tersebut (di sini cukup simulasikan dengan polling
        sampai versi replika >= versi_minimal, atau redirect ke Jakarta)."""
        pass


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
    # TODO 3: panggil baca_saldo_read_your_writes dan tunjukkan hasilnya SELALU benar
    # walau dipanggil segera setelah top_up (< REPLICATION_DELAY detik).


if __name__ == "__main__":
    main()
