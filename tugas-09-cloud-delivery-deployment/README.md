# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mulai Tugas 11).

## Studi Kasus

Pemerintah ingin membangun **Sistem Data Kependudukan** (nama, NIK, alamat, data biometrik) yang:
- Sangat **rahasia** (data pribadi warga negara, diatur UU Perlindungan Data Pribadi).
- Diakses oleh **ribuan instansi** (dukcapil daerah, kepolisian, bank untuk verifikasi KYC) dengan pola akses yang **tidak rata** (lonjakan saat musim pemilu/pendaftaran sekolah).
- Butuh **skalabilitas** agar tidak downtime saat lonjakan akses, tapi **tidak boleh** datanya berada di infrastruktur yang tidak terkendali penuh oleh negara.

## Tugas Kelompok

1. **Rekomendasikan Deployment Model** (Public / Private / Hybrid / Community Cloud) yang paling tepat untuk sistem ini. Jelaskan alasannya berdasarkan **karakteristik NIST** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dikaitkan dengan kebutuhan kerahasiaan vs skalabilitas.
2. **Rekomendasikan Service Model** (IaaS / PaaS / SaaS) yang tepat untuk komponen-komponen berbeda dari sistem ini (boleh berbeda service model untuk komponen berbeda, mis. database inti vs portal publik untuk pengecekan status).
3. Jelaskan **minimal 2 risiko spesifik** dari pilihan kalian dan mitigasinya (mis. jika Hybrid Cloud dipilih: risiko sinkronisasi data antara private & public segment).
4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).

## Jawaban dari pertanyaan diatas
1. 
Yang paling tepat untuk sistem ini yaitu : **Hybrid**, karena Hybrid itu merupakan kombinasi antara Private Cloud dan Public Cloud yang dimana berdasarkan lima karakteristik utama NIST SP 800-145. Dari segi keamanan, karakteristik resource pooling pada Private Cloud diterapkan secara khusus untuk pemerintah (single-tenant), sehingga data biometrik penduduk tersimpan secara terpisah dan tidak digunakan bersama pihak luar. Sementara itu, resource pooling pada Public Cloud digunakan untuk menangani permintaan akses dari pihak luar.

Untuk mengatasi peningkatan jumlah akses yang tidak menentu, seperti saat pemilu atau pendaftaran sekolah (PPDB), Public Cloud memanfaatkan karakteristik rapid elasticity dimana ini memungkinkan kapasitas server bertambah secara otomatis ketika jumlah pengguna meningkat dan dikurangi kembali ketika kondisi sudah normal. Proses penambahan kapasitas juga didukung oleh on-demand self-service, sehingga tim IT pemerintah dapat menambah sumber daya komputasi secara mandiri dalam waktu singkat tanpa harus menunggu pengadaan server fisik. Namun, pengaturan pada Private Cloud tetap dibatasi dan hanya dapat dilakukan oleh administrator pemerintah.

Selanjutnya, karakteristik broad network access memungkinkan berbagai instansi, seperti Dukcapil daerah, kepolisian, dan perbankan, untuk mengakses sistem melalui standar protokol web atau API tanpa harus terhubung langsung ke jaringan utama Pusat Data Nasional. Seluruh aktivitas akses tersebut juga dapat dipantau melalui measured service. Dengan fitur ini, pemerintah dapat mencatat jumlah penggunaan API oleh setiap instansi secara real-time, mengatur batas akses, serta mengetahui adanya aktivitas permintaan data yang tidak wajar.

Jadi, pada intinya Hybrid itu dapat menjaga keamanan dan kendali data pribadi masyarakat melalui Private Cloud, sekaligus memberikan kemudahan akses, fleksibilitas, dan kemampuan menangani peningkatan jumlah pengguna melalui Public Cloud.

2. 
- Untuk Database Inti Kependudukan & Data Biometrik pakai **Iaas**, kenapa? Karena isinya data paling rahasia (Nama, NIK, Alamat, Data Biometrik) yang dilindungi UU PDP. Dengan IaaS, pemerintah cuma menyewa "mesin" dasarnya saja, tapi urusan sistem operasi, konfigurasi firewall, sampai enkripsi database dipegang penuh oleh tim IT negara. Tidak ada campur tangan pihak luar di lapisan aplikasi maupun sistem operasinya.
- Untuk Portal Publik Cek Status & API Gateway (untuk Bank/Polisi/PPDB) pakai **PaaS**, kenapa? karena bagian ini tidak menyimpan data mentah warga, melainkan hanya bertugas melayani lonjakan trafik saat pemilu atau pendaftaran sekolah. Dengan PaaS, developer pemerintah cukup fokus menulis kode aplikasi dan aturan API-nya saja. Urusan menambah kapasitas server otomatis saat ramai dan update sistem dasar sudah otomatis ditangani oleh platform-nya.
- Untuk Aplikasi Pendukung Operasional (mis. Helpdesk/Ticketing Petugas Dukcapil) pakai **SaaS**, kenapa? Karena Untuk urusan administrasi ringan seperti sistem pelaporan kendala teknis operator Dukcapil kecamatan, pemerintah tidak perlu repot bikin aplikasi dari nol. Tinggal pakai layanan software yang sudah jadi lewat browser (SaaS) yang dimana datanya hanya berupa tiket keluhan teknis, bukan data pribadi kependudukan.

