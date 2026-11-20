"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm (bagian # TODO) sudah dilengkapi di bawah.

Contoh menjalankan (5 terminal terpisah):
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0      # detik menunggu balasan OK sebelum menyatakan diri leader
COORDINATOR_TIMEOUT = 6.0   # detik menunggu COORDINATOR setelah menerima OK


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()

        # state tambahan untuk Bully
        self.got_ok = threading.Event()           # diset saat menerima "OK"
        self.got_coordinator = threading.Event()  # diset saat menerima "COORDINATOR"
        self.electing = False                     # True selama election lokal berjalan

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
        if msg_type == "ELECTION":
            print(f"[Node {self.node_id}] Terima ELECTION dari node {sender_id}")
            if self.node_id > sender_id:
                # kita lebih besar -> "membully": balas OK, lalu ikut mencalonkan diri
                print(f"[Node {self.node_id}] ID saya lebih besar dari {sender_id}, kirim OK")
                self.send_message(self.peers[sender_id], "OK")
                threading.Thread(target=self.start_election, daemon=True).start()

        elif msg_type == "OK":
            print(f"[Node {self.node_id}] Terima OK dari node {sender_id} -> ada node lebih tinggi yang hidup")
            self.got_ok.set()

        elif msg_type == "COORDINATOR":
            with self.lock:
                self.leader_id = sender_id
            print(f"[Node {self.node_id}] Terima COORDINATOR: leader sekarang = node {sender_id}")
            self.got_coordinator.set()

        elif msg_type == "PING":
            pass  # cukup berhasil connect = tanda hidup

    def start_election(self):
        """Dipanggil saat node ini mendeteksi leader tidak ada / tidak merespons."""
        # jangan jalankan dua election sekaligus di node yang sama
        with self.lock:
            if self.electing:
                return
            self.electing = True

        try:
            while True:
                self.got_ok.clear()
                self.got_coordinator.clear()

                higher_peers = {pid: p for pid, p in self.peers.items() if pid > self.node_id}
                print(f"[Node {self.node_id}] Mulai election ke peer lebih tinggi: {sorted(higher_peers)}")
                for pid, port in higher_peers.items():
                    self.send_message(port, "ELECTION")

                # tunggu OK selama ELECTION_TIMEOUT
                if not self.got_ok.wait(ELECTION_TIMEOUT):
                    print(f"[Node {self.node_id}] Tidak ada OK dalam {ELECTION_TIMEOUT}s")
                    self.declare_leader()
                    return

                # ada node lebih tinggi -> berhenti mencalonkan diri, tunggu COORDINATOR
                print(f"[Node {self.node_id}] Berhenti mencalonkan diri, menunggu COORDINATOR...")
                if self.got_coordinator.wait(COORDINATOR_TIMEOUT):
                    return
                print(f"[Node {self.node_id}] COORDINATOR tidak datang, ulangi election")
        finally:
            with self.lock:
                self.electing = False

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua node lain."""
        with self.lock:
            self.leader_id = self.node_id
        print(f"[Node {self.node_id}] *** Saya menjadi LEADER, broadcast COORDINATOR ***")
        for pid, port in self.peers.items():
            ok = self.send_message(port, "COORDINATOR")
            print(f"[Node {self.node_id}]   COORDINATOR -> node {pid}: {'terkirim' if ok else 'gagal (node mati)'}")

    def monitor_leader(self):
        """Loop periodik: cek apakah leader masih hidup, trigger election jika mati."""
        while True:
            time.sleep(3)
            with self.lock:
                leader = self.leader_id
                busy = self.electing
            if busy:
                continue

            if leader is None:
                # belum tahu siapa leader (mis. ketinggalan pesan COORDINATOR)
                print(f"[Node {self.node_id}] Leader belum diketahui, mulai election")
                self.start_election()
            elif leader != self.node_id:
                if not self.send_message(self.peers[leader], "PING"):
                    print(f"[Node {self.node_id}] Leader node {leader} tidak merespons (mati?), mulai election")
                    with self.lock:
                        self.leader_id = None
                    self.start_election()


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