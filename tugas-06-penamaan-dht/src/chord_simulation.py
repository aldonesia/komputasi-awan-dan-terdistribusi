"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode(), usedforsecurity=False).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # node_id (hasil hash) -> nama node (untuk label di log)
        self.node_names: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        if node_id in self.nodes:
            print(f"[JOIN] GAGAL: hash '{node_name}' (id={node_id}) bentrok dengan "
                  f"{self._label(node_id)}")
            return

        # TODO 2: cari successor LAMA sebelum node baru bergabung.
        old_successor = self.find_successor(node_id)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        self.node_names[node_id] = node_name
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        if old_successor is None:
            print("       Node pertama di ring, belum ada data yang dipindahkan.")
            return

        # TODO 3: key yang kini menjadi tanggung jawab node baru (log saja).
        moved = self._keys_owned_by(node_id)
        if not moved:
            print(f"       Tidak ada key yang berpindah (successor lama: "
                  f"{self._label(old_successor)}).")
        for kh in moved:
            print(f"       {self._kurir_label(kh)} pindah: "
                  f"{self._label(old_successor)} -> {self._label(node_id)}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[LEAVE] GAGAL: node '{node_name}' (id={node_id}) tidak ada di ring")
            return

        keys_held = self._keys_owned_by(node_id)
        label = self._label(node_id)

        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]
        del self.node_names[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        if not self.nodes:
            print("        Ring kosong: data tidak punya penanggung jawab lagi.")
            return

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang node ini.
        if not keys_held:
            print(f"        Tidak ada key yang harus dipindahkan dari {label}.")
        for kh in keys_held:
            new_owner = self.find_successor(kh)
            print(f"        {self._kurir_label(kh)} pindah: "
                  f"{label} -> {self._label(new_owner)}")

    def find_successor(self, key_hash: int) -> int | None:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash.
        Jika tidak ada, wrap-around ke node dengan hash terkecil di ring."""
        # TODO 6
        if not self.nodes:
            return None
        candidates = [nid for nid in self.nodes if nid >= key_hash]
        if candidates:
            return min(candidates)
        return min(self.nodes)

    def _label(self, node_id: int) -> str:
        return f"{self.node_names.get(node_id, '?')} (id={node_id})"

    def _kurir_label(self, key_hash: int) -> str:
        kurir_id = self.data[key_hash][0]
        return f"{kurir_id} (hash={key_hash})"

    def _keys_owned_by(self, node_id: int) -> list[int]:
        """Key di self.data yang saat ini menjadi tanggung jawab node_id."""
        return [kh for kh in self.data if self.find_successor(kh) == node_id]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        # TODO 7
        key_hash = hash_id(kurir_id)
        owner = self.find_successor(key_hash)
        if owner is None:
            print(f"[REGISTER] GAGAL: ring kosong, '{kurir_id}' tidak bisa disimpan")
            return
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] {kurir_id} (hash={key_hash}) -> {self._label(owner)}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        # TODO 8
        key_hash = hash_id(kurir_id)
        owner = self.find_successor(key_hash)
        if owner is None:
            return None
        entry = self.data.get(key_hash)
        return entry[1] if entry else None


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
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()