"""
BISINDO GESTURE RECOGNITION - TRAINING WITH HAND METADATA DETECTION
Otomatis deteksi tangan dominan untuk setiap gesture dan simpan ke metadata
"""

# ============================================
# 1. INSTALL DEPENDENCIES
# ============================================
# Jalankan di cell pertama Colab:
"""
!pip install -q "tensorflow==2.17.1" mediapipe opencv-python scikit-learn h5py pandas
"""

# ============================================
# 2. IMPORTS
# ============================================
import os
import cv2
import numpy as np
import mediapipe as mp
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers
import json
import pandas as pd
from datetime import datetime
from collections import Counter

print("TensorFlow version:", tf.__version__)
print("MediaPipe version:", mp.__version__)

# ============================================
# 3. KONFIGURASI
# ============================================
DATA_DIR = "/content/drive/MyDrive/dataset_bisindo"  # Sesuaikan path Anda
SEQUENCE_LENGTH = 30
NUM_FEATURES = 126  # 21 landmarks * 2 hands * 3 coords (x,y,z)

# ============================================
# 4. MEDIAPIPE SETUP
# ============================================
mp_hands = mp.solutions.hands

# ============================================
# 5. HAND DETECTION FUNCTIONS
# ============================================

def normalize_hand_wrist_and_scale(hand_keypoints_63):
    """
    Normalisasi: wrist sebagai origin + scale normalization
    """
    if np.sum(np.abs(hand_keypoints_63)) < 1e-6:
        return hand_keypoints_63
    
    pts = hand_keypoints_63.reshape(21, 3)
    wrist = pts[0].copy()
    
    # Step 1: Wrist sebagai origin
    pts = pts - wrist
    
    # Step 2: Scale normalization
    distances = np.sqrt(np.sum(pts**2, axis=1))
    max_dist = np.max(distances)
    
    if max_dist > 1e-6:
        pts = pts / max_dist
    
    return pts.reshape(-1).astype(np.float32)

