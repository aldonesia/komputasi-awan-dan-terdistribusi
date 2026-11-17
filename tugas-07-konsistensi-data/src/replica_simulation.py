import time
import threading

class ReplicaServer:
    def __init__(self, name):
        self.name = name
        self.saldo = 0
        self.version = 0

class EWalletSystem:
    def __init__(self):
        self.jakarta = ReplicaServer("Jakarta")
        self.bandung = ReplicaServer("Bandung")
        self.lock = threading.Lock()

    def top_up_jakarta(self, amount):
        """Top-up dilakukan di server Jakarta"""
        with self.lock:
            self.jakarta.saldo += amount
            self.jakarta.version += 1
            print(f"[WRITE] Top-up Rp{amount} di Server Jakarta. Saldo: {self.jakarta.saldo} (Versi: {self.jakarta.version})")
        
        # Mensimulasikan delay replikasi latar belakang ke Bandung
        threading.Thread(target=self._background_replication, args=(self.jakarta.saldo, self.jakarta.version)).start()

    def _background_replication(self, saldo_val, version_val):
        time.sleep(2) # Simulasi delay jaringan lambat (2 detik)
        with self.lock:
            if version_val > self.bandung.version:
                self.bandung.saldo = saldo_val
                self.bandung.version = version_val
                print(f"[REPLICATION] Server Bandung tersinkronisasi. Saldo: {self.bandung.saldo} (Versi: {self.bandung.version})")

    def read_without_consistency(self, server_obj, client_expected_version=None):
        """TODO 1: Simulasi inconsistent read (bisa membaca data lama jika replikasi belum selesai)"""
        print(f"[READ] Membaca saldo dari Server {server_obj.name} -> Saldo: {server_obj.saldo} (Versi: {server_obj.version})")
        return server_obj.saldo

    def read_with_read_your_writes(self, server_obj, client_version):
        """TODO 2: Mekanisme Read-Your-Writes sederhana berbasis version checking"""
        with self.lock:
            if server_obj.version < client_version:
                print(f"[SYNC-FIX] Server {server_obj.name} mendeteksi data kedaluwarsa (Lokal v{server_obj.version} < Klien v{client_version}). Melakukan sinkronisasi paksa...")
                # Paksa ambil data terbaru dari Jakarta (asumsi master/primary terdepan)
                server_obj.saldo = self.jakarta.saldo
                server_obj.version = self.jakarta.version
            
            print(f"[READ-SAFE] Server {server_obj.name} menyajikan saldo konsisten -> Saldo: {server_obj.saldo} (Versi: {server_obj.version})")
        return server_obj.saldo

if __name__ == "__main__":
    system = EWalletSystem()

    print("--- SKENARIO 1: INCONSISTENT READ (BUG) ---")
    system.top_up_jakarta(50000)
    # Langsung dibaca di Bandung sebelum replikasi selesai (delay 2 detik)
    system.read_without_consistency(system.bandung)
    
    time.sleep(3) # Tunggu replikasi selesai sepenuhnya

    print("\n--- SKENARIO 2: READ-YOUR-WRITES CONSISTENCY (SOLUSI) ---")
    system.top_up_jakarta(100000)
    # Klien membawa version token terbaru (misal: Versi 2) langsung membaca di Bandung
    system.read_with_read_your_writes(system.bandung, client_version=2)