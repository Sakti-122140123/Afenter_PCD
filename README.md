# 🅿️ Dashboard Deteksi Area Parkir Motor - AFEnter

Dashboard Streamlit untuk mendeteksi area parkir motor di lingkungan kampus ITERA menggunakan pengolahan citra digital.

## 👥 Kelompok AFEnter

**Judul:** PENERAPAN PENGOLAHAN CITRA DIGITAL UNTUK MENDETEKSI AREA PARKIR DI LINGKUNGAN KAMPUS ITERA

**Institut:** Institut Teknologi Sumatera (ITERA)

## 📋 Deskripsi

Dashboard ini menerapkan metode pengolahan citra digital untuk mendeteksi area parkir kosong dan terisi pada gambar area parkir kampus ITERA. Sistem dapat memproses gambar dari dataset maupun foto yang diupload pengguna.

## ✨ Fitur

- 🏠 **Beranda**: Informasi judul, latar belakang, dan tujuan penelitian
- 📊 **Dataset & Tujuan**: Detail dataset dan alur proses pengolahan citra
- 🔬 **Proses Citra**: Pemrosesan gambar dari dataset dengan visualisasi tahapan
- 📤 **Upload Foto**: Upload dan proses foto sendiri dengan validasi otomatis

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+**
- **Streamlit**: Framework web dashboard
- **OpenCV**: Pemrosesan citra
- **NumPy**: Komputasi numerik
- **rembg**: Remove background otomatis
- **Matplotlib**: Visualisasi
- **Pillow**: Manipulasi gambar

## 📦 Instalasi

### 1. Clone atau Download Repository

```powershell
cd d:\Sakti\PCD\Dashboard
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Catatan:** Instalasi `rembg` membutuhkan waktu karena akan mendownload model AI (~176MB).

## 🚀 Cara Menjalankan

### 1. Jalankan Dashboard

```powershell
streamlit run app.py
```

Dashboard akan terbuka otomatis di browser pada alamat: `http://localhost:8501` atau Network URL: http://192.168.1.112:8501

### 2. Siapkan Dataset (Opsional)

Jika ingin menggunakan fitur "Proses Citra" dengan dataset:

1. Buat folder `dataset` di direktori yang sama dengan `app.py`
2. Masukkan gambar-gambar area parkir ke dalam folder tersebut
3. Format yang didukung: `.jpg`, `.jpeg`, `.png`, `.heic`

Contoh struktur folder:
```
Dashboard/
├── app.py
├── image_processing.py
├── requirements.txt
├── dataset/
│   ├── GK1/
│   │   ├── foto1.jpg
│   │   └── foto2.jpg
│   ├── GK2/
│   │   └── foto3.jpg
│   └── LabTek1/
│       └── foto4.jpg
```

## 📖 Cara Menggunakan Dashboard

### Halaman Beranda
- Menampilkan judul penelitian
- Latar belakang masalah parkir di ITERA
- Tujuan penelitian
- Area penelitian dan jumlah dataset

### Halaman Dataset & Tujuan
- Informasi detail tentang dataset yang digunakan
- Link download dataset dari Google Drive
- Penjelasan lengkap 11 tahapan pengolahan citra

### Halaman Proses Citra
1. Pilih gambar dari dropdown (otomatis membaca dari folder `dataset`)
2. Klik tombol **"🚀 Proses Gambar"**
3. Sistem akan memproses dan menampilkan:
   - Statistik: Total slot, slot terisi, slot kosong, jumlah motor
   - Status per slot (Occupied/Empty)
   - 9 tahapan visualisasi pemrosesan citra

### Halaman Upload Foto Sendiri
1. Baca **ketentuan upload** dengan teliti
2. Upload foto (.jpg, .jpeg, .png)
3. Sistem akan melakukan validasi otomatis:
   - Cek blur/tidak jelas
   - Cek jumlah motor (max 4)
4. Klik **"🚀 Proses Gambar Upload"**
5. Lihat hasil deteksi dan visualisasi

