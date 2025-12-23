"""
Test script untuk download model dari Hugging Face
"""

import os
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GANTI dengan repository Anda di .env!
HF_REPO_ID = os.getenv("HF_REPO_ID", "USERNAME/REPO_NAME")  # Format: username/repo-name

def test_download():
    print("="*60)
    print("🧪 Testing Hugging Face Model Download")
    print("="*60)
    print(f"Repository: {HF_REPO_ID}")
    print()
    
    try:
        # Test download model
        print("📥 Downloading bisindo_best.h5...")
        model_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="bisindo_best.h5",
            cache_dir="./test_cache"
        )
        print(f"✅ Model downloaded: {model_path}")
        
        # Check file size
        file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"📊 File size: {file_size:.2f} MB")
        print()
        
        # Test download labels
        print("📥 Downloading labels.json...")
        labels_path = hf_hub_download(
            repo_id=HF_REPO_ID,
            filename="labels.json",
            cache_dir="./test_cache"
        )
        print(f"✅ Labels downloaded: {labels_path}")
        
        # Read labels
        import json
        with open(labels_path, "r") as f:
            labels = json.load(f)
        print(f"📊 Number of labels: {len(labels)}")
        print(f"📝 Labels: {labels[:5]}...")  # First 5 labels
        print()
        
        print("="*60)
        print("✅ All downloads successful!")
        print("="*60)
        print()
        print("Next steps:")
        print("1. Update HF_REPO_ID in backend_ml/main.py")
        print("2. Run: python main.py")
        print("3. Model will auto-download on startup")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check repository ID is correct (format: username/repo-name)")
        print("2. Make sure repository is public or you have access")
        print("3. Verify files exist in the repository")
        print("4. Check internet connection")

if __name__ == "__main__":
    test_download()
