"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8          # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip

        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung; gunakan find_successor() dengan node_id INI dikecualikan
        # dulu dari self.nodes saat mencari).
        saved_ip = self.nodes.pop(node_id)
        old_successor = self.find_successor(node_id) if self.nodes else None
        self.nodes[node_id] = saved_ip

        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
        # tanggung jawab node baru (key dengan hash <= node_id, tapi masih
        # dipegang oleh successor lama) ke bawah tanggung jawab node baru.
        # (Untuk simulasi sederhana, cukup print log siapa mengambil alih apa -
        # tidak perlu benar-benar memindahkan struktur data kompleks.)
        if old_successor is not None and old_successor != node_id:
            for key_hash, (kurir_id, _) in self.data.items():
                if self.find_successor(key_hash) == node_id:
                    print(
                        f"  -> [MIGRASI JOIN] Key '{kurir_id}' (hash={key_hash}) "
                        f"diambil alih oleh node {node_id} ('{node_name}') "
                        f"dari successor lama node {old_successor}"
                    )

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[LEAVE] Node '{node_name}' (id={node_id}) tidak ada di dalam ring")
            return

        # Catat semua key yang tadinya menjadi tanggung jawab node ini sebelum keluar
        keys_held = [
            key_hash for key_hash in self.data
            if self.find_successor(key_hash) == node_id
        ]

        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        if self.nodes:
            for key_hash in keys_held:
                new_successor = self.find_successor(key_hash)
                kurir_id, _ = self.data[key_hash]
                print(
                    f"  -> [MIGRASI LEAVE] Key '{kurir_id}' (hash={key_hash}) "
                    f"dipindahkan dari node {node_id} ('{node_name}') "
                    f"ke successor baru node {new_successor} ({self.nodes[new_successor]})"
                )

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            raise ValueError("Ring masih kosong, belum ada node yang bergabung.")

        sorted_node_ids = sorted(self.nodes.keys())
        for node_id in sorted_node_ids:
            if node_id >= key_hash:
                return node_id

        # Wrap-around ke node dengan nilai hash terkecil di ring
        return sorted_node_ids[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        successor_id = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(
            f"[REGISTER] Kurir '{kurir_id}' (hash={key_hash}) -> IP {ip_kurir} "
            f"disimpan pada node {successor_id} ({self.nodes[successor_id]})"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        if not self.nodes or key_hash not in self.data:
            print(f"[LOOKUP] Kurir '{kurir_id}' (hash={key_hash}) tidak ditemukan di ring")
            return None

        successor_id = self.find_successor(key_hash)
        _, ip_kurir = self.data[key_hash]
        print(
            f"[LOOKUP] Kurir '{kurir_id}' (hash={key_hash}) dilayani oleh "
            f"node {successor_id} ({self.nodes[successor_id]}) -> IP: {ip_kurir}"
        )
        return ip_kurir


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    print("=== 1. INISIALISASI RING (4 NODE AWAL) ===")
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-bandung-1", "10.0.0.2")
    ring.join("node-surabaya-1", "10.0.0.3")
    ring.join("node-medan-1", "10.0.0.4")

    print("\n=== 2. REGISTRASI DATA KURIR ===")
    ring.register_kurir("kurir-001", "192.168.1.101")
    ring.register_kurir("kurir-002", "192.168.1.102")
    ring.register_kurir("kurir-003", "192.168.1.103")
    ring.register_kurir("kurir-004", "192.168.1.104")

    print("\n=== 3. LOOKUP AWAL ===")
    ring.lookup("kurir-001")
    ring.lookup("kurir-002")
    ring.lookup("kurir-003")
    ring.lookup("kurir-004")

    print("\n=== 4. SKENARIO NODE BARU BERGABUNG (JOIN) ===")
    ring.join("node-makassar-1", "10.0.0.5")
    ring.lookup("kurir-001")
    ring.lookup("kurir-002")
    ring.lookup("kurir-003")
    ring.lookup("kurir-004")

    print("\n=== 5. SKENARIO NODE KELUAR (LEAVE) ===")
    ring.leave("node-surabaya-1")
    ring.lookup("kurir-001")
    ring.lookup("kurir-002")
    ring.lookup("kurir-003")
    ring.lookup("kurir-004")


if __name__ == "__main__":
    main()
w
