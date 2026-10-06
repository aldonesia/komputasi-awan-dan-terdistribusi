"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time

NUM_ORDERS = 100        # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 10        # jumlah thread pekerja

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
# Sengaja rawan race condition jika diakses tanpa proteksi.
processed_count = 0

# TODO 1: Buat objek Lock di sini untuk melindungi `processed_count`.
lock = threading.Lock()

# Diubah oleh main hanya ketika seluruh thread percobaan sebelumnya selesai.
use_lock = False


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan kerja nyata (mis. validasi, hitung total harga)
    time.sleep(random.uniform(0.001, 0.01))

    # TODO 2: Tambahkan increment `processed_count` DI SINI.
    # Langkah 1: jalankan dulu tanpa lock (increment biasa: processed_count += 1)
    #            dan buktikan hasil akhirnya sering salah (< NUM_ORDERS).
    # Langkah 2: bungkus increment dengan `with lock:` dan buktikan hasilnya
    #            selalu tepat NUM_ORDERS. Simpan bukti kedua kondisi ini
    #            di JURNAL.md / folder bukti/.
    if use_lock:
        with lock:
            current_count = processed_count
            time.sleep(0.001)
            processed_count = current_count + 1
    else:
        # Sengaja pisahkan baca dan tulis agar lost update dapat terlihat.
        # Jeda di antara keduanya memberi kesempatan thread lain membaca
        # nilai yang sama. Jeda I/O di atas saja tidak membuat celah ini.
        current_count = processed_count
        time.sleep(0.001)
        processed_count = current_count + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    global processed_count, use_lock
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: Bagi `order_ids` menjadi NUM_WORKERS bagian, buat satu
    # threading.Thread per bagian yang menjalankan `worker(...)`,
    # start semua thread, lalu join semua thread sebelum lanjut.
    for mode in (False, True):
        use_lock = mode
        processed_count = 0
        threads = []

        print(f"\n=== {'DENGAN LOCK' if use_lock else 'TANPA LOCK'} ===")
        print(f"Jumlah pesanan: {NUM_ORDERS}; jumlah worker: {NUM_WORKERS}")

        for worker_index in range(NUM_WORKERS):
            # Round-robin: worker 0 mendapat ID 1, 11, 21, ..., 91.
            assigned_orders = order_ids[worker_index::NUM_WORKERS]
            thread = threading.Thread(target=worker, args=(assigned_orders,))
            threads.append(thread)

        # Start semua worker sebelum join, bukan start-join satu per satu.
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
        print(f"Update counter yang hilang: {NUM_ORDERS - processed_count}")
        if processed_count != NUM_ORDERS:
            print("RACE CONDITION TERDETEKSI - counter tidak sesuai!")
        else:
            print("Counter sesuai jumlah pesanan.")


if __name__ == "__main__":
    main()
