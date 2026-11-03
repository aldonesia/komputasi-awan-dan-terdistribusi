# Tugas 4 - Implementasi RPC dan Message Queue (Komputasi Awan)

Repositori ini berisi implementasi Tugas 4 mata kuliah Komputasi Awan dan Terdistribusi. Proyek ini mendemonstrasikan dua pola komunikasi antar-layanan (mikroservis):
1. **Jalur A (RPC):** Komunikasi sinkron menggunakan `xmlrpc` standar dari Python.
2. **Jalur B (Message Queue):** Komunikasi asinkron (*decoupling*) menggunakan **RabbitMQ** dan *library* `pika`.

## 👥 Anggota Kelompok 9

| Nama | NIM | Kontribusi |
| :--- | :--- | :--- |
| Naufal Fudhail | 103072400013 | Implementasi RPC Server & Client, Error Handling, Jurnal |
| Diandra Nanditya Mulkis | 103072400075 | Setup Message Queue, Logika Publisher, dan Consumer |
| Samuel Nelson Wabiser | 103072400111 | Dockerisasi RabbitMQ, Pengujian Asinkron, Dokumentasi |

*(Catatan: Kolom kontribusi disesuaikan dengan konteks pengerjaan Tugas 4, silakan sesuaikan kembali jika ada pembagian kerja yang spesifik di tim kalian).*

---

## 📁 Struktur Repositori

```text
tugas-04-rpc-message-queue/
│
├── rpc/                     # Jalur A: Implementasi RPC
│   ├── server.py            # Simulasi modul Pembayaran (Server)
│   └── client.py            # Simulasi modul Pesanan (Client)
│
├── mq/                      # Jalur B: Implementasi Message Queue
│   ├── docker-compose.yml   # Konfigurasi container RabbitMQ
│   ├── requirements.txt     # Dependency Python (pika)
│   ├── consumer.py          # Simulasi modul Kurir (Consumer)
│   └── publisher.py         # Simulasi modul Pembayaran (Publisher)
│
├── bukti/                   # Folder screenshot bukti pengujian
├── JURNAL.md                # Laporan jurnal proses dan kendala
└── README.md                # Dokumentasi utama (file ini)
