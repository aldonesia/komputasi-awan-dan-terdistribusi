import pika
import json
import time

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"\n[CONSUMER] Menerima tugas pengiriman untuk Order: {data['order_id']}")
    print(f"-> Item: {data['item']} | User: {data['user_id']}")
    print("-> Mengirim instruksi ke aplikasi Kurir...")
    
    # Simulasi proses kerja kurir
    time.sleep(2)
    print(f"[CONSUMER] Selesai memproses Order {data['order_id']}!")
    
    # Beritahu RabbitMQ bahwa pesan telah sukses diproses
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='notifikasi_kurir', durable=True)
    
    # Batasi agar consumer hanya mengambil 1 pesan dalam satu waktu (fair dispatch)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='notifikasi_kurir', on_message_callback=callback)
    
    print("[CONSUMER] Modul Kurir siap mendengarkan event dari antrean. Tekan CTRL+C untuk keluar.\n")
    channel.start_consuming()

if __name__ == "__main__":
    main()