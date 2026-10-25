
"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash ID node atau kurir ke ruang identifier 0..255."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id -> IP node
        self.nodes = {}

        # node_id -> {hash_kurir: (kurir_id, ip_kurir)}
        self.data = {}

    def find_successor(self, key_hash: int) -> int:
        """Cari successor berdasarkan hash, dengan wrap-around."""
        if not self.nodes:
            raise RuntimeError("Ring belum memiliki node")

        urut = sorted(self.nodes.keys())

        for node_id in urut:
            if node_id >= key_hash:
                return node_id

        return urut[0]


    def join(self, node_name: str, node_ip: str):
        node_id = hash_id(node_name)

        if node_id in self.nodes:
            print(f"[JOIN] Node {node_name} sudah ada")
            return

        # Simpan daftar node lama sebelum node baru masuk
        old_node_ids = list(self.nodes.keys())

        # Tambahkan node baru
        self.nodes[node_id] = node_ip
        self.data[node_id] = {}

        print(f"[JOIN] Node {node_name} bergabung dengan id={node_id}")

        for old_node in old_node_ids:
            for key_hash in list(self.data[old_node].keys()):
                new_successor = self.find_successor(key_hash)
                print(
                    f"[CEK] kurir_hash={key_hash}, "
                    f"successor={new_successor}, node_baru={node_id}"
                )

                if new_successor == node_id:
                    record = self.data[old_node].pop(key_hash)
                    self.data[node_id][key_hash] = record

                    kurir_id, ip_kurir = record
                    print(
                        f"[PINDAH] {kurir_id} ({ip_kurir}) "
                        f"dari node {old_node} ke node {node_id}"
                    )


    def leave(self, node_name: str):
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[LEAVE] Node {node_name} tidak ditemukan")
            return

        # Simpan data node yang keluar
        data_keluar = self.data.pop(node_id)
        del self.nodes[node_id]

        print(f"[LEAVE] Node {node_name} keluar dari ring")

        if not self.nodes:
            print("[LEAVE] Tidak ada node tersisa")
            return

        # Alihkan seluruh data ke successor yang baru
        for key_hash, record in data_keluar.items():
            successor = self.find_successor(key_hash)
            self.data[successor][key_hash] = record

            kurir_id, ip_kurir = record
            print(
                f"[PINDAH] {kurir_id} ({ip_kurir}) "
                f"dari node {node_id} ke node {successor}"
            )

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)

        self.data[node_id][key_hash] = (kurir_id, ip_kurir)

        print(
            f"[REGISTER] {kurir_id} (hash={key_hash}) "
            f"disimpan di node {node_id}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)

        record = self.data[node_id].get(key_hash)

        if record is not None:
            print(
                f"[LOOKUP] {kurir_id} ditemukan "
                f"di node {node_id}"
            )
            return record[1]

        print(f"[LOOKUP] {kurir_id} tidak ditemukan")
        return None


def main():
    ring = ChordRing()

    # Skenario awal: empat node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Registrasi kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")
    ring.register_kurir("kurir-test-13", "192.168.1.99")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-surabaya-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
