# Aplikasi Deteksi Stunting dengan Chatbot

## Deskripsi Singkat

Aplikasi ini adalah sistem pakar inovatif yang menggabungkan teknologi chatbot dengan metode Certainty Factor (CF) untuk mendeteksi dan menilai risiko stunting pada anak. Sistem bekerja dengan cara:

1. **Pengumpulan Data**: Pengguna memasukkan data dasar anak (tinggi, berat, usia, jenis kelamin)
2. **Penilaian Interaktif**: Chatbot melakukan wawancara terstruktur tentang kondisi anak
3. **Analisis Pakar**: Sistem memproses data menggunakan algoritma Certainty Factor dengan aturan yang ditentukan pakar
4. **Hasil**: Memberikan penilaian risiko stunting dengan tingkat kepercayaan dan rekomendasi

Fitur Utama:
- Autentikasi pengguna yang aman melalui WhatsApp OTP
- Percakapan chatbot dinamis berdasarkan respon pengguna
- Perhitungan risiko stunting secara real-time
- Rekomendasi berbasis bukti
- Pelacakan riwayat yang komprehensif

Pengguna Target:
- Orang Tua/Wali
- Petugas Kesehatan
- Spesialis Perkembangan Anak
- Petugas Kesehatan Masyarakat

# Aplikasi Deteksi Stunting dengan Chatbot

Aplikasi sistem pakar berbasis web yang mengimplementasikan mekanisme Certainty Factor untuk mendeteksi stunting pada anak melalui antarmuka chatbot interaktif.

## Gambaran Proyek

Aplikasi ini dikembangkan sebagai bagian dari penelitian berjudul:
"Inovasi Aplikasi Deteksi Stunting Menggunakan Chatbot Sebagai Strategi Mencapai Universal Health Coverage dalam SDGs"

## Fitur

- Autentikasi pengguna dengan verifikasi WhatsApp OTP
- Antarmuka chatbot interaktif untuk pengumpulan data
- Implementasi sistem pakar menggunakan Certainty Factor
- Analisis pengukuran fisik (tinggi, berat)
- Penilaian perilaku dan perkembangan
- Pelacakan riwayat detail
- Evaluasi risiko stunting komprehensif
- Rekomendasi profesional berdasarkan hasil

## Persyaratan Teknis

- Python 3.8 atau lebih tinggi
- MongoDB 4.4 atau lebih tinggi
- Framework web Flask
- Paket Python tambahan (lihat requirements.txt)

## Instalasi

1. Clone repositori
2. Install dependensi:
```bash
pip install -r requirements.txt
```

## Konfigurasi

### 1. Pengaturan MongoDB
1. Install MongoDB di sistem Anda
2. Buat database baru
3. Perbarui string koneksi MongoDB di `config.py`:
```python
self.MONGDB_URI = "mongodb://username:password@host:port/database"
```

### 2. Konfigurasi WhatsApp OTP
1. Siapkan layanan WhatsApp OTP
2. Perbarui alamat server OTP di `config.py`:
```python
self.SERVER_WA_OTP_ADDRESS = "http://your_otp_server:port"
```

### 3. Secret Key Aplikasi
1. Generate kunci acak yang aman
2. Perbarui secret key di `config.py`:
```python
self.APP_SECRET = "your_secure_secret_key"
```

## Integrasi WhatsApp OTP

### Gambaran Umum
Aplikasi menggunakan WhatsApp OTP (One-Time Password) untuk verifikasi pengguna. Sistem ini memastikan registrasi dan autentikasi pengguna yang aman melalui pesan WhatsApp.

### Alur OTP
1. Pengguna memasukkan detail registrasi
2. Sistem menghasilkan OTP 6 digit
3. OTP dikirim ke nomor WhatsApp pengguna
4. Pengguna memasukkan OTP untuk verifikasi
5. Akun diaktifkan setelah verifikasi berhasil

### Pilihan Konfigurasi OTP

#### 1. Menggunakan Layanan WhatsApp OTP yang Disediakan
Hubungi pengembang untuk integrasi:
- Telepon: 082113791904
- Fitur:
  - Pengiriman pesan WhatsApp otomatis
  - Pembuatan dan validasi OTP
  - Enkripsi pesan aman
  - Perlindungan rate limiting
  - Pemantauan percobaan gagal

