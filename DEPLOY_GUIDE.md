# 🚀 Panduan Deploy ke Streamlit Cloud

## 📋 Prerequisites

1. Akun GitHub (untuk repository)
2. Akun Streamlit Cloud (https://share.streamlit.io/)

## 📁 File yang Sudah Disiapkan untuk Deploy

✅ `packages.txt` - Dependencies sistem untuk OpenCV  
✅ `.streamlit/config.toml` - Konfigurasi Streamlit  
✅ `runtime.txt` - Versi Python 3.10  
✅ `requirements.txt` - Dependencies Python (optimized)  
✅ `app.py` - Aplikasi utama  
✅ `image_processing.py` - Modul pemrosesan (with error handling)  
✅ `.gitignore` - Files yang tidak perlu di-commit

## 🔧 Langkah-Langkah Deploy

### 1️⃣ Push ke GitHub

```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin deploy
```

### 2️⃣ Deploy di Streamlit Cloud

1. Buka https://share.streamlit.io/
2. Login dengan akun GitHub
3. Klik "New app"
4. Pilih repository: `byllee/Afenter_PCD`
5. Branch: `deploy` (atau `main` jika sudah merge)
6. Main file path: `app.py`
7. Klik "Deploy!"

### 3️⃣ Tunggu Proses Deploy (5-10 menit)

Streamlit akan otomatis:

- ✅ Install system packages (`libgl1`, `libglib2.0-0`)
- ✅ Setup Python 3.10
- ✅ Install Python dependencies
- ✅ Download rembg AI model (~180MB)
- ✅ Apply config

### 4️⃣ App Siap Digunakan! 🎉

URL app akan seperti:

```
https://afenter-pcd.streamlit.app
```

## 🔍 Verifikasi Files Sebelum Deploy

Pastikan files berikut ada dan benar:

### ✅ requirements.txt

```txt
streamlit>=1.28.0
opencv-python-headless==4.8.1.78
numpy>=1.24.0,<2.0.0
matplotlib>=3.7.0
rembg==2.0.50
Pillow>=10.0.0
torch>=2.0.0
onnxruntime
```

### ✅ packages.txt

```txt
libgl1
libglib2.0-0
```

### ✅ runtime.txt

```txt
python-3.10
```

## ⚠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'cv2'"

**Solusi:** Pastikan menggunakan `opencv-python-headless`, bukan `opencv-python`

### Error: "OSError: libGL.so.1: cannot open shared object file"

**Solusi:** Pastikan `packages.txt` berisi `libgl1` dan `libglib2.0-0`

### Error: "No module named 'torch'"

**Solusi:** Tambahkan `torch>=2.0.0` dan `onnxruntime` di requirements.txt

### Error: Memory/Timeout saat processing

**Solusi:**

- Rembg model berat (~180MB)
- First load akan lambat (normal)
- Kurangi ukuran gambar jika perlu

### Error: Dataset tidak muncul

**Solusi:**

- Pastikan folder `dataset/` ter-commit ke GitHub
- Cek size dataset (max ~500MB untuk free tier)
- Jika terlalu besar, gunakan sample dataset saja

## 📊 Optimasi Performa

### Caching (sudah implemented)

```python
@st.cache_resource
def load_model():
    # Model di-cache agar tidak reload setiap kali
    pass
```

### Lazy Loading

- Dataset hanya dimuat saat halaman "Proses Citra" dibuka
- Background removal hanya saat tombol diklik

### Error Handling

- Fallback jika background removal gagal
- Validasi gambar sebelum proses
- User-friendly error messages

## 🔗 Link Penting

- **Streamlit Cloud**: https://share.streamlit.io/
- **Docs**: https://docs.streamlit.io/
- **Community**: https://discuss.streamlit.io/
- **GitHub Repo**: https://github.com/byllee/Afenter_PCD

## 📈 Monitoring

Setelah deploy, monitor:

1. **App logs** - Cek errors di Streamlit dashboard
2. **Resource usage** - CPU/Memory di metrics
3. **Response time** - First load vs subsequent loads

## 🆘 Support

Jika masih error:

1. Cek logs di Streamlit Cloud dashboard (klik "Manage app" → "Logs")
2. Copy error message lengkap
3. Cek compatibility Python 3.10 + package versions
4. Test locally dulu: `streamlit run app.py`

---

**Kelompok AFEnter** - Institut Teknologi Sumatera (ITERA) © 2025