3. 
- Risiko Kebocoran Data NIK dan Biometrik saat Pertukaran Data antara Private Cloud dan Public Cloud
**masalah:** Ketika pihak bank melakukan verifikasi identitas nasabah untuk kebutuhan KYC, permintaan data akan melewati Public Cloud sebelum diteruskan ke database yang berada di Private Cloud. Apabila bagian Public Cloud mengalami serangan atau menyimpan data pada log maupun cache, informasi pribadi penduduk berpotensi bocor.
**solusi:** emerintah perlu menggunakan koneksi privat yang aman, seperti Dedicated VPN atau Direct Connect, dengan perlindungan mutual TLS untuk komunikasi antara kedua cloud. Selain itu, Public Cloud harus menerapkan kebijakan Zero-Data-Retention, yaitu tidak menyimpan data NIK maupun foto biometrik pengguna. Public Cloud hanya bertugas meneruskan permintaan verifikasi dan menerima hasilnya, misalnya berupa jawaban "Cocok" atau "Tidak Cocok".
- Risiko Serangan DDoS dan Pengambilan Data secara Massal melalui API
**masalah:** Penyerang dapat memanfaatkan kondisi ketika jumlah pengguna sedang meningkat, seperti saat pembukaan PPDB, untuk melakukan serangan DDoS atau mengakses API secara berlebihan. Penyerang juga dapat menggunakan akun instansi yang telah dicuri untuk melakukan pengecekan NIK secara massal.
**solusi:** Sistem perlu dilengkapi Web Application Firewall (WAF) dan Rate Limiting untuk membatasi jumlah permintaan berdasarkan sertifikat digital masing-masing instansi. Selain itu, penggunaan Message Queue dapat membantu mengatur antrean permintaan sebelum diteruskan ke Private Cloud. Dengan demikian, jika terjadi serangan pada bagian luar sistem, database utama tetap terlindungi dan risiko gangguan pada keseluruhan layanan dapat dikurangi.

4. 
Kenapa kita tidak memilih public cloud murni sebagai model yang cocok untuk kasus ini karena, data kependudukan terlalu sensitif jika seluruhnya disimpan di cloud milik perusahaan komersial. Data seperti NIK, KK, sidik jari, dan iris mata harus tetap berada di bawah kendali pemerintah agar keamanan dan kerahasiaannya lebih terjaga. Kalau Hybrid Cloud itu menggabungkan Private Cloud untuk menyimpan data utama dan Public Cloud untuk melayani akses dari masyarakat maupun instansi luar.Selain itu, meskipun instansi Dukcapil di daerah (seperti tingkat kabupaten/kota) tidak memiliki infrastruktur Private Cloud atau ruang server sendiri, sistem ini tetap bisa berjalan. Alasannya, Private Cloud milik pemerintah dibangun secara terpusat di Pusat Data Nasional. Dukcapil daerah cukup mengaksesnya sebagai client menggunakan komputer biasa melalui jalur VPN atau intranet pemerintah yang terenkripsi. Jika koneksi internet di daerah sedang tidak stabil, aplikasi di komputer petugas bisa menyimpan data perekaman warga secara sementara dalam bentuk terenkripsi (local encrypted cache), lalu otomatis mengirimnya ke server pusat saat jaringan kembali normal. 

Dari alasan ini mungkin ada pertanyaan lanjutan seperti "kalau gitu kenapa tidak memakai private aja?", kenapa kita tetap pakai hybrid karena private cocok jika penggunanya cuma petugas Dukcapil. Namun karena sistem ini harus melayani jutaan akses eksternal yang meledak secara musiman, negara tetap membutuhkan Public Cloud di lapisan depan agar sistem tidak tumbang dan anggaran tidak boros



## Struktur Submission

```
tugas-09-cloud-delivery-deployment/
├── README.md      # Analisis lengkap (isi dengan poin 1-4 di atas)
├── JURNAL.md
└── bukti/          # (opsional) diagram pendukung
```

## Rubrik Penilaian (Tugas 9)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan rekomendasi deployment model | 30% | Argumen berbasis karakteristik NIST, bukan sekadar "private cloud lebih aman" tanpa detail |
| Ketepatan rekomendasi service model | 25% | Pemetaan komponen sistem ke IaaS/PaaS/SaaS masuk akal |
| Analisis risiko & mitigasi | 25% | Risiko spesifik ke konteks data kependudukan (bukan risiko generik) |
| Perbandingan dengan alternatif yang ditolak | 20% | Argumen penolakan jelas dan berdasar |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum karakteristik NIST/deployment model untuk brainstorming; **tidak boleh** meminta AI menuliskan rekomendasi/analisis akhir yang tinggal ditempel ke `README.md`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Jawaban yang terasa seperti "template" (bisa dipakai untuk sistem cloud apa saja tanpa menyebut spesifik kependudukan/data pribadi/regulasi) akan dinilai rendah pada komponen ketepatan rekomendasi.
- `README.md` wajib membahas minimal satu skenario tandingan yang kalian buat sendiri (mis. "bagaimana jika instansi daerah tidak punya infrastruktur private cloud sendiri?") beserta jawabannya.
