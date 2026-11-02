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

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        sorted_node_ids = sorted(self.nodes.keys())
        for nid in sorted_node_ids:
            if nid >= key_hash:
                return nid
        # Jika tidak ada yang >= key_hash, wrap-around ke ID terkecil di ring
        return sorted_node_ids[0]

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 2: cari successor LAMA dari node_id ini (sebelum node baru dimasukkan ke self.nodes)
        old_successor = None
        if self.nodes:
            old_successor = self.find_successor(node_id)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 3: pindahkan semua key di self.data yang sekarang menjadi tanggung jawab node baru
        # (yaitu key dengan hash <= node_id, yang sebelumnya dipegang oleh successor lama)
        if old_successor is not None and old_successor != node_id:
            keys_to_migrate = []
            for k_hash in list(self.data.keys()):
                # Aturan kepemilikan di Chord: data dikelola node pertama yang ID-nya >= k_hash
                # Jika node baru berada di antara predecessor lama dan old_successor, data berpindah ke node baru.
                # Sederhananya dalam simulasi ini: key yang hash-nya <= node_id (atau wrap-around) diambil alih.
                if old_successor < node_id:
                    if old_successor < k_hash <= node_id:
                        keys_to_migrate.append(k_hash)
                else:  # Kondisi wrap-around ring
                    if k_hash <= node_id or k_hash > old_successor:
                        keys_to_migrate.append(k_hash)
            
            for k_hash in keys_to_migrate:
                kurir_info = self.data[k_hash]
                print(f"  -> Migrasi data kurir '{kurir_info[0]}' (hash={k_hash}) dari successor lama (id={old_successor}) ke node baru (id={node_id})")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            return

        # Tentukan successor tujuan migrasi data sebelum node dihapus
        temp_nodes = {k: v for k, v in self.nodes.items() if k != node_id}
        successor_id = None
        if temp_nodes:
            # Cari successor di sisa node
            sorted_temp = sorted(temp_nodes.keys())
            for nid in sorted_temp:
                if nid >= node_id:
                    successor_id = nid
                    break
            if successor_id is None:
                successor_id = sorted_temp[0]

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang node ini, pindahkan
        keys_to_migrate = [k_hash for k_hash in self.data.keys() if self.find_successor(k_hash) == node_id]
        for k_hash in keys_to_migrate:
            kurir_info = self.data[k_hash]
            if successor_id is not None:
                print(f"  -> Migrasi data kurir '{kurir_info[0]}' (hash={k_hash}) dari node keluar (id={node_id}) ke successor (id={successor_id})")

        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node penanggung jawab,
        # lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        responsible_node = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] Kurir '{kurir_id}' (hash={key_hash}) disimpan di Node ID {responsible_node}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node penanggung jawab,
        # lalu kembalikan ip_kurir dari self.data jika ada.
        responsible_node = self.find_successor(key_hash)
        if key_hash in self.data:
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