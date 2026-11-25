"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan memakai socket server/client.
Logika Bully Algorithm dilengkapi pada bagian TODO.

Jalankan 5 node pada 5 terminal terpisah.
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0  # detik menunggu balasan OK


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port

        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()

        # Mencegah dua election berjalan bersamaan di node yang sama.
        self.election_in_progress = False

        # Penanda bahwa pesan OK atau COORDINATOR sudah diterima.
        self.ok_received = threading.Event()
        self.coordinator_received = threading.Event()

    def log(self, message: str):
        waktu = time.strftime("%H:%M:%S")
        print(
            f"[{waktu}] [Node {self.node_id}] {message}",
            flush=True,
        )

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
        """Dipanggil setiap kali node menerima pesan dari node lain."""

        # Abaikan pengirim yang tidak tercantum dalam daftar peer.
        if sender_id not in self.peers:
            return

        # PING menggunakan keberhasilan koneksi TCP sebagai tanda hidup.
        if msg_type == "PING":
            return

        self.log(f"TERIMA {msg_type} dari node {sender_id}")

        # TODO 1: menangani ELECTION, OK, dan COORDINATOR.
        if msg_type == "ELECTION":
            if self.node_id > sender_id:
                self.send_message(self.peers[sender_id], "OK")
                self.log(f"KIRIM OK ke node {sender_id}")

                # Node dengan ID lebih tinggi ikut melakukan election.
                self.start_election()

        elif msg_type == "OK":
            if sender_id > self.node_id:
                with self.lock:
                    if self.election_in_progress:
                        self.ok_received.set()

        elif msg_type == "COORDINATOR":
            if sender_id < self.node_id:
                # Jika kita masih hidup dan ID lebih tinggi,
                # kita ikut mencalonkan diri.
                self.log(
                    f"Node {sender_id} ber-ID lebih rendah; "
                    "mulai election."
                )
                self.start_election()
            else:
                with self.lock:
                    self.leader_id = sender_id
                    self.coordinator_received.set()

                self.log(f"LEADER SAAT INI: node {sender_id}")

    def start_election(self):
        """Memulai pemilihan ketika leader tidak ada atau tidak merespons."""

        with self.lock:
            if self.election_in_progress:
                return

            self.election_in_progress = True
            self.leader_id = None
            self.ok_received.clear()
            self.coordinator_received.clear()

        # TODO 2: kirim ELECTION ke semua node dengan ID lebih tinggi.
        higher_peers = {
            pid: port
            for pid, port in self.peers.items()
            if pid > self.node_id
        }

        self.log(
            f"MULAI ELECTION; kandidat lebih tinggi: "
            f"{sorted(higher_peers)}"
        )

        try:
            for peer_id, peer_port in higher_peers.items():
                sent = self.send_message(peer_port, "ELECTION")
                status = "terkirim" if sent else "tidak terhubung"
                self.log(f"KIRIM ELECTION ke node {peer_id}: {status}")

            # Tunggu OK atau pengumuman leader.
            deadline = time.monotonic() + ELECTION_TIMEOUT

            while time.monotonic() < deadline:
                if self.coordinator_received.is_set():
                    return

                if self.ok_received.is_set():
                    break

                self.coordinator_received.wait(0.05)

            if self.coordinator_received.is_set():
                return

            if self.ok_received.is_set():
                self.log(
                    "Ada OK dari node lebih tinggi; "
                    "menunggu COORDINATOR."
                )

                # Batasi waktu tunggu agar tidak menunggu selamanya
                # apabila pengirim OK mati sebelum mengumumkan leader.
                coordinator_timeout = (
                    ELECTION_TIMEOUT * (len(self.peers) + 1)
                )

                received = self.coordinator_received.wait(
                    coordinator_timeout
                )

                if not received:
                    self.log(
                        "COORDINATOR belum datang; monitor akan "
                        "mencoba election lagi."
                    )
            else:
                self.declare_leader()

        finally:
            with self.lock:
                self.election_in_progress = False

    def declare_leader(self):
        """Menyatakan diri sebagai leader dan memberi tahu semua peer."""

        # TODO 3: simpan diri sendiri sebagai leader.
        with self.lock:
            # Periksa ulang jika balasan tiba tepat saat timeout.
            if self.ok_received.is_set() or self.leader_id is not None:
                return

            self.leader_id = self.node_id
            self.coordinator_received.set()

        self.log(
            f"TERPILIH LEADER: node {self.node_id}; "
            "broadcast COORDINATOR."
        )

        # Kirim pengumuman ke SEMUA peer.
        for peer_id, peer_port in self.peers.items():
            sent = self.send_message(peer_port, "COORDINATOR")
            status = "terkirim" if sent else "tidak terhubung"
            self.log(
                f"KIRIM COORDINATOR ke node {peer_id}: {status}"
            )

    def monitor_leader(self):
        """Memeriksa leader secara berkala dan memulai election jika mati."""

        while True:
            time.sleep(3)

            # TODO 4: periksa kondisi leader.
            with self.lock:
                leader_id = self.leader_id
                busy = self.election_in_progress

            if busy:
                continue

            if leader_id is None:
                self.log("Belum ada leader; mencoba election.")
                self.start_election()

            elif leader_id != self.node_id:
                alive = self.send_message(
                    self.peers[leader_id],
                    "PING",
                )

                if not alive:
                    with self.lock:
                        # Abaikan hasil pemeriksaan lama apabila
                        # leader sudah berubah atau election dimulai.
                        if (
                            self.leader_id != leader_id
                            or self.election_in_progress
                        ):
                            continue

                        self.leader_id = None

                    self.log(
                        f"LEADER node {leader_id} TIDAK MERESPONS; "
                        "mulai pemilihan ulang."
                    )
                    self.start_election()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument(
        "--peers",
        type=str,
        required=True,
        help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005",
    )
    args = parser.parse_args()

    # Konvensi port: node N memakai port 5000 + N.
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(
        target=node.start_server,
        daemon=True,
    ).start()

    threading.Thread(
        target=node.monitor_leader,
        daemon=True,
    ).start()

    time.sleep(1)
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProses node dihentikan.", flush=True)