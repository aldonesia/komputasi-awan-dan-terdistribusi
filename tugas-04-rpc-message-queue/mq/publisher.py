import pika
import json
import datetime

def main():
    # Koneksi ke RabbitMQ lokal
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Deklarasikan antrean (queue) yang tahan lama (durable)
    channel.queue_declare(queue='notifikasi_kurir', durable=True)
    
    payload = {
        "order_id": "ORD-998877",
        "user_id": "user_123",
        "item": "Nasi Goreng Spesial",
        "status": "pembayaran_berhasil",
        "timestamp": str(datetime.datetime.now())
    }
    
    message = json.dumps(payload)
    
    # Kirim pesan ke antrean tanpa menunggu consumer aktif
    channel.basic_publish(
        exchange='',
        routing_key='notifikasi_kurir',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2, # Membuat pesan persistent (tersimpan walau broker restart)
        )
    )
    
    print(f"[PUBLISHER] Event pembayaran berhasil dikirim ke antrean: {message}")
    connection.close()

if __name__ == "__main__":
    main()