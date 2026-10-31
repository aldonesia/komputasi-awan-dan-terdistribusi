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

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        if node_id in self.nodes:
            print(f"[JOIN] Node '{node_name}' sudah ada")
            return

        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung, gunakan find_successor() dengan node_id INI dikecualikan
        # dulu dari self.nodes saat mencari).
        old_successors = {}

        for key_hash in self.data:
            old_successors[key_hash] = self.find_successor(key_hash)

        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) "f"bergabung, alamat {node_ip}")

        # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
        # tanggung jawab node baru (key dengan hash <= node_id, tapi masih
        # dipegang oleh successor lama) ke bawah tanggung jawab node baru.
        # (Untuk simulasi sederhana, cukup print log siapa mengambil alih apa -
        # tidak perlu benar-benar memindahkan struktur data kompleks.)
        for key_hash, (kurir_id, _) in self.data.items():

            old_successor = old_successors[key_hash]
            new_successor = self.find_successor(key_hash)

            if old_successor != new_successor:
                print(
                    f"[TRANSFER] {kurir_id}: "
                    f"node {old_successor} -> node {new_successor}"
                )

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[LEAVE] Node '{node_name}' tidak ditemukan")
            return

        if len(self.nodes) <= 1:
            print("[LEAVE] Tidak bisa mengeluarkan node terakhir")
            return
        
        # TODO 4: hapus node_id dari self.nodes.
        transferred_data = []

        for key_hash, (kurir_id, _) in self.data.items():
            old_successor = self.find_successor(key_hash)

            if old_successor == node_id:
                transferred_data.append((key_hash, kurir_id))

        del self.nodes[node_id]

        print(
            f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring"
        )

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        for key_hash, kurir_id in transferred_data:
            new_successor = self.find_successor(key_hash)

            print(
                f"[TRANSFER] {kurir_id}: "
                f"node {node_id} -> node {new_successor}"
            )

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            raise ValueError("Ring belum memiliki node")

        sorted_nodes = sorted(self.nodes.keys())

        for node_id in sorted_nodes:
            if node_id >= key_hash:
                return node_id

        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        successor = self.find_successor(key_hash)

        self.data[key_hash] = (kurir_id, ip_kurir)

        print(
            f"[REGISTER] {kurir_id} (hash={key_hash}) "
            f"disimpan di node {successor}"
        )

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)

        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        successor = self.find_successor(key_hash)

        result = self.data.get(key_hash)

        if result is None:
            print(f"[LOOKUP] {kurir_id} tidak ditemukan")
            return None

        print(f"[LOOKUP] {kurir_id} ditemukan di node {successor}")

        return result[1]

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