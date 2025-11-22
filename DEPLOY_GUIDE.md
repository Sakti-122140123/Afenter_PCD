# 🚀 Panduan Deploy ke Streamlit Cloud

## 📋 Prerequisites

1. Akun GitHub (untuk repository)
2. Akun Streamlit Cloud (https://share.streamlit.io/)

## 📁 File yang Sudah Disiapkan untuk Deploy

✅ `packages.txt` - Dependencies sistem untuk OpenCV  
✅ `.streamlit/config.toml` - Konfigurasi Streamlit  
✅ `runtime.txt` - Versi Python yang digunakan  
✅ `requirements.txt` - Dependencies Python (sudah ada)  
✅ `app.py` - Aplikasi utama (sudah ada)  
✅ `image_processing.py` - Modul pemrosesan (sudah ada)

## 🔧 Langkah-Langkah Deploy

### 1️⃣ Push ke GitHub

```bash
git add .
git commit -m "Prepare for Streamlit deployment"
git push origin main
```

### 2️⃣ Deploy di Streamlit Cloud

1. Buka https://share.streamlit.io/
2. Login dengan akun GitHub
3. Klik "New app"
4. Pilih repository: `byllee/Afenter_PCD`
5. Branch: `main`
6. Main file path: `app.py`
7. Klik "Deploy!"

### 3️⃣ Tunggu Proses Deploy

- Streamlit akan otomatis:
  - Install dependencies dari `requirements.txt`
  - Install system packages dari `packages.txt`
  - Setup Python version dari `runtime.txt`
  - Apply config dari `.streamlit/config.toml`

### 4️⃣ App Siap Digunakan!

Setelah deploy selesai, app akan tersedia di URL:

```
https://share.streamlit.io/[username]/afenter-pcd/main/app.py
```

## ⚠️ Catatan Penting

### Dataset

- Folder `dataset/` di repository akan ikut ter-deploy
- Pastikan dataset sudah ter-commit ke GitHub
- Jika dataset terlalu besar (>100MB), pertimbangkan:
  - Upload ke GitHub LFS
  - Atau gunakan external storage (Google Drive, S3, dll)

### Troubleshooting

**Problem: OpenCV error**

- Sudah ditangani dengan `packages.txt` yang berisi:
  ```
  libgl1-mesa-glx
  libglib2.0-0
  ```

**Problem: Memory error saat remove background**

- `rembg` menggunakan AI model yang cukup berat
- Jika error, coba kurangi ukuran gambar di `resize_image()`

**Problem: Upload file terlalu besar**

- Sudah diatur `maxUploadSize = 200` MB di config.toml
- Jika masih error, user harus upload gambar lebih kecil

**Problem: App loading lambat**

- Normal untuk first load karena install rembg model
- Subsequent loads akan lebih cepat

## 🔗 Link Penting

- **Streamlit Cloud**: https://share.streamlit.io/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Deploy Tutorial**: https://docs.streamlit.io/streamlit-community-cloud/get-started

## 📞 Support

Jika ada masalah saat deploy, cek:

1. Logs di Streamlit Cloud dashboard
2. Pastikan semua file ter-commit dengan benar
3. Verifikasi `requirements.txt` compatible

---

**Kelompok AFEnter** - Institut Teknologi Sumatera (ITERA) © 2025
