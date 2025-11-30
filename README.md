# 🅿️ Deteksi Area Parkir Motor

## 📋 Deskripsi

Aplikasi ini menggunakan berbagai teknik pengolahan citra untuk mendeteksi dan menghitung jumlah motor pada area parkir, meliputi:

- Background Removal (menggunakan `rembg`)
- Grayscale Conversion
- Gaussian Blur
- Otsu Thresholding
- Operasi Morfologi (Opening & Closing)
- Distance Transform
- Watershed Segmentation

---

## 🌐 Akses Aplikasi

Aplikasi sudah di-deploy dan dapat diakses langsung melalui:

**🔗 [https://afenter.streamlit.app/](https://afenter.streamlit.app/)**

---

## 🚀 Menjalankan Secara Lokal (Opsional)

Jika ingin menjalankan di komputer lokal:

### 1. Clone Repository

```bash
git clone https://github.com/byllee/Afenter_PCD.git
cd Afenter_PCD
git checkout deploy
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

---

## 📦 Dependencies

- `streamlit` - Framework web app
- `opencv-python-headless` - Pengolahan citra
- `numpy` - Operasi array
- `matplotlib` - Visualisasi
- `rembg` - Background removal
- `onnxruntime` - Runtime untuk model ML
- `Pillow` - Manipulasi gambar

---

## 📁 Struktur Proyek

```
Afenter_PCD/
├── app.py                 # Aplikasi utama Streamlit
├── image_processing.py    # Modul pemrosesan citra
├── requirements.txt       # Daftar dependencies
├── README.md              # Dokumentasi
└── dataset/               # Folder dataset gambar
    └── All Dataset/       # Koleksi gambar parkir
```

---

## 🖼️ Fitur

- ✅ Upload gambar parkir motor
- ✅ Pilih gambar dari dataset yang tersedia
- ✅ Visualisasi tahapan pemrosesan citra
- ✅ Deteksi dan penghitungan jumlah motor
- ✅ Validasi kualitas gambar (deteksi blur)

---

## 👥 Tim AFEnter

Kelompok mahasiswa Institut Teknologi Sumatera (ITERA) untuk tugas mata kuliah Pengolahan Citra Digital.

| Nama                         | NIM       | Role                                |
| ---------------------------- | --------- | ----------------------------------- |
| Nur Afni Daem Miarti         | 122140011 | Image Processing Engineer           |
| Muhammad Fadhil Alfitra Budi | 122140025 | UI/UX & Presentation Designer       |
| Nayla Fayyiza Khairina       | 122140033 | Image Processing Engineer           |
| Febriani Nawang Wulan        | 122140071 | Research & Documentation Specialist |
| Sakti Mujahid Imani          | 122140123 | Project Manager (PM)                |
| Bayu Prameswara Haris        | 122140219 | Data Analyst & Evaluator            |

---

## 📝 Lisensi

Proyek ini dibuat untuk keperluan akademik.
