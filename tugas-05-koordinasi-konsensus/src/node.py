"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) harus kalian lengkapi sendiri.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK sebelum menyatakan diri leader


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()
        
        # --- TAMBAHKAN DUA BARIS INI ---
        self.is_electing = False
        self.ok_received = threading.Event()

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}")
        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_connection, args=(conn,), daemon=True).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()
            if not data:
                return
            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika node target tidak merespons (dianggap mati)."""
        try:
            with socket.create_connection(("localhost", target_port), timeout=1.0) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm (LENGKAPI BAGIAN INI) ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        # TODO 1: Tangani jenis pesan ELECTION, OK, COORDINATOR, dan PING
        if msg_type == "ELECTION":
            print(f"[Node {self.node_id}] Menerima 'ELECTION' dari node {sender_id}")
            if self.node_id > sender_id:
                # Balas "OK" ke sender bahwa ID kita lebih besar
                sender_port = self.peers.get(sender_id)
                if sender_port:
                    self.send_message(sender_port, "OK")
                
                # Jalankan election sendiri jika sedang tidak dalam proses election
                if not self.is_electing:
                    threading.Thread(target=self.start_election, daemon=True).start()

        elif msg_type == "OK":
            print(f"[Node {self.node_id}] Menerima 'OK' dari node {sender_id}")
            # Tandai bahwa ada node ber-ID lebih tinggi yang masih aktif
            self.ok_received.set()

        elif msg_type == "COORDINATOR":
            with self.lock:
                self.leader_id = sender_id
                self.is_electing = False
            print(f"[Node {self.node_id}] LEADER BARU TERDETEKSI: Node {sender_id}")

        elif msg_type == "PING":
            # Ditanggapi oleh infrastruktur handle_connection bahwa connection berhasil
            pass

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        with self.lock:
            if self.is_electing:
                return
            self.is_electing = True
            self.ok_received.clear()

        higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
        print(f"[Node {self.node_id}] Memulai election. Mengirim 'ELECTION' ke: {list(higher_peers.keys())}")

        # Jika tidak ada peer yang ID-nya lebih besar, langsung deklarasikan diri sebagai leader
        if not higher_peers:
            self.declare_leader()
            return

        # Kirim ELECTION ke semua peer yang ID-nya lebih besar
        any_sent = False
        for pid, port in higher_peers.items():
            if self.send_message(port, "ELECTION"):
                any_sent = True

        # TODO 2: Tunggu ELECTION_TIMEOUT detik untuk balasan "OK"
        got_ok = self.ok_received.wait(timeout=ELECTION_TIMEOUT)

        if not got_ok:
            # Tidak ada balasan "OK" dalam kurun waktu timeout -> deklarasikan diri sebagai leader
            print(f"[Node {self.node_id}] Tidak ada respon OK dari ID lebih tinggi dalam {ELECTION_TIMEOUT}s.")
            self.declare_leader()
        else:
            print(f"[Node {self.node_id}] Ada node ber-ID lebih tinggi yang aktif. Menunggu COORDINATOR baru...")
            with self.lock:
                self.is_electing = False

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        # TODO 3: Set leader_id dan broadcast "COORDINATOR" ke SEMUA peer
        with self.lock:
            self.leader_id = self.node_id
            self.is_electing = False

        print(f"[Node {self.node_id}] SAYA ADALAH LEADER BARU!")

        for pid, port in self.peers.items():
            self.send_message(port, "COORDINATOR")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            # TODO 4: Cek keberadaan/koneksi ke leader
            with self.lock:
                current_leader = self.leader_id
                is_currently_electing = self.is_electing

            if current_leader is not None and current_leader != self.node_id and not is_currently_electing:
                leader_port = self.peers.get(current_leader)
                # Tes ping koneksi ke leader saat ini
                if leader_port is not None:
                    is_alive = self.send_message(leader_port, "PING")
                    if not is_alive:
                        print(f"[Node {self.node_id}] LEADER MATI! Leader (Node {current_leader}) tidak merespons PING.")
                        with self.lock:
                            self.leader_id = None
                        threading.Thread(target=self.start_election, daemon=True).start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--peers", type=str, required=True,
                         help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005")
    args = parser.parse_args()

    # Asumsi konvensi port: id N selalu di port 5000+N (lihat contoh perintah di README).
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1)  # beri waktu semua node lain start dulu sebelum election awal
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
