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


## Analisis Kami
#### 1. Rekomendasikan Deployment Model
Disini kami memilih Hybrid cloud sebagai deployment model untuk Sistem Data Kependudukan karena dari case yang diberikan dan penjelasannya itu perlu kombinasi antara kerahasiaan data negara, aksesibilitas oleh ribuan instansi dibawahnya dan skalabilitas saat ada lonjakan traffic misal saat ada pemilu atau hal lain. Dengan model deployment hybrid komponen yang paling rahasia/sensitif (Data pribadi rakyat) seperti NIK,  alamat dan data biometrik yang dilindungi UU Perlindungan Data Pribadi akan berada di bagian private cloud dibawah pengawasan negara secara langsung,sedangkan ribuan instansi dibawahnya yang perlu akses ke data pribadi seperti dukcapil, kepolisian dan lain-lain tetap bisa akses melalui jalur yang aman dan khusus tanpa harus menyentuh langsung ke database intinya. Sementara itu, public cloud digunakan secara terbatas pada portal layanan publik (yang tidak menyimpan data inti secara permanen) agar mampu menampung lonjakan akses ekstrem tanpa membebani infrastruktur inti negara.

Berikut alasan berdasarkan karakteristik NIST:

**a. On-Demand Self Service:** Saat trafik tinggi (ada pemilu atau pembukaan bank baru dll), tim IT negara bisa langsung menambahkan node ke bagian yang perlu tambahan sumber daya (tanpa harus nunggu upgrade server fisiknya). Agar kerahasiaannya tetap terjaga hanya orang / administrator pemerintah yang boleh mengubah-ubah alokasi sumber dayanya.
<br>
**b. Broad Network Access:** Ribuan instansi itu tersebar dibanyak wilayah indonesia dan banyak jenisnya, semua instansi ini bisa akses ke server jaringan pemerintahan yang harus melalui jaringan terenkripsi sehingga data warga negara itu tetap aman dan tidak terekspos ke publik .
<br>
**c. Resource Pooling:** Sumber daya server itu terpusat daripada setiap instansi punya servernya sendiri, kemudian agar bisa dibagi secara dinamis ke instansi yang sedang tinggi trafiknya dan ini lebih aman karena yang perlu diamankan itu tidak banyak hanya server pusat yang terisolasi dari publik (jadi tidak perlu jaga server dari ribuan instansi).
<br>
**d. Rapid Elasticity:** Saat beban suatu instansi membesar untuuk akses ke komponen khusus misal data orang yang melakukan pemilu sistem dapat melakukan penyesuaian otomatis pada komponen yang tinggi trafiknya (khusus yang bukan database inti agar kerahasiaan tetap terjaga) sehingga server tidak mengalami downtime atau mati dan kembalikan ke penggunaan normal saat kondisi mereda.
<br>
**e. Measured Service:** Setiap pemakaian sumber daya saat  trafik meningkat dan jumlah permintaan verifikasi API oleh masing-masing instansi maupun bank dicatat otomatis secara terukur untuk pengaturan kuota dan efisiensi biaya. Pencatatan  akses secara rinci tersebut sekaligus berfungsi sebagai jejak audit sesuai ketentuan UU PDP guna memantau pihak mana yang mengakses data kependudukan serta mendeteksi anomali atau potensi kebocoran data secara cepat.

#### 2. Rekomendasikan Service Model
Karena dipenjelasan case awal Sistem Data Kependudukan ini harus punya kerahasiaan yang tinggu dan kebutuhan skalabilitasnya beda kami tidak memakai 1 service model saja, oleh karena itu kami berpikir untuk menggunakan 2 model yaotu IaaS dan PaaS yaitu:

**a. IaaS (Infrastructure as a Service)** Untuk Komponen Rahasia (Database Inti NIK & Biometrik): Untuk menyimpan data yang sensitif seperti NIK, alamat, dan data biometrik warga negara, kami memilih IaaS di atas private cloud milik negara. Dengan IaaS, tim IT negara memegang kendali penuh mulai dari sistem operasi, konfigurasi jaringan, firewall, hingga enkripsi penyimpanannya agar tetap patuh pada UU Perlindungan Data Pribadi tanpa campur tangan pihak luar.

**b. PaaS (Platform as a Service)** Untuk Aplikasi Layanan Instansi, API, Verifikasi KYC, dan Portal Publik: Untuk lapisan aplikasi dan gerbang layanan seperti API Gateway verifikasi KYC bagi bank dan kepolisian, web operasional untuk banyak intansi seperti Dukcapil daerah, serta portal publik pengecekan status saat musim pemilu atau pendaftaran SIM dan lian-lain kami memilih PaaS. Dengan PaaS, tim pengembang pemerintah bisa fokus mengembangkan dan mengamankan aplikasinya sendiri, sementara urusan runtime dan penyesuaian kapasitas otomatis saat trafik melonjak ditangani oleh platform tanpa harus mengatur ulang sumber daya.

#### 3. Jelaskan minimal 2 risiko spesifik
**Risiko 1: Kebocoran data pribadi lewat jalur antara private dan public segment**

