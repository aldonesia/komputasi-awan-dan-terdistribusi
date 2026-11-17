"""
Tugas 4 - Jalur B: Consumer (simulasi modul Kurir/Notifikasi)
Jalankan file ini SEBELUM publisher.py untuk uji normal, atau SESUDAHNYA
untuk membuktikan pesan tetap tersimpan di antrean (asynchronous decoupling).
"""

import pika
import json

QUEUE_NAME = "pembayaran_berhasil"


def callback(ch, method, properties, body):
    pesan = json.loads(body)
    # TODO 1: proses pesan (misalnya cetak "Kurir menerima notifikasi
    # pembayaran untuk {user_id} sejumlah {jumlah}").
    print(
        f"Kurir menerima notifikasi pembayaran untuk "
        f"{pesan['user_id']} sejulah {pesan['jumlah']}"
    )

    # TODO 2: kirim acknowledgement ke RabbitMQ (ch.basic_ack) supaya
    # pesan dihapus dari antrean setelah berhasil diproses.
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # TODO 3: buat koneksi & channel seperti di publisher.py, deklarasikan
    # queue yang SAMA (durable=True), lalu daftarkan `callback` dengan
    # channel.basic_consume(...).
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Queue harus dideklarasikan sama persis dengan publisher (durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Hanya ambil 1 pesan pada satu waktu sampai di-ack (fair dispatch)
    channel.basic_qos(prefetch_count=1)

    # auto_ack=False agar acknowledgement dilakukan manual di callback
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=False,
    )

    print("Menunggu event dari antrean 'pembayaran_berhasil'... (Ctrl+C untuk berhenti)")

    # TODO 4: panggil channel.start_consuming()
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nConsumer dihentikan.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
