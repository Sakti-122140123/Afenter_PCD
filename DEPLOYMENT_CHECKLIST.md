# ✅ Deployment Checklist - Streamlit Cloud

## 📦 Files yang Harus Ada

### ✅ Wajib Ada:

- [x] `app.py` - Main application file
- [x] `image_processing.py` - Image processing module
- [x] `requirements.txt` - Python dependencies
- [x] `packages.txt` - System dependencies (Linux packages)
- [x] `runtime.txt` - Python version specification
- [x] `.streamlit/config.toml` - Streamlit configuration

### ✅ Optional:

- [x] `README.md` - Project documentation
- [x] `DEPLOY_GUIDE.md` - Deployment guide
- [x] `dataset/` - Sample images (optional, bisa besar)
- [x] `.gitignore` - Files to ignore

## 🔍 Pre-Deployment Verification

### 1. Check `requirements.txt`

```txt
streamlit>=1.28.0          ✅ Installed
opencv-python-headless     ✅ Headless version (no GUI)
numpy<2.0.0               ✅ Version compatible
Pillow>=10.0.0            ✅ Image processing
rembg==2.0.50             ✅ Background removal
onnxruntime               ✅ For rembg model
```

**❌ TIDAK BOLEH:**

- `opencv-python` (use headless version)
- `torch` tanpa version (terlalu besar, >1GB)
- `matplotlib` jika tidak digunakan

### 2. Check `packages.txt`

```txt
libgl1          ✅ OpenCV dependency
libglib2.0-0    ✅ System library
libgomp1        ✅ OpenMP support
```

### 3. Check `runtime.txt`

```txt
python-3.10     ✅ Stable version
```

**✅ Supported:** 3.9, 3.10, 3.11
**❌ Not recommended:** 3.12 (too new)

### 4. Check `app.py` Imports

```python
✅ import streamlit as st
✅ import cv2
✅ import numpy as np
✅ from PIL import Image
✅ import os
✅ from image_processing import process_parking_image

❌ import matplotlib.pyplot (REMOVED - not needed)
❌ import io (REMOVED - not needed)
```

### 5. Check for Caching

```python
@st.cache_data              ✅ Added to load_dataset_images()
@st.cache_resource          ✅ Can be added for heavy operations
```

## 🚀 Deployment Steps

### Step 1: Commit to GitHub

```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment - optimized"
git push origin deploy
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select:
   - Repository: `byllee/Afenter_PCD`
   - Branch: `deploy`
   - Main file: `app.py`
4. Click "Deploy!"

### Step 3: Wait for Build (5-10 minutes)

Monitor logs for:

- ✅ Installing system packages...
- ✅ Installing Python packages...
- ✅ Downloading rembg model (~180MB)
- ✅ Starting Streamlit...

## ⚠️ Common Errors & Solutions

### Error 1: "ModuleNotFoundError: No module named 'cv2'"

**Solution:** Check requirements.txt uses `opencv-python-headless`

### Error 2: "ImportError: libGL.so.1"

**Solution:** Add `libgl1` to packages.txt

### Error 3: "Cannot install torch"

**Solution:** Remove `torch` from requirements.txt (rembg uses onnxruntime)

### Error 4: "Memory limit exceeded"

**Solution:**

- Remove large dataset files
- Use sample images only
- Reduce image size in `resize_image()`

### Error 5: "Build timeout"

**Solution:**

- Too many/large dependencies
- Check if dataset folder is too large
- Consider using .slugignore

## 📊 Performance Optimization

### Current Optimizations:

- ✅ `@st.cache_data` for dataset loading
- ✅ Removed unused imports (matplotlib, io)
- ✅ Using opencv-headless (smaller)
- ✅ onnxruntime instead of torch
- ✅ Error handling with fallback

### Additional Tips:

- First load will be slow (~2-3 min) - normal
- Subsequent loads faster (~5-10 sec)
- Rembg model downloads on first use
- Keep dataset folder small (<100MB)

## 🔗 Important Links

- **App URL:** Will be `https://[your-app-name].streamlit.app`
- **Dashboard:** https://share.streamlit.io/
- **Logs:** Click "Manage app" → "Logs"
- **Docs:** https://docs.streamlit.io/

## ✅ Final Checklist Before Deploy

- [ ] All imports correct in app.py
- [ ] No matplotlib if not used
- [ ] requirements.txt has headless opencv
- [ ] packages.txt has system dependencies
- [ ] runtime.txt specifies python version
- [ ] Dataset folder size reasonable
- [ ] All files committed to GitHub
- [ ] Branch is `deploy` or `main`
- [ ] No secrets in code (if any, use secrets.toml)

## 🎉 Success Indicators

When deployment succeeds:

1. ✅ Build logs show "Your app is live!"
2. ✅ Can access app URL
3. ✅ All 4 pages load without error
4. ✅ Can upload and process images
5. ✅ Dataset images (if any) load correctly

---

**Kelompok AFEnter** - ITERA © 2025
