# Jurnal Proses — Tugas 9

## Diskusi deployment model
- **Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu:**
  1. **Public Cloud murni:** Sempat dipertimbangkan karena unggul pada karakteristik *rapid elasticity*, *on-demand self-service*, dan efisiensi biaya (*measured service*) untuk menangani lonjakan trafik ekstrem seperti saat pemilu atau pendaftaran serentak. Namun opsi ini ditolak karena sifat *resource pooling* yang *multi-tenant* membuat negara tidak memiliki kendali penuh atas infrastruktur fisik, sehingga melanggar prinsip kedaulatan data dan berisiko tinggi terhadap kepatuhan UU Perlindungan Data Pribadi (UU PDP) untuk data sensitif seperti NIK dan biometrik.
  2. **Private Cloud murni:** Menjamin isolasi dan kontrol penuh negara atas data kependudukan, tetapi kurang efisien dan sulit berskala cepat (*rapid elasticity*) jika harus menampung lonjakan akses portal publik secara tiba-tiba tanpa menyediakan kapasitas cadangan yang mahal (*over-provisioning*).
  3. **Keputusan Akhir adalah Hybrid Cloud:** Dipilih sebagai titik tengah terbaik antara kerahasiaan data dan skalabilitas. Data kependudukan inti (NIK, alamat, biometrik) ditempatkan di segmen *private cloud* milik negara sebagai *single source of truth*, sementara portal layanan publik yang bersifat *stateless* (tanpa penyimpanan data inti permanen) dijalankan di *public cloud* agar elastis menghadapi lonjakan trafik. Komunikasi antarsegmen dibatasi ketat melalui API Gateway di zona DMZ dengan enkripsi *mutual TLS*, serta mendukung instansi daerah melalui konsep *resource pooling* terpusat tanpa penyimpanan data lokal di daerah.

## Diskusi service model per komponen
- **IaaS (Infrastructure as a Service) untuk Database Inti (NIK, Alamat, Biometrik):** Dijalankan di atas *private cloud* negara agar tim IT pemerintah memegang kendali penuh mulai dari level sistem operasi, konfigurasi jaringan, *firewall*, hingga enkripsi penyimpanan demi memenuhi standar keamanan UU PDP tanpa ketergantungan pada pihak eksternal.
- **PaaS (Platform as a Service) untuk API Gateway KYC, Aplikasi Instansi, dan Portal Publik:** Digunakan untuk layanan verifikasi identitas (bank/kepolisian), web operasional instansi (Dukcapil daerah), serta portal cek status publik. Dengan PaaS, tim pengembang pemerintah dapat berfokus penuh pada keamanan logika aplikasi dan otorisasi akses, sementara manajemen *runtime* dan penskalaan otomatis (*auto-scaling*) saat beban memuncak ditangani langsung oleh platform.
- **SaaS (Software as a Service) tidak digunakan:** Ditolak karena sistem data kependudukan nasional membutuhkan kustomisasi alur otorisasi tingkat tinggi dan tata kelola data yang tidak boleh bergantung pada aplikasi jadi milik vendor pihak ketiga.

## Bukti Pertemuan & Diskusi Kelompok
Diskusi pembagian arsitektur sistem, pemetaan 5 karakteristik NIST, analisis risiko *hybrid cloud*, serta penyusunan skenario tandingan dilakukan bersama rekan kelompok:

![Bukti Pertemuan](bukti/pertemuan.png)

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 24/11/2026 | Gemini | "Bantu susun kerangka rangkuman diskusi teknis untuk jurnal proses mengenai pemilihan Hybrid Cloud serta pembagian IaaS dan PaaS pada sistem data kependudukan berbasis 5 karakteristik NIST." | Memberikan struktur perbandingan antara kerahasiaan data (UU PDP) dan skalabilitas trafik publik untuk merangkum alasan pemilihan arsitektur *Hybrid Cloud* dan pemisahan komponen *service model*. | Menyusun ulang poin-poin perbandingan opsi *deployment* dan pemetaan *service model* ke dalam catatan proses diskusi kelompok di `JURNAL.md` agar mirip dengan keputusan teknis pada `README.md`. |
| 24-11-2026 | Gemini | Bertanya  untuk menjelaskan perbedaan On-Demand Self-Service vs Rapid Elasticity, alasan Resource Pooling menjaga kerahasiaan dan konsep komponen stateless dan yang bukan stateless | AI menjelaskan bahwa self-service berarti mengatur mandiri tanpa perantara provider, rapid elasticity adalah auto-scaling saat trafik melonjak, resource pooling di private cloud mengisolasi server negara, dan stateless hanya memproses request tanpa menyimpan data permanen. | Dapat menulis dengan lebih yakin untuk bagian karakteristik NIST dengan case ini |
| |||||
||||||
