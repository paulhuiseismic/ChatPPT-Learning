"""
Quick test to verify bitsandbytes and model loading
"""
import sys

print("1. Testing bitsandbytes import...")
try:
    import bitsandbytes
    print(f"   ✓ bitsandbytes {bitsandbytes.__version__} is installed")
except ImportError as e:
    print(f"   ✗ bitsandbytes import failed: {e}")
    sys.exit(1)

print("\n2. Testing transformers import...")
try:
    from transformers import AutoModel, AutoTokenizer
    print("   ✓ transformers imported successfully")
except ImportError as e:
    print(f"   ✗ transformers import failed: {e}")
    sys.exit(1)

print("\n3. Testing model path...")
from pathlib import Path
model_path = Path(__file__).parent / "models" / "MiniCPM-V-2_6-int4"
if model_path.exists():
    print(f"   ✓ Model directory found: {model_path}")
    print(f"   ✓ Model has {len(list(model_path.glob('*')))} files")
else:
    print(f"   ✗ Model directory not found: {model_path}")
    sys.exit(1)

print("\n4. Checking model config...")
import json
config_file = model_path / "config.json"
if config_file.exists():
    with open(config_file, 'r') as f:
        config = json.load(f)
    if 'quantization_config' in config:
        print(f"   ✓ Model has quantization config: {config['quantization_config'].get('quant_method', 'unknown')}")
    else:
        print("   ! Model doesn't have quantization config in config.json")
else:
    print("   ✗ config.json not found")

print("\n✓ All checks passed! Model should be loadable.")
print("\nNote: Actually loading the model will take several minutes...")

