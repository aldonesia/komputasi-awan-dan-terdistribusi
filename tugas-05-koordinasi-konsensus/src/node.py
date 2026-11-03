"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) tidak diubah.
Logika Bully Algorithm (TODO 1-4) sudah dilengkapi.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0    # detik menunggu balasan OK sebelum menyatakan diri leader
COORDINATOR_TIMEOUT = 4.0 # detik menunggu COORDINATOR setelah menerima OK


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()

        # Sinkronisasi election
        self.ok_received = threading.Event()           # di-set saat pesan OK tiba
        self.coordinator_received = threading.Event()  # di-set saat pesan COORDINATOR tiba
        self.election_running = False                  # cegah election ganda di node yang sama

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

    # ---------- Logika Bully Algorithm ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Dipanggil setiap kali node ini menerima pesan dari node lain."""
        if msg_type != "PING":
            print(f"[Node {self.node_id}] Menerima '{msg_type}' dari node {sender_id}")

        # TODO 1
        if msg_type == "ELECTION":
            # Hanya node ber-ID lebih besar yang boleh "membully" pengirim.
            if self.node_id > sender_id:
                sender_port = self.peers.get(sender_id)
                if sender_port:
                    self.send_message(sender_port, "OK")
                # Jalankan di thread lain agar handler socket tidak terblokir saat wait().
                threading.Thread(target=self.start_election, daemon=True).start()

        elif msg_type == "OK":
            # Ada node lebih tinggi yang hidup -> jangan jadi leader.
            self.ok_received.set()

        elif msg_type == "COORDINATOR":
            if sender_id < self.node_id:
                # Pengirim ber-ID lebih kecil mengaku leader, padahal kita lebih berhak.
                # Tolak, lalu ambil alih lewat election sendiri.
                print(f"[Node {self.node_id}] Menolak COORDINATOR dari node {sender_id} (ID lebih kecil)")
                threading.Thread(target=self.start_election, daemon=True).start()
            else:
                with self.lock:
                    self.leader_id = sender_id
                self.coordinator_received.set()
                print(f"[Node {self.node_id}] Leader sekarang: Node {sender_id}")

        # "PING" hanya dipakai untuk cek hidup-mati; tidak perlu tindakan.

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        # Cegah dua election berjalan bersamaan di node yang sama.
        with self.lock:
            if self.election_running:
                return
            self.election_running = True

        try:
            while True:
                # TODO 2
                self.ok_received.clear()
                self.coordinator_received.clear()

                higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
                print(f"[Node {self.node_id}] Mulai election ke peer lebih tinggi: {higher_peers}")

                # Kirim ELECTION; hitung berapa peer tinggi yang benar-benar terjangkau.
                reachable = [pid for pid, p in higher_peers.items()
                             if self.send_message(p, "ELECTION")]

                if not reachable:
                    # Tidak ada node lebih tinggi yang hidup -> kita leader.
                    self.declare_leader()
                    return

                if not self.ok_received.wait(timeout=ELECTION_TIMEOUT):
                    # Terjangkau tapi tidak membalas OK dalam batas waktu.
                    self.declare_leader()
                    return

                # Ada yang membalas OK: tunggu dia mengumumkan diri sebagai COORDINATOR.
                if self.coordinator_received.wait(timeout=COORDINATOR_TIMEOUT):
                    return
                print(f"[Node {self.node_id}] COORDINATOR tidak datang, ulangi election")
        finally:
            with self.lock:
                self.election_running = False

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        # TODO 3
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] Saya jadi leader! Broadcast COORDINATOR")
        for pid, port in self.peers.items():
            self.send_message(port, "COORDINATOR")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            # TODO 4
            with self.lock:
                current_leader = self.leader_id
                busy = self.election_running

            if busy or current_leader == self.node_id:
                continue

            if current_leader is None:
                # Belum tahu leader sama sekali (mis. leader baru belum terdengar).
                threading.Thread(target=self.start_election, daemon=True).start()
                continue

            leader_port = self.peers.get(current_leader)
            if leader_port and not self.send_message(leader_port, "PING"):
                print(f"[Node {self.node_id}] Leader (Node {current_leader}) tidak merespons! Memicu election")
                with self.lock:
                    if self.leader_id == current_leader:
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
