"""
Modul untuk pemrosesan citra parkir motor
Kelompok: AFEnter
"""

import cv2
import numpy as np
from rembg import remove
from typing import Tuple, List, Dict
import io
import time


def remove_background(image_bytes: bytes) -> np.ndarray:
    """
    Menghapus background dari gambar menggunakan rembg
    
    Args:
        image_bytes: Bytes dari gambar input
        
    Returns:
        np.ndarray: Gambar tanpa background
    """
    from PIL import Image as PILImage
    
    nobg_result = remove(image_bytes)
    
    # Convert result to bytes if it's not already
    if isinstance(nobg_result, bytes):
        nobg_bytes = nobg_result
    elif isinstance(nobg_result, PILImage.Image):
        # Handle PIL Image from rembg
        buf = io.BytesIO()
        nobg_result.save(buf, format='PNG')
        nobg_bytes = buf.getvalue()
    elif isinstance(nobg_result, np.ndarray):
        # Handle ndarray
        _, encoded = cv2.imencode('.png', nobg_result)
        nobg_bytes = encoded.tobytes()
    else:
        # Fallback - try to get bytes
        nobg_bytes = bytes(nobg_result)
    
    nparr = np.frombuffer(nobg_bytes, np.uint8)
    img_nobg = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_nobg is None:
        raise ValueError("Failed to decode image after background removal")
    return img_nobg


def resize_image(image: np.ndarray, width: int = 960, height: int = 540) -> np.ndarray:
    """
    Resize gambar ke ukuran yang ditentukan
    
    Args:
        image: Gambar input
        width: Lebar target
        height: Tinggi target
        
    Returns:
        np.ndarray: Gambar yang sudah di-resize
    """
    return cv2.resize(image, (width, height))