def extract_hand_keypoints_two_hands(image, hands_model):
    """
    Extract landmarks dari 2 tangan
    Return: 
      - features: [right_hand(63), left_hand(63)] = 126 features
      - hand_info: { "has_right": bool, "has_left": bool }
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands_model.process(image_rgb)

    right_hand = np.zeros(63, dtype=np.float32)
    left_hand = np.zeros(63, dtype=np.float32)
    has_right = False
    has_left = False

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness
        ):
            label = handedness.classification[0].label
            
            keypoints = []
            for lm in hand_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
            keypoints = np.array(keypoints, dtype=np.float32)
            
            # Normalisasi
            keypoints = normalize_hand_wrist_and_scale(keypoints)
            
            if label == "Right":
                right_hand = keypoints
                has_right = True
            else:
                left_hand = keypoints
                has_left = True
    
    # PENTING: Urutan RIGHT dulu, LEFT kemudian
    features = np.concatenate([right_hand, left_hand])
    hand_info = {"has_right": has_right, "has_left": has_left}
    
    return features, hand_info

def check_video_detection(video_path, show_details=False):
    """
    Check apakah video bisa di-detect MediaPipe
    Return: (success, total_frames, detected_frames, error_msg)
    """
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return (False, 0, 0, "Cannot open video")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            cap.release()
            return (False, 0, 0, "Empty video")
        
        detected_frames = 0
        
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            
            # Sample 10 frames untuk check
            sample_indices = np.linspace(0, total_frames-1, min(10, total_frames)).astype(int)
            
            for idx in sample_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue
                
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)
                
                if results.multi_hand_landmarks:
                    detected_frames += 1
        
        cap.release()
        
        detection_rate = detected_frames / len(sample_indices) if len(sample_indices) > 0 else 0
        
        if detection_rate < 0.3:  # Minimal 30% frame terdeteksi
            return (False, total_frames, detected_frames, f"Low detection rate: {detection_rate:.1%}")
        
        return (True, total_frames, detected_frames, None)
    
    except Exception as e:
        return (False, 0, 0, str(e))

def video_to_sequence_with_hand_info(video_path, sequence_length=SEQUENCE_LENGTH):
    """
    Convert video to sequence of landmarks + detect dominant hand
    Dengan validasi yang sama seperti bisindo_training_complete.py
    Return: 
      - sequence: numpy array (sequence_length, 126) atau None jika gagal
      - dominant_hand: "L", "R", or "LR"
      - detection_info: dict dengan info deteksi
    """
    # Validasi dulu sebelum proses
    success, total_frames, detected_frames, error = check_video_detection(video_path)
    if not success:
        return None, None, {
            "error": error or "Video validation failed",
            "total_frames": total_frames,
            "detected_frames": detected_frames
        }
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        return None, None, {"error": "No frames in video"}

    # Sample frames evenly
    indices = np.linspace(0, total_frames - 1, sequence_length).astype(int)
    sequence = []
    hand_patterns = []  # Track which hands detected in each frame
    frames_with_hands = 0  # Counter untuk frame yang ada tangan

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:

        frame_id = 0
        target_idx_pos = 0

        while cap.isOpened() and target_idx_pos < len(indices):
            ret, frame = cap.read()
            if not ret:
                break

            if frame_id == indices[target_idx_pos]:
                keypoints, hand_info = extract_hand_keypoints_two_hands(frame, hands)
                sequence.append(keypoints)
                
                # Track hand pattern
                pattern = ""
                if hand_info["has_right"]:
                    pattern += "R"
                if hand_info["has_left"]:
                    pattern += "L"
                
                if pattern:
                    hand_patterns.append(pattern)
                    frames_with_hands += 1
                
                target_idx_pos += 1

            frame_id += 1

    cap.release()

    # Validasi: Apakah semua frame berhasil diambil?
    if len(sequence) != sequence_length:
        return None, None, {
            "error": "Incomplete sequence",
            "expected": sequence_length,
            "got": len(sequence)
        }

    # Hitung detection ratio
    detection_ratio = frames_with_hands / sequence_length

    # Determine dominant hand pattern
    if hand_patterns:
        # Count most common pattern
        pattern_counter = Counter(hand_patterns)
        dominant_pattern = pattern_counter.most_common(1)[0][0]
        
        # Normalize to standard format
        if "R" in dominant_pattern and "L" in dominant_pattern:
            dominant_hand = "LR"
        elif "R" in dominant_pattern:
            dominant_hand = "R"
        elif "L" in dominant_pattern:
            dominant_hand = "L"
        else:
            dominant_hand = "UNKNOWN"
    else:
        dominant_hand = "UNKNOWN"

    detection_info = {
        "detection_ratio": detection_ratio,
        "frames_with_hands": frames_with_hands,
        "total_frames": sequence_length,
        "hand_patterns": dict(pattern_counter)
    }

    return np.array(sequence, dtype=np.float32), dominant_hand, detection_info

# ============================================
# 6. LOAD DATASET WITH HAND METADATA
# ============================================
print("\n" + "="*60)
print("LOADING DATASET WITH HAND METADATA DETECTION")
print("="*60)

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Directory tidak ditemukan: {DATA_DIR}")

class_names = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
print(f"📂 Ditemukan {len(class_names)} kelas: {class_names}")

X_data = []
y_data = []
gesture_hand_metadata = {}  # { "GestureName": "L/R/LR" }

failed_videos = []  # Track video yang gagal

for class_idx, class_name in enumerate(class_names):
    class_path = os.path.join(DATA_DIR, class_name)
    video_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.mp4', '.avi', '.mov'))]
    
    print(f"\n📹 Processing class: {class_name} ({len(video_files)} videos)")
    
    hand_patterns_for_class = []
    success_count = 0
    fail_count = 0
    
    for video_file in video_files:
        video_path = os.path.join(class_path, video_file)
        seq, dominant_hand, detection_info = video_to_sequence_with_hand_info(video_path)
        
        if seq is not None:
            X_data.append(seq)
            y_data.append(class_idx)
            hand_patterns_for_class.append(dominant_hand)
            success_count += 1
        else:
            fail_count += 1
            error_msg = detection_info.get("error", "Unknown error")
            failed_videos.append({
                "class": class_name,
                "video": video_file,
                "error": error_msg,
                "details": detection_info
            })
            print(f"   ❌ FAILED: {video_file}")
            print(f"      Reason: {error_msg}")
            if "detection_ratio" in detection_info:
                print(f"      Detection ratio: {detection_info['detection_ratio']:.1%} (min required: 80%)")
            if "frames_with_hands" in detection_info:
                print(f"      Frames with hands: {detection_info['frames_with_hands']}/{detection_info['total_frames']}")
    
    # Determine most common hand pattern for this gesture
    if hand_patterns_for_class:
        pattern_counter = Counter(hand_patterns_for_class)
        most_common_hand = pattern_counter.most_common(1)[0][0]
        gesture_hand_metadata[class_name] = most_common_hand
        
        print(f"   ✅ Success: {success_count}/{len(video_files)} videos")
        print(f"   🖐️  Dominant hand: {most_common_hand}")
        print(f"   📊 Hand distribution: {dict(pattern_counter)}")
        
        if fail_count > 0:
            print(f"   ⚠️  Failed: {fail_count} videos (see details above)")
    else:
        print(f"   ❌ NO VALID VIDEOS! All {len(video_files)} videos failed validation")
        
# Print summary of failed videos
if failed_videos:
    print("\n" + "="*60)
    print("⚠️  VALIDATION SUMMARY - FAILED VIDEOS")
    print("="*60)
    print(f"Total failed videos: {len(failed_videos)}")
    
    # Save to CSV for detailed analysis
    df_failed = pd.DataFrame(failed_videos)
    failed_report_path = "models/failed_videos_report.csv"
    df_failed.to_csv(failed_report_path, index=False)
    print(f"📄 Detailed report saved to: {failed_report_path}")
    
    # Group by error type
    error_counts = df_failed['error'].value_counts()
    print("\n📊 Error breakdown:")
    for error_type, count in error_counts.items():
        print(f"   - {error_type}: {count} videos")
    
    print("\n⚠️  WARNING: Some videos failed validation!")
    print("   Please check the videos and re-record if necessary.")
    print("   Training will continue with valid videos only.")
else:
    print("\n✅ All videos passed validation!")

X_data = np.array(X_data, dtype=np.float32)
y_data = np.array(y_data, dtype=np.int32)

print(f"\n" + "="*60)
print("DATASET LOADING SUMMARY")
print("="*60)
print(f"✅ Total sequences loaded: {len(X_data)}")
print(f"✅ Data shape: {X_data.shape}")
print(f"✅ Labels shape: {y_data.shape}")

# Validasi minimal: apakah ada cukup data?
if len(X_data) == 0:
    raise ValueError("❌ NO DATA LOADED! All videos failed validation. Please check your dataset.")

# Validasi per class
print(f"\n📊 Samples per class:")
for class_idx, class_name in enumerate(class_names):
    count = np.sum(y_data == class_idx)
    print(f"   {class_name}: {count} samples")
    if count < 5:
        print(f"      ⚠️  WARNING: Very few samples! Recommend at least 20 samples per class.")

# Save gesture hand metadata
metadata_path = "models/gesture_hands_metadata.json"
os.makedirs("models", exist_ok=True)
with open(metadata_path, "w") as f:
    json.dump(gesture_hand_metadata, f, indent=2)
print(f"\n💾 Gesture hand metadata saved to: {metadata_path}")
print(f"📋 Metadata content:")
for gesture, hand in gesture_hand_metadata.items():
    print(f"   {gesture}: {hand}")

# ============================================
# 7. SPLIT DATA
# ============================================
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    stratify=y_data,
    random_state=42
)

print(f"\nTrain: {X_train.shape} {y_train.shape}")
print(f"Test:  {X_test.shape} {y_test.shape}")

# ============================================
# 8. DATA AUGMENTATION
# ============================================
print("\n" + "="*60)
print("DATA AUGMENTATION")
print("="*60)

def augment_sequence(seq, n_aug=2):
    aug_list = []
    
    for _ in range(n_aug):
        aug = seq.copy()
        
        # Gaussian noise
        noise = np.random.normal(0, 0.01, seq.shape).astype(np.float32)
        aug = aug + noise
        
        # Time shift
        shift = np.random.randint(-3, 4)
        aug = np.roll(aug, shift, axis=0)
        
        # Speed variation
        if np.random.random() > 0.5:
            indices = np.sort(np.random.choice(len(aug), size=len(aug), replace=True))
            aug = aug[indices]
        
        aug_list.append(aug)
    
    return aug_list

X_train_aug = []
y_train_aug = []

for seq, label in zip(X_train, y_train):
    X_train_aug.append(seq)
    y_train_aug.append(label)
    
    aug_seqs = augment_sequence(seq, n_aug=2)
    for aug in aug_seqs:
        X_train_aug.append(aug)
        y_train_aug.append(label)

X_train = np.array(X_train_aug, dtype=np.float32)
y_train = np.array(y_train_aug, dtype=np.int32)

print(f"✅ After augmentation: {X_train.shape}")

# ============================================
# 9. BUILD MODEL
# ============================================
print("\n" + "="*60)
print("BUILDING MODEL")
print("="*60)

num_classes = len(class_names)

model = tf.keras.Sequential([
    layers.Input(shape=(SEQUENCE_LENGTH, NUM_FEATURES)),
    layers.LSTM(128, return_sequences=True),
    layers.Dropout(0.3),
    layers.LSTM(64, return_sequences=True),
    layers.Dropout(0.3),
    layers.LSTM(32),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ============================================
# 10. TRAIN MODEL
# ============================================
print("\n" + "="*60)
print("TRAINING MODEL")
print("="*60)

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=15, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint('models/bisindo_best.h5', save_best_only=True),
    tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
]

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=32,
    callbacks=callbacks,
    verbose=1
)

# ============================================
# 11. EVALUATE
# ============================================
print("\n" + "="*60)
print("EVALUATION")
print("="*60)

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss:.6f}")
print(f"Test Accuracy: {test_acc:.4f}")

# ============================================
# 12. SAVE ARTIFACTS
# ============================================
model.save("models/bisindo_best.h5")
print("✅ Model saved: models/bisindo_best.h5")

with open("models/labels.json", "w") as f:
    json.dump(class_names, f)
print("✅ Labels saved: models/labels.json")

print(f"\n✅ Gesture hand metadata already saved: {metadata_path}")
print("\n🎉 TRAINING COMPLETE!")
print("\n📋 Next steps:")
print("1. Download models/bisindo_best.h5")
print("2. Download models/labels.json")
print("3. Download models/gesture_hands_metadata.json")
print("4. Copy gesture_hands_metadata.json content to frontend gestureHands.js")
