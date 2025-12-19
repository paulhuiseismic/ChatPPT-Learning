from PIL import Image
from transformers import AutoModel, AutoTokenizer
from pathlib import Path
import sys


# Get the absolute path to the model directory
current_dir = Path(__file__).parent
model_path = (current_dir.parent / "models" / "MiniCPM-V-2_6-int4").resolve()

print(f"Loading model from: {model_path}")

# Check if bitsandbytes is available
try:
    import bitsandbytes
    print(f"bitsandbytes version {bitsandbytes.__version__} is available")
    HAS_BITSANDBYTES = True
except ImportError:
    print("ERROR: bitsandbytes not found!")
    print("This quantized model requires bitsandbytes to run.")
    print("Please install it with: pip install bitsandbytes")
    sys.exit(1)

try:
    # Check PyTorch CUDA compatibility
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")

    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        gpu_capability = torch.cuda.get_device_capability(0)
        print(f"GPU compute capability: sm_{gpu_capability[0]}{gpu_capability[1]}")

    # Load model with quantization using bitsandbytes
    print("Loading quantized model (this may take a few minutes)...")

    try:
        # Try GPU first
        model = AutoModel.from_pretrained(
            str(model_path),
            trust_remote_code=True,
            device_map="auto"  # Automatically distribute the model across available devices
        )
        print("✓ Model loaded on GPU successfully!")
    except Exception as gpu_error:
        print(f"\n⚠ GPU loading failed: {gpu_error}")
        print("\nAttempting to load on CPU (this will be slower and use more RAM)...")

        # Fallback to CPU
        model = AutoModel.from_pretrained(
            str(model_path),
            trust_remote_code=True,
            device_map="cpu",
            torch_dtype=torch.float32
        )
        print("✓ Model loaded on CPU successfully!")

    tokenizer = AutoTokenizer.from_pretrained(str(model_path), trust_remote_code=True)
    model.eval()

except Exception as e:
    print(f"\n❌ ERROR: Failed to load model: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. GPU Compatibility Issue:")
    print("   - Your GPU may be too new for the current PyTorch version")
    print("   - Install PyTorch nightly: pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu124")
    print("2. Check if bitsandbytes is properly installed: pip install bitsandbytes")
    print("3. Ensure you have enough RAM (model requires ~8GB+ RAM)")
    sys.exit(1)

def chat_with_image(image_file, question='请描述这张图片', sampling=False, temperature=0.2, stream=False):
    image = Image.open(image_file).convert("RGB")

    msgs = [{'role': 'user', 'content': [image, question]}]

    if not stream:
        return model.chat(image=None, msgs=msgs, tokenizer=tokenizer, temperature=temperature)
    else:
        generated_text = ""
        for new_text in model.chat(image=None, msgs=msgs, tokenizer=tokenizer, sampling=sampling, temperature=temperature, stream=True):
            generated_text += new_text
            print(new_text, flush=True, end='')
        return generated_text


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python src/minicpm_v_model.py <image_file>")
        sys.exit(1)

    image_file = sys.argv[1]
    question = "what is in the image?"
    response = chat_with_image(image_file, question, sampling=True, temperature=0.7, stream=True)
    print("\nFinal Response:", response)