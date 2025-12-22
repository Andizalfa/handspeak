# BISINDO Sign Language Recognition Model

Model untuk mengenali 50 gerakan Bahasa Isyarat Indonesia (BISINDO) menggunakan LSTM dan MediaPipe Hand Landmarks.

## Model Information

- **Architecture**: LSTM (Long Short-Term Memory)
- **Input**: Sequence of 30 frames, each with 126 features (21 landmarks × 2 hands × 3 coordinates)
- **Output**: 50 BISINDO gesture classes
- **Framework**: TensorFlow/Keras
- **Format**: HDF5 (.h5)

## Labels

Model dapat mengenali 50 kata BISINDO:
- Huruf: A-Z
- Kata umum: Aku, Kamu, Dia, Apa, Dimana, Kapan, Siapa, dll.

Lihat `labels.json` untuk daftar lengkap.

## Usage

### Download Model

```python
from huggingface_hub import hf_hub_download

# Download model
model_path = hf_hub_download(
    repo_id="USERNAME/bisindo-model",
    filename="bisindo_best.h5"
)

# Download labels
labels_path = hf_hub_download(
    repo_id="USERNAME/bisindo-model",
    filename="labels.json"
)
```

### Load and Predict

```python
import tensorflow as tf
import json
import numpy as np

# Load model
model = tf.keras.models.load_model(model_path)

# Load labels
with open(labels_path, "r") as f:
    labels = json.load(f)

# Prepare input: shape (1, 30, 126)
# sequence = your_hand_landmarks_sequence
# sequence = np.expand_dims(sequence, axis=0)

# Predict
predictions = model.predict(sequence)
predicted_class = np.argmax(predictions[0])
predicted_label = labels[predicted_class]
confidence = predictions[0][predicted_class]

print(f"Predicted: {predicted_label} ({confidence:.2%})")
```

## Training Details

- **Dataset**: Custom BISINDO video dataset
- **Sequence Length**: 30 frames per gesture
- **Hand Detection**: MediaPipe Hands
- **Features**: Normalized 3D landmarks (x, y, z)
- **Training**: LSTM with dropout and regularization

## Model Architecture

```
Input (30, 126)
    ↓
LSTM (128 units)
    ↓
Dropout (0.3)
    ↓
LSTM (64 units)
    ↓
Dropout (0.3)
    ↓
Dense (50 units, softmax)
```

## Performance

- **Training Accuracy**: ~95%
- **Validation Accuracy**: ~92%
- **Inference Speed**: ~50ms per prediction (CPU)

## Citation

If you use this model, please cite:

```bibtex
@misc{bisindo-model-2025,
  title={BISINDO Sign Language Recognition using LSTM},
  author={Your Name},
  year={2025},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/USERNAME/bisindo-model}}
}
```

## License

MIT License

## Contact

For questions or issues, please open an issue in the repository or contact: your-email@example.com
