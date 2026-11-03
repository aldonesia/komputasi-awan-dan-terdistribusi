"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Simulasi consistent hashing, lookup, dan perubahan anggota ring.
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
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
        if node_id in self.nodes:
            raise ValueError(f"Node '{node_name}' memiliki ID {node_id} yang sudah dipakai")

        old_owners = {key: self.find_successor(key) for key in self.data} if self.nodes else {}
        self.nodes[node_id] = node_ip
        print(f"Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        moved = [(key, old_owners[key]) for key in self.data
                 if old_owners and self.find_successor(key) != old_owners[key]]
        if moved:
            for key, old_owner in moved:
                courier_id, _ = self.data[key]
                print(f"  {courier_id} (hash={key}): node {old_owner} -> node {node_id}")
        else:
            print("  Tidak ada mapping yang berpindah.")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            raise ValueError(f"Node '{node_name}' (id={node_id}) tidak ada di ring")

        old_owners = {key: self.find_successor(key) for key in self.data}
        del self.nodes[node_id]
        print(f"Node '{node_name}' (id={node_id}) keluar dari ring")
        moved = [(key, old_owners[key], self.find_successor(key))
                 for key in self.data if old_owners[key] == node_id] if self.nodes else []
        if moved:
            for key, old_owner, new_owner in moved:
                courier_id, _ = self.data[key]
                print(f"  {courier_id} (hash={key}): node {old_owner} -> node {new_owner}")
        else:
            if self.nodes:
                print("  Tidak ada mapping yang dipegang node ini.")
            else:
                print("  Ring kini kosong; mapping belum memiliki successor.")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        if not self.nodes:
            raise LookupError("Ring kosong: belum ada node yang dapat melayani lookup")
        for node_id in sorted(self.nodes):
            if node_id >= key_hash:
                return node_id
        return min(self.nodes)

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        owner = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"Daftar {kurir_id} (hash={key_hash}) -> {ip_kurir}; disimpan di node {owner}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        self.find_successor(key_hash)  # Resolusi penanggung jawab untuk key ini.
        record = self.data.get(key_hash)
        if record is None or record[0] != kurir_id:
            return None
        return record[1]


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-67", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-2")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()
