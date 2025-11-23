"""
Dashboard Streamlit - Deteksi Area Parkir Motor
Kelompok: AFEnter
Institut Teknologi Sumatera (ITERA)
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from image_processing import process_parking_image
import io


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Dashboard Deteksi Parkir - AFEnter",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header h1 {
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        font-family: 'Poppins', sans-serif;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #e1f5ff 0%, #b3e5fc 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffc107;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        font-family: 'Poppins', sans-serif;
    }
    
    .member-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .member-card:hover {
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
        border-left-color: #764ba2;
    }
    
    .member-name {
        font-weight: 600;
        color: #667eea;
        font-size: 18px;
        margin-bottom: 5px;
    }
    
    .member-nim {
        color: #666;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .member-role {
        color: #764ba2;
        font-size: 14px;
        font-style: italic;
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border: none;
        margin: 30px 0;
        border-radius: 2px;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNGSI HELPER
# =========================================================
def load_dataset_images(dataset_path="dataset"):
    """Memuat semua gambar dari folder dataset"""
    if not os.path.exists(dataset_path):
        return []
    
    images = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.heic')):
                images.append(os.path.join(root, file))
    return images


def validate_image(image_array, max_motors=4):
    """
    Validasi gambar sesuai ketentuan
    Returns: (is_valid, message)
    """
    # Cek blur menggunakan Laplacian variance
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    if laplacian_var < 100:
        return False, "❌ Gambar terlalu blur! Pastikan foto jelas dan fokus."
    
    return True, "✅ Gambar memenuhi ketentuan dasar."


def display_process_steps(results):
    """Menampilkan langkah-langkah pemrosesan dalam grid"""
    st.subheader("📊 Tahapan Pemrosesan Citra")
    
    # Buat 3 kolom untuk 9 gambar
    steps = [
        ("Original", results['original'], False),
        ("No Background", results['no_background'], False),
        ("Grayscale", results['grayscale'], True),
        ("Gaussian Blur", results['gaussian_blur'], True),
        ("Threshold (Otsu)", results['threshold'], True),
        ("Morphology", results['morphology'], True),
        ("Distance Transform", results['distance_transform'], True),
        ("Sure Foreground", results['sure_foreground'], True),
        ("Final Detection", results['final_output'], False)
    ]
    
    # Tampilkan dalam grid 3x3
    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(steps):
                title, img, is_gray = steps[i + j]
                with cols[j]:
                    st.markdown(f"**{i+j+1}. {title}**")
                    if is_gray:
                        st.image(img, use_container_width=True, clamp=True)
                    else:
                        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_container_width=True)


# =========================================================
# HEADER UTAMA
# =========================================================
st.markdown("""
<div class="main-header">
    <h1>🅿️ DASHBOARD DETEKSI AREA PARKIR MOTOR</h1>
    <h3>✨ Kelompok AFEnter ✨</h3>
    <p style="font-size: 16px; margin-top: 10px;">Institut Teknologi Sumatera (ITERA)</p>
    <p style="font-size: 14px; opacity: 0.9;">Pengolahan Citra Digital - 2025</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR - NAVIGASI
