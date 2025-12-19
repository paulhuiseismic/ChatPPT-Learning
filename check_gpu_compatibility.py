"""
Quick verification script for PyTorch and GPU compatibility
"""
import sys

print("=" * 60)
print("GPU Compatibility Check")
print("=" * 60)

# Check PyTorch
print("\n1. Checking PyTorch...")
try:
    import torch
    print(f"   ✓ PyTorch version: {torch.__version__}")
except ImportError as e:
    print(f"   ✗ PyTorch not installed: {e}")
    sys.exit(1)

# Check CUDA availability
print("\n2. Checking CUDA...")
if torch.cuda.is_available():
    print(f"   ✓ CUDA is available")
    print(f"   ✓ CUDA version: {torch.version.cuda}")
    print(f"   ✓ Number of GPUs: {torch.cuda.device_count()}")
else:
    print(f"   ✗ CUDA is NOT available")
    print(f"   ! Model will run on CPU (slower)")

# Check GPU details
if torch.cuda.is_available():
    print("\n3. GPU Information...")
    for i in range(torch.cuda.device_count()):
        print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
        capability = torch.cuda.get_device_capability(i)
        print(f"   Compute Capability: sm_{capability[0]}{capability[1]}")
        print(f"   Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")

# Check supported architectures
print("\n4. Supported CUDA Architectures...")
if torch.cuda.is_available():
    arch_list = torch.cuda.get_arch_list()
    print(f"   Supported: {', '.join(arch_list)}")

    # Check if Blackwell (sm_120) is supported
    if 'sm_120' in ' '.join(arch_list) or 'compute_120' in ' '.join(arch_list):
        print(f"   ✓ Blackwell architecture (sm_120) is SUPPORTED")
    else:
        print(f"   ⚠ Blackwell architecture (sm_120) is NOT listed")
        print(f"   ! You may encounter 'no kernel image' errors")
        print(f"   ! Consider installing PyTorch nightly build")
else:
    print("   N/A (CUDA not available)")

# Check bitsandbytes
print("\n5. Checking bitsandbytes...")
try:
    import bitsandbytes
    print(f"   ✓ bitsandbytes version: {bitsandbytes.__version__}")
except ImportError as e:
    print(f"   ✗ bitsandbytes not installed: {e}")

# Check transformers
print("\n6. Checking transformers...")
try:
    import transformers
    print(f"   ✓ transformers version: {transformers.__version__}")
except ImportError as e:
    print(f"   ✗ transformers not installed: {e}")

# Final recommendation
print("\n" + "=" * 60)
print("RECOMMENDATION")
print("=" * 60)

if torch.cuda.is_available():
    capability = torch.cuda.get_device_capability(0)
    arch_str = f"sm_{capability[0]}{capability[1]}"
    arch_list = torch.cuda.get_arch_list()

    if arch_str in ' '.join(arch_list) or f"compute_{capability[0]}{capability[1]}" in ' '.join(arch_list):
        print("✓ Your GPU is fully supported!")
        print("  You can run the model with GPU acceleration.")
    else:
        print("⚠ Your GPU may not be fully supported.")
        print(f"  Your GPU: {arch_str}")
        print(f"  Supported: {', '.join(arch_list[:5])}...")
        print("\nOptions:")
        print("1. Install PyTorch nightly:")
        print("   pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu124")
        print("2. Use CPU mode (slower but will work)")
else:
    print("! CUDA is not available.")
    print("  The model will run on CPU (much slower).")
    print("\nTo enable GPU:")
    print("1. Install NVIDIA drivers")
    print("2. Install PyTorch with CUDA:")
    print("   pip install torch --index-url https://download.pytorch.org/whl/cu121")

print("=" * 60)

