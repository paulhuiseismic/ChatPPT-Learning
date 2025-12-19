# Quick Fix for "CUDA error: no kernel image is available"

## Your GPU
- **Model**: NVIDIA RTX PRO 3000 Blackwell Generation
- **CUDA Capability**: sm_120 (Blackwell architecture)
- **Issue**: Standard PyTorch doesn't support Blackwell yet

## Quick Solution

Run this command to install PyTorch nightly with Blackwell support:

```powershell
.\.venv\Scripts\python.exe -m pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
```

Or run the automated script:
```powershell
.\install_pytorch_blackwell.bat
```

## What This Does

1. Installs PyTorch nightly build (development version)
2. Includes support for CUDA 12.4+ and Blackwell architecture (sm_120)
3. Upgrades bitsandbytes for better compatibility

## Verification

After installation, run:
```powershell
python check_gpu_compatibility.py
```

This will show if your GPU is now supported.

## Alternative: CPU Mode

If you don't want to wait for the large download, the script will automatically fall back to CPU mode. It will be slower but will work.

Just run:
```powershell
python src\minicpm_v_model.py images\forecast.png
```

The script will detect the GPU issue and use CPU instead.

## Need Help?

See `docs/BLACKWELL_GPU_SETUP.md` for detailed troubleshooting.