## ⚠️ Ketentuan Upload Foto

Untuk hasil optimal, foto yang diupload harus memenuhi ketentuan:

1. ✅ Foto berisikan **maksimal 4 motor** saja
2. ✅ Bagian bawah foto menampakkan **ban motor**
3. ✅ Foto harus **jelas, tidak blur**
4. ✅ Foto kendaraan **tidak boleh bertumpuk** dengan kendaraan lain
5. ✅ Hanya area parkir **bagian pojok**
6. ✅ Gambar diambil dari jarak **kurang lebih 2 meter**

## 🔬 Alur Pemrosesan Citra

1. **Ambil Gambar** → Scanning folder dataset
2. **Remove Background** → Hapus latar belakang menggunakan AI (rembg)
3. **Resize Image** → Seragamkan ukuran 960×540 pixel
4. **Grayscale & Blur** → Konversi ke grayscale + Gaussian blur
5. **Threshold Otsu** → Binarisasi otomatis
6. **Morfologi** → Closing + Opening untuk membersihkan noise
7. **Distance Transform** → Identifikasi area motor yang pasti
8. **ROI** → Fokus pada area parkir (35% dari atas dihilangkan)
9. **Deteksi Kontur** → Filter kontur berdasarkan luas (300-250.000 piksel)
10. **Bagi Slot** → Membagi gambar menjadi 4 slot parkir
11. **Cek Occupancy** → Deteksi slot terisi atau kosong

## 📁 Struktur Project

```
Dashboard/
├── app.py                    # File utama aplikasi Streamlit
├── image_processing.py       # Modul pemrosesan citra
├── requirements.txt          # Dependencies Python
├── README.md                 # Dokumentasi (file ini)
├── dataset/                  # Folder dataset (buat sendiri)
│   └── README.md
└── venv/                     # Virtual environment (opsional)
```

## 🔧 Troubleshooting

### Error: ModuleNotFoundError
```powershell
pip install -r requirements.txt
```

### Error: rembg tidak bisa mendownload model
- Pastikan koneksi internet stabil
- Coba install ulang: `pip uninstall rembg` lalu `pip install rembg`

### Dashboard tidak terbuka di browser
- Pastikan port 8501 tidak digunakan aplikasi lain
- Coba jalankan dengan port berbeda: `streamlit run app.py --server.port 8502`

### Gambar tidak muncul di halaman "Proses Citra"
- Pastikan folder `dataset` sudah dibuat
- Pastikan ada file gambar (.jpg, .png, .jpeg, .heic) di dalam folder

### Hasil deteksi tidak akurat
- Pastikan foto memenuhi ketentuan (jelas, tidak blur, max 4 motor)
- Coba foto dengan pencahayaan lebih baik
- Pastikan motor tidak bertumpuk/overlap

## 📊 Link Dataset

Dataset primer (243 citra) dapat didownload dari:
[Google Drive - Dataset Parkir ITERA](https://drive.google.com/drive/folders/1_Yisu9bMHBWHbZx7UoBywWo2qlKj73br)

## 📝 Catatan Pengembangan

- Dashboard ini menggunakan **rembg** untuk background removal yang memerlukan model AI
- Proses pertama kali akan lebih lama karena download model (~176MB)
- Hasil terbaik didapat dari foto dengan:
  - Pencahayaan baik
  - Sudut pandang dari atas (bird's eye view)
  - Motor tidak saling bertumpuk
  - Latar belakang kontras dengan motor

## 👨‍💻 Pengembang

**Kelompok AFEnter**
- Mata Kuliah: Pengolahan Citra Digital
- Institusi: Institut Teknologi Sumatera (ITERA)
- Tahun: 2025

## 📄 Lisensi

Project ini dibuat untuk keperluan akademik tugas akhir mata kuliah Pengolahan Citra Digital.

---

**Selamat menggunakan Dashboard Deteksi Area Parkir! 🚀**

Jika ada pertanyaan atau masalah, silakan hubungi kelompok AFEnter.