# =========================================================
st.sidebar.title("📋 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["🏠 Beranda", "📊 Dataset & Tujuan", "🔬 Proses Citra", "📤 Upload Foto Sendiri"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👥 Anggota Kelompok AFEnter")
st.sidebar.markdown("""
<div>
<b>🔹 Sakti Mujahid Imani</b><br>
<span style='color: #666;'>122140123 - Project Manager</span><br><br>

<b>🔹 Nur Afni Daem Miarti</b><br>
<span style='color: #666;'>122140011 - Image Processing</span><br><br>

<b>🔹 Nayla Fayyiza Khairina</b><br>
<span style='color: #666;'>122140033 - Image Processing</span><br><br>

<b>🔹 Febriani Nawang Wulan</b><br>
<span style='color: #666;'>122140071 - Research & Docs</span><br><br>

<b>🔹 Bayu Prameswara Haris</b><br>
<span style='color: #666;'>122140219 - Data Analyst</span><br><br>

<b>🔹 Muhammad Fadhil A.B.</b><br>
<span style='color: #666;'>122140025 - UI/UX Designer</span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("**Mata Kuliah:** Pengolahan Citra Digital")
st.sidebar.markdown("**Program Studi:** Teknik Informatika ITERA")


# =========================================================
# HALAMAN 1: BERANDA
# =========================================================
if menu == "🏠 Beranda":
    st.header("📌 Judul Project")
    st.markdown("""
    <div>
        <h3 style="color: #667eea;">PENERAPAN PENGOLAHAN CITRA DIGITAL UNTUK MENDETEKSI AREA PARKIR DI LINGKUNGAN KAMPUS ITERA</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📖 Latar Belakang")
    st.markdown("""
    <div style="text-align: justify;">
    Peningkatan jumlah civitas akademika setiap tahunnya membuat kebutuhan lahan parkir semakin tinggi, 
    sementara ketersediaan area parkir tetap terbatas. Kondisi ini menyebabkan pengguna kendaraan kesulitan 
    menemukan slot kosong, terutama pada jam-jam sibuk, sehingga memicu munculnya perilaku parkir tidak teratur.
    Di lingkungan ITERA, permasalahan tersebut semakin jelas terlihat, di mana banyak mahasiswa memarkirkan 
    kendaraan tidak sesuai dengan area yang telah disediakan. Akibatnya, area parkir menjadi tidak tertata 
    dan sering muncul kerancuan dalam menilai apakah suatu ruang masih cukup untuk satu motor atau tidak.
    Selain itu, sistem parkir di kampus yang masih bersifat manual mengharuskan pengguna berkeliling untuk 
    mengecek ketersediaan tempat parkir, sehingga tidak efisien dan tidak mendukung mobilitas yang lancar.
    Untuk mengatasi hal ini, teknologi computer vision melalui pengolahan citra digital menawarkan solusi 
    dengan kemampuan mengidentifikasi area parkir kosong tanpa pemasangan sensor fisik. Penerapan analisis citra 
    pada area parkir ITERA diharapkan mampu membantu mendeteksi slot kosong secara otomatis serta mendukung 
    terciptanya sistem parkir yang lebih tertata dan selaras dengan konsep smart campus.
    </div>
    """, unsafe_allow_html=True)
    
    st.header("🎯 Tujuan")
    st.markdown("""
    <div
    </b> Menerapkan metode pengolahan citra digital dalam mendeteksi area parkir kosong serta area yang terisi 
    kendaraan pada citra area parkir kampus Institut Teknologi Sumatera (ITERA) secara akurat dan efisien</b>.
    </div>
    """, unsafe_allow_html=True)
    
    # Gambar ilustrasi (opsional)
    st.header("🏫 Area Penelitian")
    col1, col2 = st.columns(2)
    with col1:
        st.info("📍 **Lokasi Pengambilan Dataset:**")
        st.markdown("""
        - Gedung Kuliah (GK-1 dan GK-2)
        - Laboratorium Teknik 1 dan 3
        - Gedung C dan E
        """)
    with col2:
        st.info("📈 **Jumlah Data:**")
        st.markdown("""
        - **243 citra** area parkir motor
        - Berbagai kondisi pencahayaan
        - Berbagai tingkat kepadatan (Occupancy)
        """)
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # Section Anggota Kelompok
    st.header("👥 Anggota Kelompok AFEnter")
    
    # Baris 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="member-card">
            <div class="member-name">🫅 Sakti Mujahid Imani</div>
            <div class="member-nim">NIM: 122140123</div>
            <div class="member-role">Project Manager (PM)</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="member-card">
            <div class="member-name">👩‍⚖️ Nayla Fayyiza Khairina</div>
            <div class="member-nim">NIM: 122140033</div>
            <div class="member-role">Image Processing Engineer</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="member-card">
            <div class="member-name">👨‍🔧 Bayu Prameswara Haris</div>
            <div class="member-nim">NIM: 122140219</div>
            <div class="member-role">Data Analyst & Evaluator</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="member-card">
            <div class="member-name">👩‍⚖️ Nur Afni Daem Miarti</div>
            <div class="member-nim">NIM: 122140011</div>
            <div class="member-role">Image Processing Engineer</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="member-card">
            <div class="member-name">👩‍💼 Febriani Nawang Wulan</div>
            <div class="member-nim">NIM: 122140071</div>
            <div class="member-role">Research & Documentation Specialist</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="member-card">
            <div class="member-name">👨‍🎨 Muhammad Fadhil Alfitra Budi</div>
            <div class="member-nim">NIM: 122140025</div>
            <div class="member-role">UI/UX & Presentation Designer</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# HALAMAN 2: DATASET & TUJUAN
# =========================================================
elif menu == "📊 Dataset & Tujuan":
    st.header("📦 Sumber Dataset")
    
    st.markdown("""
    <div>
        <h4>Dataset Primer</h4>
        <p>Dataset yang dikumpulkan sebanyak <b>243 citra</b> yang tersebar di:</p>
        <ul>
            <li>Gedung Kuliah Umum 1 (GKU-1)</li>
            <li>Gedung Kuliah Umum 2 (GKU-2)</li>
            <li>Laboratorium Teknik 1</li>
            <li>Laboratorium Teknik 3</li>
            <li>Gedung C</li>
            <li>Gedung E</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔗 Link Dataset")
    st.markdown("""
    [📥 Download Dataset dari Google Drive](https://drive.google.com/drive/folders/1_Yisu9bMHBWHbZx7UoBywWo2qlKj73br)
    """)
    
    st.markdown("---")
    
    st.header("⚙️ Alur Proses Pengolahan Citra")
    
    with st.expander("📖 Lihat Detail Setiap Tahap"):
        steps_detail = {
            "1. Ambil Gambar dari Dataset": "Program melakukan scanning seluruh folder menggunakan os.walk(). Setiap file gambar (JPG, PNG, JPEG) dimasukkan ke dalam list untuk diproses.",
            
            "2. Remove Background": "Menggunakan library rembg dengan model AI untuk memisahkan objek motor dari latar belakang, sehingga fokus pada kendaraan.",
            
            "3. Resize Image": "Gambar di-resize menjadi 960 × 540 pixel untuk memastikan komputasi stabil dan konsisten.",
            
            "4. Grayscale → Gaussian Blur": "Konversi ke grayscale untuk menyederhanakan data, kemudian Gaussian Blur untuk mengurangi noise.",
            
            "5. Thresholding Otsu": "Mengubah citra menjadi hitam-putih otomatis berdasarkan histogram. Motor menjadi putih, background hitam.",
            
            "6. Morfologi (Closing → Opening)": "Closing menutup lubang kecil pada objek. Opening menghapus noise kecil. Hasilnya objek motor lebih solid.",
            
            "7. Distance Transform": "Menghitung jarak setiap piksel putih ke tepi terdekat, menghasilkan area 'sure foreground' yang pasti merupakan motor.",
            
            "8. Tentukan ROI": "Mengambil 35% dari atas gambar untuk fokus pada area parkir, menghilangkan langit/tembok.",
            
            "9. Deteksi Kontur Motor": "Menganalisis kontur dengan luas piksel 300-250.000. Terlalu kecil = noise, terlalu besar = bukan motor.",
            
            "10. Bagi Menjadi 4 Slot": "Lebar gambar dibagi 4 bagian sama besar, setiap bagian = 1 slot parkir.",
            
            "11. Cek Occupancy": "Setiap slot dicek apakah ada motor. Jika ada overlap → Occupied (merah), jika tidak → Empty (hijau)."
        }
        
        for step, desc in steps_detail.items():
            st.markdown(f"**{step}**")
            st.write(desc)
            st.markdown("---")


# =========================================================
# HALAMAN 3: PROSES CITRA
# =========================================================
elif menu == "🔬 Proses Citra":
    st.header("🔬 Pemrosesan Gambar dari Dataset")
    
    # Cek keberadaan folder dataset
    dataset_path = "dataset"
    
    if not os.path.exists(dataset_path):
        st.warning(f"⚠️ Folder `{dataset_path}` tidak ditemukan. Silakan buat folder dan masukkan gambar dataset.")
        st.info("📁 Cara: Buat folder bernama `dataset` di direktori yang sama dengan file app.py ini.")
    else:
        images = load_dataset_images(dataset_path)
        
        if len(images) == 0:
            st.warning(f"⚠️ Tidak ada gambar dalam folder `{dataset_path}`. Silakan masukkan gambar (.jpg, .png, .jpeg.)")
        else:
            st.success(f"✅ Ditemukan **{len(images)}** gambar dalam dataset")
            
            # Pilih gambar
            selected_image = st.selectbox(
                "Pilih gambar untuk diproses:",
                images,
                format_func=lambda x: os.path.basename(x)
            )
            
            if st.button("🚀 Proses Gambar", type="primary"):
                if selected_image is None:
                    st.error("Silakan pilih gambar terlebih dahulu")
                else:
                    with st.spinner("Memproses gambar... Mohon tunggu..."):
                        # Baca gambar sebagai bytes
                        with open(selected_image, "rb") as f:
                            image_bytes = f.read()
                        
                        # Proses
                        results = process_parking_image(image_bytes)
                        
                        # Simpan hasil ke session state
                        st.session_state['results'] = results
                        st.success("✅ Pemrosesan selesai!")
            
            # Tampilkan hasil jika ada
            if 'results' in st.session_state:
                results = st.session_state['results']
                
                st.markdown("---")
                
                # Statistik
                st.header("📈 Hasil Deteksi")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-box" style="color: black;">
                        <h2 style="color: black;">{results['total_slots']}</h2>
                        <p>Total Slot</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-box" style="background-color: #ffcdd2; color: black;">
                        <h2 style="color: black;">{results['occupied_slots']}</h2>
                        <p>Slot Terisi</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-box" style="background-color: #c8e6c9; color: black;">
                        <h2 style="color: black;">{results['empty_slots']}</h2>
                        <p>Slot Kosong</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-box" style="color: black;">
                        <h2 style="color: black;">{results['motor_count']}</h2>
                        <p>Motor Terdeteksi</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detail per slot
                st.markdown("### 🅿️ Status Per Slot:")
                cols = st.columns(4)
                for idx, status in enumerate(results['slot_results']):
                    with cols[idx]:
                        if status == "Occupied":
                            st.error(f"**Slot {idx+1}:** {status}")
                        else:
                            st.success(f"**Slot {idx+1}:** {status}")
                
                st.markdown("---")
                
                # Tampilkan semua tahapan
                display_process_steps(results)


# =========================================================
# HALAMAN 4: UPLOAD FOTO SENDIRI
# =========================================================
elif menu == "📤 Upload Foto Sendiri":
    st.header("📤 Upload dan Proses Foto Anda")
    
    # Ketentuan upload
    st.markdown("""
    <div class="info-box" style="color: black;">
        <h4 style="color: black;">⚠️ Ketentuan Upload Foto </h4>
        <ol>
            <li>Foto harus berisikan <b>maksimal 4 motor</b> saja</li>
            <li>Bagian bawah foto harus menampakkan <b>ban motor</b></li>
            <li>Foto harus <b>jelas, tidak blur</b></li>
            <li>Foto kendaraan <b>tidak boleh bertumpuk</b> dengan kendaraan lain</li>
            <li>Hanya bisa parkiran <b>bagian pojok</b></li>
            <li>Gambar diambil dari jarak <b>kurang lebih 2 meter</b></li>
            <li>Format: JPG, JPEG, PNG</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload file
    uploaded_file = st.file_uploader(
        "Pilih gambar area parkir:",
        type=['jpg', 'jpeg', 'png'],
        help="Upload foto area parkir sesuai ketentuan di atas"
    )
    
    if uploaded_file is not None:
        # Tampilkan preview
        st.subheader("👁️ Preview Gambar")
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar yang diupload", use_container_width=True)
        
        # Validasi gambar
        image_array = np.array(image)
        if len(image_array.shape) == 2:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
        elif image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
        else:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        is_valid, message = validate_image(image_array)
        
        if is_valid:
            st.success(message)
        else:
            st.error(message)
        
        # Tombol proses
        if st.button("🚀 Proses Gambar Upload", type="primary", disabled=not is_valid):
            with st.spinner("Memproses gambar Anda... Mohon tunggu..."):
                # Convert ke bytes
                uploaded_file.seek(0)
                image_bytes = uploaded_file.read()
                
                try:
                    # Proses
                    results = process_parking_image(image_bytes)
                    
                    # Cek jumlah motor
                    if results['motor_count'] > 4:
                        st.error(f"❌ Terdeteksi {results['motor_count']} motor! Maksimal 4 motor sesuai ketentuan.")
                        st.warning("Silakan upload gambar lain yang memenuhi ketentuan.")
                    else:
                        st.success(f"✅ Pemrosesan selesai! Terdeteksi {results['motor_count']} motor.")
                        
                        # Simpan hasil
                        st.session_state['upload_results'] = results
                        
                except Exception as e:
                    st.error(f"❌ Terjadi error saat memproses: {str(e)}")
        
        # Tampilkan hasil jika ada
        if 'upload_results' in st.session_state:
            results = st.session_state['upload_results']
            
            st.markdown("---")
            
            # Statistik
            st.header("📈 Hasil Deteksi")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-box" style="color: black;">
                    <h2 style="color: black;">{results['total_slots']}</h2>
                    <p>Total Slot</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-box" style="background-color: #ffcdd2; color: black;">
                    <h2 style="color: black;">{results['occupied_slots']}</h2>
                    <p>Slot Terisi</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-box" style="background-color: #c8e6c9; color: black;">
                    <h2 style="color: black;">{results['empty_slots']}</h2>
                    <p>Slot Kosong</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-box" style="color: black;">
                    <h2 style="color: black;">{results['motor_count']}</h2>
                    <p>Motor Terdeteksi</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detail per slot
            st.markdown("### 🅿️ Status Per Slot:")
            cols = st.columns(4)
            for idx, status in enumerate(results['slot_results']):
                with cols[idx]:
                    if status == "Occupied":
                        st.error(f"**Slot {idx+1}:** {status}")
                    else:
                        st.success(f"**Slot {idx+1}:** {status}")
            
            st.markdown("---")
            
            # Tampilkan semua tahapan
            display_process_steps(results)


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><b>Dashboard Deteksi Area Parkir Motor</b></p>
    <p>Kelompok AFEnter - Pengolahan Citra Digital</p>
    <p>Institut Teknologi Sumatera (ITERA) © 2025</p>
</div>
""", unsafe_allow_html=True)
