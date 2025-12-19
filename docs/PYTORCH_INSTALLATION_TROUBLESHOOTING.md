# PyTorch Installation Troubleshooting

## Issue: PyTorch Installation Failed

### Error Messages
```
ERROR: Could not find a version that satisfies the requirement torchaudio
ERROR: No matching distribution found for torchaudio
PyTorch not installed: No module named 'torch'
```

## Root Cause
1. PyTorch nightly builds may not include torchaudio for Windows
2. Network connection issues during large downloads
3. Index URL conflicts

## Solutions (Try in Order)

### Solution 1: Install Without torchaudio (RECOMMENDED)
```powershell
.\.venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Why this works**: torchaudio is optional for vision models like MiniCPM-V

### Solution 2: Use the Simple Installation Script
```powershell
.\install_pytorch_simple.bat
```

### Solution 3: Install from Default PyPI (Smaller Download)
```powershell
.\.venv\Scripts\Activate.ps1
pip install torch torchvision
```

**Note**: This installs CPU-only version, but the model will still work (just slower)

### Solution 4: Manual Step-by-Step Installation
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Uninstall any existing PyTorch
pip uninstall -y torch torchvision torchaudio

# Install PyTorch with CUDA 12.1
pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121

# Verify installation
python -c "import torch; print('PyTorch:', torch.__version__)"
```

### Solution 5: CPU-Only Version (Fastest to Install)
```powershell
.\.venv\Scripts\Activate.ps1
pip install torch torchvision
```

This installs the CPU-only version (~200MB vs ~2.5GB for CUDA version).

## Verification

After installation, verify PyTorch is working:

```powershell
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
```

Expected output:
```
PyTorch version: 2.5.1+cu121  (or similar)
CUDA available: True or False
```

## What to Do After Installation

### If CUDA is available (True):
Your GPU will be used, but may fall back to CPU due to Blackwell compatibility.

### If CUDA is NOT available (False):
The model will run on CPU automatically. This is okay - slower but functional.

## Running the Model

After PyTorch is installed (with or without CUDA), run:
```powershell
python src\minicpm_v_model.py images\forecast.png
```

The script will:
1. ✓ Detect if CUDA is available
2. ✓ Try GPU first (if available)
3. ✓ Fall back to CPU if GPU fails
4. ✓ Show clear status messages

## Common Issues

### Issue: "No module named 'torch'"
**Solution**: PyTorch installation didn't complete. Try Solution 3 or 5 above.

### Issue: "Connection timed out"
**Solution**: 
- Use a more stable network connection
- Try installing during off-peak hours
- Use CPU-only version (Solution 5) first to get running

### Issue: "CUDA error: no kernel image"
**Solution**: This is the Blackwell GPU issue. The script now handles this automatically with CPU fallback.

## Network Issues During Download

If downloads keep timing out:

1. **Increase timeout**:
   ```powershell
   pip install --timeout 300 torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

2. **Use a download accelerator**: Download the .whl file manually from https://download.pytorch.org/whl/cu121/ then:
   ```powershell
   pip install path\to\downloaded\torch-*.whl
   ```

3. **Split the installation**:
   ```powershell
   pip install torch --index-url https://download.pytorch.org/whl/cu121
   pip install torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

## Quick Test

To test if everything is working:

```powershell
python check_gpu_compatibility.py
```

This will show your complete setup status.

## Bottom Line

**You don't need the perfect PyTorch installation!**

- ✓ CPU-only PyTorch will work (just slower)
- ✓ CUDA PyTorch with Blackwell incompatibility will fall back to CPU
- ✓ The script handles all edge cases automatically

**Just get PyTorch installed (any version), and the model will work!**

## Recommended Quick Fix

Run this now to get started immediately:
```powershell
.\.venv\Scripts\Activate.ps1
pip install torch torchvision
python src\minicpm_v_model.py images\forecast.png
```

CPU mode works fine for testing! You can optimize later.

