"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Kode lengkap dengan perbaikan pada TODO 1, TODO 2, dan TODO 3.
"""

import threading
import random
import time

NUM_ORDERS = 100  # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 100 # jumlah thread pekerja

# Counter untuk menghitung total pesanan yang berhasil diproses.
processed_count = 0

# TODO 1: Membuat objek Lock untuk melindungi `processed_count`.
lock = threading.Lock()

def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasi kerja awal
    time.sleep(random.uniform(0.001, 0.005))

    # TODO 2: Menambahkan increment `processed_count`.

   
    current_value = processed_count     # 1. Membaca nilai saat ini
    time.sleep(0.0001)                  # 2. Jeda mikro yang memicu bentrok antar thread
    processed_count = current_value + 1 # 3. Menulis kembali nilai baru (rawan tertimpa)

def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)

def main() -> None:
    global processed_count
    processed_count = 0  # Reset counter
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: Bagi `order_ids` menjadi NUM_WORKERS bagian, buat dan start thread.
    threads = []
    chunk_size = len(order_ids) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start_idx = i * chunk_size
        # Memastikan sisa pembagian masuk ke worker terakhir
        end_idx = (i + 1) * chunk_size if i < NUM_WORKERS - 1 else len(order_ids)
        chunk = order_ids[start_idx:end_idx]

        # Membuat thread baru
        t = threading.Thread(target=worker, args=(chunk,))
        # Memasukkan ke dalam list threads
        threads.append(t)
        # Menjalankan thread
        t.start()

    # Menunggu seluruh thread selesai bekerja
    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count}")
    if processed_count != NUM_ORDERS:
        print(f"RACE CONDITION TERDETEKSI - nilai counter meleset karena akses bersamaan tanpa Lock! (seharusnya : {NUM_ORDERS})" )
    else:
        print("HASIL AKURAT - Sinkronisasi Lock berhasil!")

if __name__ == "__main__":
    main()