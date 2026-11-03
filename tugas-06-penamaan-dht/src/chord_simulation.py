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

        # TODO 2: cari successor LAMA dari node_id ini (sebelum node baru dimasukkan)
        old_successor_id = None
        if self.nodes:
            old_successor_id = self.find_successor(node_id)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 3: pindahkan key yang seharusnya menjadi tanggung jawab node baru
        if old_successor_id is not None and old_successor_id != node_id:
            keys_to_transfer = []
            for key_hash in self.data.keys():
                # Data dititipkan ke node baru jika key_hash lebih kecil/sama dengan node_id
                # ATAU jika terjadi wrap-around antara node lama dan baru.
                new_responsible = self.find_successor(key_hash)
                if new_responsible == node_id:
                    keys_to_transfer.append(key_hash)
            
            for k in keys_to_transfer:
                kurir_id, ip_kurir = self.data[k]
                print(f"  -> Memindahkan data {kurir_id} (hash={k}) dari node {old_successor_id} ke node {node_id}")


    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            return

        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang node ini
        if self.nodes:
            keys_to_reassign = []
            for key_hash in self.data.keys():
                # Jika node yang baru saja keluar adalah node yang seharusnya bertanggung jawab,
                # datanya kini dialihkan ke successor baru
                new_successor_id = self.find_successor(key_hash)
                keys_to_reassign.append((key_hash, new_successor_id))
            
            for k, new_succ_id in keys_to_reassign:
                kurir_id, ip_kurir = self.data[k]
                print(f"  -> Data {kurir_id} (hash={k}) diambil alih oleh node {new_succ_id}")


    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        
        # TODO 6: implementasikan logika successor
        if not self.nodes:
            return None
            
        sorted_nodes = sorted(self.nodes.keys())
        
        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id
                
        # Wrap-around ke node terkecil jika key_hash lebih besar dari semua node
        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        
        # TODO 7: panggil find_successor(key_hash)
        successor_id = self.find_successor(key_hash)
        if successor_id is not None:
            self.data[key_hash] = (kurir_id, ip_kurir)
            print(f"[REGISTER] Kurir {kurir_id} (hash={key_hash}) disimpan di Node ID {successor_id}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        
        # TODO 8: gunakan find_successor(key_hash)
        successor_id = self.find_successor(key_hash)
        if successor_id is not None and key_hash in self.data:
            return self.data[key_hash][1]
        return None


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