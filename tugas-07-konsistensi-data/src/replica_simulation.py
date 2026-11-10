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

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int, mode: str="poll", max_wait: float = RYW_MAX_WAIT) -> float:
        """TODO 2: implementasikan Read-Your-Writes -
        jika replika yang dituju versi datanya < versi_minimal (client pernah
        melihat versi lebih baru sebelumnya), tunggu/redirect ke replika yang
        sudah punya versi tersebut (di sini cukup simulasikan dengan polling
        sampai versi replika >= versi_minimal, atau redirect ke Jakarta)."""
        pass
        replica = self._pilih(server)

        # Replika sudah cukup baru -> langsung baca (kasus paling umum, tanpa overhead)
        saldo, versi = replica.snapshot(user_id)
        if versi >= versi_minimal:
            log(f"[RYW] {server} sudah punya versi {versi} (>= {versi_minimal}), baca langsung")
            return saldo

        # Replika tertinggal
        if mode == "redirect":
            log(f"[RYW] {server} baru versi {versi} < {versi_minimal}, redirect ke Jakarta")
            return self.jakarta.snapshot(user_id)[0]

        log(f"[RYW] {server} baru versi {versi} < {versi_minimal}, menunggu replikasi...")
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            time.sleep(RYW_POLL_INTERVAL)
            saldo, versi = replica.snapshot(user_id)  # snapshot atomik: saldo & versi konsisten
            if versi >= versi_minimal:
                log(f"[RYW] {server} sudah mencapai versi {versi}, baca dari {server}")
                return saldo

        # Timeout -> fallback ke primary agar tetap benar
        log(f"[RYW] timeout {max_wait}s menunggu {server}, fallback redirect ke Jakarta")
        return self.jakarta.snapshot(user_id)[0]

def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("\n=== Skenario dengan Read-Your-Writes ===")
    versi_terakhir = system.top_up(user_id, 20000)  # token RYW = versi penulisan ini
    # Dipanggil segera setelah top_up (< REPLICATION_DELAY), mode poll:
    saldo = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir)
    print("Baca saldo dari Bandung (RYW, poll):", saldo)
    assert saldo == 70000, "RYW gagal: saldo tidak sesuai"
    print("-> Benar: 70000 (50000 + 20000), walau dibaca segera setelah top-up")

    print("\n=== Read-Your-Writes mode redirect ===")
    versi_terakhir = system.top_up(user_id, 10000)
    saldo = system.baca_saldo_read_your_writes(
        user_id, "Bandung", versi_terakhir, mode="redirect"
    )
    print("Baca saldo dari Bandung (RYW, redirect):", saldo)
    assert saldo == 80000
    print("-> Benar: 80000, langsung dibaca dari Jakarta tanpa menunggu")

    print("\n=== Read-Your-Writes: poll timeout lalu fallback ke Jakarta ===")
    versi_terakhir = system.top_up(user_id, 5000)
    saldo = system.baca_saldo_read_your_writes(
        user_id, "Bandung", versi_terakhir, mode="poll", max_wait=0.5
    )
    print("Baca saldo dari Bandung (RYW, fallback):", saldo)
    assert saldo == 85000
    print("-> Benar: 85000, walau max_wait lebih pendek dari delay replikasi")

    system.wait_replication()  # tunggu semua replikasi selesai sebelum program berakhir
    print("\nSetelah semua replikasi selesai:")
    print("  Jakarta:", system.jakarta.read(user_id))
    print("  Bandung:", system.bandung.read(user_id))
    # TODO 3: panggil baca_saldo_read_your_writes dan tunjukkan hasilnya SELALU benar
    # walau dipanggil segera setelah top_up (< REPLICATION_DELAY detik).


if __name__ == "__main__":
    main()