#### 2. Implementasi Kustom
Bangun sistem OTP sendiri menggunakan:
1. WhatsApp Business API
2. Bot WhatsApp Kustom
   - Contoh implementasi: [Go-OpenAI-WhatsApp-Bot](https://github.com/alipbudiman/Go-OpenAI-WhatsApp-Bot)
   - Modifikasi yang diperlukan:
     ```python
     # Tambahkan pembuatan OTP
     # Tambahkan template pesan
     # Implementasikan endpoint verifikasi
     ```

### Langkah-langkah Keamanan
1. Masa Berlaku OTP: 10 menit
2. Maksimum Percobaan: 3 kali
3. Masa Jeda: 10 menit setelah percobaan gagal
4. Rate Limiting berbasis IP
5. Validasi Nomor Telepon
6. Perlindungan Anti-Spam

## Koleksi Database

Aplikasi menggunakan koleksi MongoDB berikut:

1. `account` - Data autentikasi pengguna
2. `user_log` - Data sesi aktif
3. `user_history` - Catatan riwayat penilaian

## Implementasi Certainty Factor

Sistem mengevaluasi risiko stunting menggunakan beberapa faktor:

1. Pengukuran Fisik (G1, G2)
   - Rasio tinggi-untuk-usia
   - Rasio berat-untuk-tinggi

2. Indikator Kesehatan (G3, G4)
   - Perkembangan kognitif
   - Kerentanan terhadap infeksi

3. Pola Pertumbuhan (G5)
   - Perubahan komposisi tubuh
   - Kecepatan pertumbuhan

4. Indikator Perilaku (G6-G9)
   - Interaksi sosial
   - Praktik pemberian makan
   - Riwayat medis

## Detail Aturan Stunting

Aturan-aturan yang digunakan dalam sistem ini tersimpan dalam format Excel ([RULE_STUNTING_CRITERIA.xlsx](/RULE_STUNTING_CRITERIA.xlsx)) dengan struktur sebagai berikut:

### Kategori Gejala dan Nilai CF

1. **Input Awal (G1-G2)**
   - G1: Tinggi Badan/Usia, Panjang Badan/Usia (CF: 1.0)
   - G2: Berat Badan/Panjang Badan, Berat Badan/Tinggi Badan beberapa bulan terakhir (CF: 0.8)

2. **Indikator Perkembangan (G3-G4)**
   - G3: Kemampuan Kognitif [Ya/Tidak] (CF: 0.6)
   - G4: Riwayat penyakit infeksi (demam, muntah, diare) [Text] (CF: 0.6)

3. **Indikator Fisik (G5-G6)**
   - G5: Proporsi tubuh (gemuk pendek) [5 opsi] (CF: 0.6)
   - G6: Perilaku sosial (kontak mata) [5 opsi] (CF: 0.6)

4. **Riwayat Kesehatan (G7-G9)**
   - G7: Anemia/TBC [Text] (CF: 0.6)
   - G8: Riwayat ASI Eksklusif [Ya/Tidak] (CF: 0.6)
   - G9: MPASI dini [Ya/Tidak] (CF: 0.6)

### Nilai Certainty Factor (CF)

| Uncertain Term | CF PAKAR |
|---------------|----------|
| Definitely (Pasti) | 1.0 |
| Almost Certainty (Hampir Pasti) | 0.8 |
| Probably (Kemungkinan Besar) | 0.6 |
| Maybe (Mungkin) | 0.4 |
| Unknown (Tidak Tahu) | -0.2 to 0.2 |
| Maybe Not (Mungkin Tidak) | -0.4 |
| Probably Not (Kemungkinan Besar Tidak) | -0.6 |
| Almost Certainly Not (Hampir Pasti Tidak) | -0.8 |
| Definitely Not (Pasti Tidak) | -1.0 |

### Rumus Perhitungan CF

```
1. Perhitungan CF per Gejala:
   CFGx = CF_user * CF_pakar

2. Kombinasi CF:
   CF_combine1 (CF_gejala1, CF_gejala4) = CF_gejala1 + CF_gejala4 * (1 - CF_gejala1)
   
3. Kombinasi dengan CF Sebelumnya:
   CF_combine2 (CF_old, CF_gejala2) = CF_old + CF_gejala2 * (1 - CF_old)

4. Urutan Evaluasi:
   - Hitung CFG1 = CF_user * CF_pakar
   - Hitung CFG4 = CF_user * CF_pakar
   - Hitung CFG2 = CF_user * CF_pakar
   - Kombinasikan menggunakan rumus CF_combine
```

## Menjalankan Aplikasi

Mulai aplikasi:
```bash
python app.py
```
Aplikasi akan tersedia di `http://localhost:5000`

## Pertimbangan Keamanan

1. Selalu gunakan HTTPS di produksi
2. Perbarui dependensi secara teratur
3. Terapkan rate limiting untuk permintaan OTP
4. Gunakan manajemen sesi yang aman
5. Validasi semua input pengguna

## Kontribusi

1. Fork repositori
2. Buat branch fitur Anda
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request baru

## Dukungan

Untuk dukungan integrasi WhatsApp OTP atau pertanyaan, hubungi:
- Pengembang: 082113791904
- Alternatif: Bangun solusi kustom menggunakan contoh di [Go-OpenAI-WhatsApp-Bot](https://github.com/alipbudiman/Go-OpenAI-WhatsApp-Bot)

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detail.