def preprocess_image(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Melakukan preprocessing: grayscale dan gaussian blur
    
    Args:
        image: Gambar input (BGR)
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: (grayscale, blur)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray, gray_blur


def apply_threshold(gray_blur: np.ndarray) -> np.ndarray:
    """
    Menerapkan Otsu thresholding
    
    Args:
        gray_blur: Gambar grayscale yang sudah di-blur
        
    Returns:
        np.ndarray: Binary image hasil threshold
    """
    _, thresh = cv2.threshold(
        gray_blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresh


def apply_morphology(thresh: np.ndarray) -> np.ndarray:
    """
    Menerapkan operasi morfologi (closing + opening)
    
    Args:
        thresh: Binary image hasil threshold
        
    Returns:
        np.ndarray: Image setelah operasi morfologi
    """
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=1)
    return opening


def apply_distance_transform(opening: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Menerapkan distance transform dan menghasilkan sure foreground
    
    Args:
        opening: Image hasil morfologi
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: (distance_transform_normalized, sure_foreground)
    """
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    dist_norm = np.zeros_like(dist_transform, dtype=np.float32)
    cv2.normalize(dist_transform, dist_norm, 0, 1.0, cv2.NORM_MINMAX)
    
    _, sure_fg_result = cv2.threshold(
        dist_transform,
        0.3 * dist_transform.max(),
        255, 0
    )
    sure_fg = np.uint8(sure_fg_result)
    
    return dist_norm, np.array(sure_fg, dtype=np.uint8)


def extract_roi(sure_fg: np.ndarray, roi_percentage: float = 0.35) -> Tuple[np.ndarray, int]:
    """
    Mengekstrak Region of Interest (ROI) - area parkir
    
    Args:
        sure_fg: Sure foreground image
        roi_percentage: Persentase dari atas yang diabaikan
        
    Returns:
        Tuple[np.ndarray, int]: (ROI motor, y_start ROI)
    """
    h, w = sure_fg.shape
    roi_y_start = int(h * roi_percentage)
    roi_motor = sure_fg[roi_y_start:h, :]
    return roi_motor, roi_y_start


def detect_motor_contours(roi_motor: np.ndarray, 
                         roi_y_start: int,
                         min_area: int = 300,
                         max_area: int = 250000) -> List[Tuple[int, int, int, int]]:
    """
    Mendeteksi kontur motor dan menghasilkan bounding boxes
    
    Args:
        roi_motor: ROI yang berisi area parkir
        roi_y_start: Offset Y dari ROI
        min_area: Luas minimum kontur yang dianggap motor
        max_area: Luas maksimum kontur yang dianggap motor
        
    Returns:
        List[Tuple[int, int, int, int]]: List of (x, y, width, height) bounding boxes
    """
    contours, _ = cv2.findContours(
        roi_motor, 
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    motor_boxes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            x, y, wb, hb = cv2.boundingRect(cnt)
            motor_boxes.append((x, y + roi_y_start, wb, hb))
    
    return motor_boxes


def create_parking_slots(image: np.ndarray,
                        motor_boxes: List[Tuple[int, int, int, int]],
                        roi_y_start: int,
                        slot_count: int = 4) -> Tuple[np.ndarray, List[str]]:
    """
    Membuat grid slot parkir dan mendeteksi occupancy
    
    Args:
        image: Gambar original untuk digambar
        motor_boxes: List bounding boxes motor
        roi_y_start: Y start dari ROI
        slot_count: Jumlah slot parkir
        
    Returns:
        Tuple[np.ndarray, List[str]]: (Image dengan grid, status setiap slot)
    """
    h, w = image.shape[:2]
    slot_width = w // slot_count
    
    output_grid = image.copy()
    slot_results = []
    
    for i in range(slot_count):
        sx = i * slot_width
        sy = roi_y_start
        ex = sx + slot_width
        ey = h
        
        # Cek apakah ada motor dalam slot ini
        occupied = False
        for (mx, my, mw, mh) in motor_boxes:
            if mx < ex and mx + mw > sx:
                occupied = True
                break
        
        color = (0, 0, 255) if occupied else (0, 255, 0)
        status = "Occupied" if occupied else "Empty"
        slot_results.append(status)
        
        # Gambar rectangle dan text
        cv2.rectangle(output_grid, (sx, sy), (ex, ey), color, 3)
        cv2.putText(
            output_grid, 
            status, 
            (sx + 5, sy + 25),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            color, 
            2
        )
    
    return output_grid, slot_results


def process_parking_image(image_bytes: bytes) -> dict:
    """
    Fungsi utama untuk memproses gambar parkir secara lengkap
    menggunakan pendekatan rule-based untuk mendeteksi slot parkir.
    
    Args:
        image_bytes: Bytes dari gambar input
        
    Returns:
        dict: Dictionary berisi semua hasil pemrosesan dan statistik
    """
    # Start timing
    start_time = time.time()
    timing_metrics = {}
    
    # 1. Baca dan resize gambar asli
    t0 = time.time()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_original = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_original is None:
        raise ValueError("Failed to decode input image")
    img_original = resize_image(img_original)
    timing_metrics['load_resize'] = round((time.time() - t0) * 1000, 2)
    
    # 2. Remove background
    t0 = time.time()
    img_nobg = remove_background(image_bytes)
    img_nobg = resize_image(img_nobg)
    timing_metrics['background_removal'] = round((time.time() - t0) * 1000, 2)
    
    # 3. Preprocessing
    t0 = time.time()
    gray, gray_blur = preprocess_image(img_nobg)
    timing_metrics['preprocessing'] = round((time.time() - t0) * 1000, 2)
    
    # 4. Threshold
    t0 = time.time()
    thresh = apply_threshold(gray_blur)
    timing_metrics['thresholding'] = round((time.time() - t0) * 1000, 2)
    
    # 5. Morfologi
    t0 = time.time()
    opening = apply_morphology(thresh)
    timing_metrics['morphology'] = round((time.time() - t0) * 1000, 2)
    
    # 6. Distance Transform
    t0 = time.time()
    dist_norm, sure_fg = apply_distance_transform(opening)
    timing_metrics['distance_transform'] = round((time.time() - t0) * 1000, 2)
    
    # 7. Extract ROI
    t0 = time.time()
    roi_motor, roi_y_start = extract_roi(sure_fg)
    timing_metrics['roi_extraction'] = round((time.time() - t0) * 1000, 2)
    
    # 8. Deteksi kontur dalam ROI
    t0 = time.time()
    motor_boxes = detect_motor_contours(roi_motor, roi_y_start)
    timing_metrics['contour_detection'] = round((time.time() - t0) * 1000, 2)
    
    # 9. Create parking slots (4 slot untuk 4 motor)
    t0 = time.time()
    output_grid, slot_results = create_parking_slots(
        img_original, 
        motor_boxes, 
        roi_y_start
    )
    timing_metrics['slot_creation'] = round((time.time() - t0) * 1000, 2)
    
    # Total processing time
    total_time = round((time.time() - start_time) * 1000, 2)
    timing_metrics['total'] = total_time
    
    # Hitung statistik dasar
    total_slots = len(slot_results)
    occupied_slots = sum(1 for s in slot_results if s == "Occupied")
    empty_slots = total_slots - occupied_slots
    
    # === EVALUASI: Occupancy Rate ===
    # Metrik utama untuk mengevaluasi hasil deteksi slot parkir
    occupancy_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
    
    return {
        'original': img_original,
        'no_background': img_nobg,
        'grayscale': gray,
        'gaussian_blur': gray_blur,
        'threshold': thresh,
        'morphology': opening,
        'distance_transform': dist_norm,
        'sure_foreground': sure_fg,
        'final_output': output_grid,
        'slot_results': slot_results,
        'total_slots': total_slots,
        'occupied_slots': occupied_slots,
        'empty_slots': empty_slots,
        # Evaluation Metrics - Simplified (Occupancy Rate only)
        'evaluation': {
            'timing': timing_metrics,
            'occupancy_rate': round(occupancy_rate, 2)
        }
    }
