import hashlib

M_BITS = 8  # ruang identifier 0..255
RING_SIZE = 2**M_BITS


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

    def find_successor(self, key_hash: int) -> int | None:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash.

        Jika tidak ada, wrap-around ke node dengan hash terkecil di ring.
        """
        if not self.nodes:
            return None

        # Urutkan seluruh node_id yang aktif di dalam ring
        sorted_node_ids = sorted(self.nodes.keys())

        # Cari node pertama yang nilainya >= key_hash
        for node_id in sorted_node_ids:
            if node_id >= key_hash:
                return node_id

        # Jika key_hash lebih besar dari semua node, putar kembali ke node terkecil (wrap-around)
        return sorted_node_ids[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        target_node = self.find_successor(key_hash)

        if target_node is not None:
            self.data[key_hash] = (kurir_id, ip_kurir)
            print(
                f"[REGISTER] Kurir '{kurir_id}' (hash={key_hash}) dialokasikan ke Node ID {target_node}"
            )

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        target_node = self.find_successor(key_hash)

        # Jika key_hash ada di penyimpanan data dan node penanggung jawab ditemukan
        if key_hash in self.data and target_node is not None:
            _, ip_kurir = self.data[key_hash]
            return ip_kurir

        return None

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring dan pindahkan hak data dari successor lamanya."""
        node_id = hash_id(node_name)

        # Cari successor LAMA sebelum node baru resmi didaftarkan
        old_successor = self.find_successor(node_id)

        # Daftarkan node baru ke dalam ring
        self.nodes[node_id] = node_ip
        print(
            f"[JOIN] Node '{node_name}' (id={node_id}) bergabung dengan IP {node_ip}"
        )

        # Retribusi data: cek data mana yang kini menjadi milik node_id baru
        if old_successor is not None and old_successor != node_id:
            migrated_keys = []
            for k_hash, (k_id, _) in self.data.items():
                if self.find_successor(k_hash) == node_id:
                    migrated_keys.append(f"'{k_id}' (hash={k_hash})")

            if migrated_keys:
                print(
                    f"       -> Node ID {node_id} mengambil alih data {migrated_keys} dari Node ID {old_successor}"
                )

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring dan alihkan datanya ke successor baru."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            return

        # Identifikasi data yang saat ini dipegang oleh node yang akan keluar
        data_to_reassign = [
            (k_hash, k_id)
            for k_hash, (k_id, _) in self.data.items()
            if self.find_successor(k_hash) == node_id
        ]

        # Hapus node dari ring
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        # Alihkan penanggung jawab data ke successor baru
        for k_hash, k_id in data_to_reassign:
            new_successor = self.find_successor(k_hash)
            print(
                f"        -> Data '{k_id}' (hash={k_hash}) dialihkan ke Node ID {new_successor}"
            )


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    print("\n--- Pendaftaran Kurir ---")
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()