Portal publik berjalan di *public cloud* (PaaS), sedangkan data inti ada di *private cloud* (IaaS). Karena itu ada jalur komunikasi antara keduanya, dan jalur itu bisa menjadi titik masuk serangan. Contohnya *SQL injection* atau API *abuse* lewat portal publik yang menembus sampai ke *database* NIK dan biometrik. Data biometrik tidak bisa diganti seperti password. Jika bocor, dampaknya permanen bagi warga, dan pemerintah bisa dianggap lalai menurut UU PDP.

**Mitigasi:**
Portal publik tidak boleh *query* langsung ke *database* inti. Semua permintaan lewat API *Gateway* di zona perantara (DMZ), dengan hak akses minimum dan hanya mengembalikan data terbatas (misalnya status "terverifikasi" atau "belum").
Seluruh jalur antar-segment memakai koneksi privat terenkripsi (VPN *site-to-site* atau *private link*) dengan mutual TLS, bukan internet publik.
Data yang diproses di *public cloud* bersifat *stateless*, tidak disimpan permanen, dan data sensitif ditokenisasi atau di-*masking*.
Pasang WAF dan rate limiting di gerbang publik, serta audit log dari *Measured Service* dipantau untuk mendeteksi anomali akses.

**Risiko 2: Inkonsistensi dan keterlambatan sinkronisasi data antar-segment**

Pada *Hybrid Cloud*, sebagian data (*cache*, status layanan, hasil verifikasi) berada di dua tempat. Saat lonjakan akses seperti pemilu, atau saat koneksi ke *private cloud* terganggu, data di portal publik bisa berbeda dari data inti. Akibatnya, warga bisa melihat status kependudukan yang salah. Bank bisa gagal atau salah melakukan KYC karena data lama. Perbedaan data kependudukan juga bisa menimbulkan masalah hukum dan administrasi, misalnya hak pilih.

**Mitigasi:**
*Database* inti di *private cloud* ditetapkan sebagai *single source of truth*. Data di *public cloud* hanya *cache read-only* dengan masa berlaku (TTL) pendek.
Perubahan data disinkronkan melalui antrean pesan (*message queue*) dengan mekanisme *retry* dan *idempotency*, sehingga tidak ada data hilang atau ganda saat koneksi putus.
Untuk verifikasi kritis seperti KYC bank, selalu validasi langsung ke data inti lewat API *Gateway*.
Siapkan monitoring selisih data dan prosedur rekonsiliasi berkala.

#### 4. Bandingkan singkat dengan satu alternatif yang kalian tolak 
**Alternatif yang ditolak: Public Cloud murni**

*Public Cloud* unggul di tiga karakteristik NIST, yaitu *rapid elasticity, on-demand self-service*, dan *measured service* yang efisien biaya. Lonjakan akses saat pemilu atau pendaftaran sekolah sebenarnya paling mudah ditangani di sini. Namun kami menolaknya karena tiga alasan, antara lain:
1. Bertentangan dengan syarat studi kasus. Kasus menyebut data tidak boleh berada di infrastruktur yang tidak terkendali penuh oleh negara. Di *Public Cloud*, *resource pooling* berarti sumber daya fisik dipakai bersama banyak pelanggan (*multi-tenant*) dan dikelola penyedia. Negara tidak punya kendali penuh atas *server* fisik, jaringan, maupun siapa yang memiliki akses administratif di level infrastruktur.
2. Risiko hukum dan kedaulatan data. NIK, alamat, dan biometrik adalah data pribadi sensitif dalam UU PDP. Menyimpannya di infrastruktur pihak ketiga, apalagi yang bisa tunduk pada hukum negara lain, meningkatkan risiko akses oleh pihak yang tidak berwenang dan menyulitkan penegakan tanggung jawab jika terjadi kebocoran.
3. Dampak kebocoran terlalu besar. Jika data seluruh penduduk berada di lingkungan *multi-tenant*, satu celah isolasi antar-*tenant* cukup untuk membuka data nasional sekaligus. Data biometrik yang bocor juga tidak bisa "diganti".

Karena itu, *Hybrid Cloud* dipilih sebagai jalan tengah. Data rahasia tetap di *private cloud*, dan sifat elastis *Public Cloud* dipakai hanya untuk komponen yang tidak menyimpan data inti.

#### Skenario Tandingan 
Bagaimana jika instansi daerah tidak punya infrastruktur *private cloud* sendiri?

Jawaban: Instansi daerah tidak perlu membangun *private cloud* sendiri. Sesuai prinsip *resource pooling, private cloud* dibangun terpusat oleh pemerintah pusat (misalnya di pusat data nasional) dan dipakai bersama seluruh instansi lewat jaringan pemerintah yang terenkripsi (*broad network access*). Instansi daerah cukup memakai aplikasi *web* operasional dan API yang tersedia sebagai PaaS, dengan akses terbatas sesuai peran (*role-based access control*) dan autentikasi berlapis. Data tidak disimpan di perangkat atau server daerah, sehingga risiko kebocoran di tingkat daerah yang keamanannya lebih lemah ikut berkurang. Konsekuensinya, jaringan daerah menjadi titik kritis sehingga perlu koneksi cadangan dan prosedur akses darurat saat jaringan terganggu.

