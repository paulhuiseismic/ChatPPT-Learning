# Fixing CUDA Compatibility for Blackwell GPU (sm_120)

## Problem
Your NVIDIA RTX PRO 3000 Blackwell Generation GPU has CUDA capability **sm_120**, which is not supported by standard PyTorch releases. The current stable PyTorch only supports up to sm_90.

## Error Message
```
CUDA error: no kernel image is available for execution on the device
```

This happens because PyTorch doesn't have compiled kernels for your GPU architecture.

## Solution

### Option 1: Install PyTorch Nightly (Recommended)
PyTorch nightly builds include support for newer GPU architectures like Blackwell.

**Run the installation script:**
```powershell
.\install_pytorch_blackwell.bat
```

**Or manually install:**
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Uninstall old PyTorch
pip uninstall -y torch torchvision torchaudio

# Install PyTorch nightly with CUDA 12.4
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

# Upgrade bitsandbytes
pip install --upgrade bitsandbytes
```

### Option 2: Use CPU Fallback (Already Implemented)
The `minicpm_v_model.py` script now automatically falls back to CPU if GPU loading fails. This will work but be slower.

### Option 3: Use PyTorch with CUDA 12.6+ (Future)
Wait for official PyTorch 2.6+ stable release with Blackwell support.

## Verification

After installation, verify that PyTorch recognizes your GPU:

```powershell
.\.venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); print('Supported archs:', torch.cuda.get_arch_list() if torch.cuda.is_available() else 'N/A')"
```

You should see your GPU listed and sm_120 in the supported architectures.

## Testing the Model

Once installed, run:
```powershell
python src\minicpm_v_model.py images\forecast.png
```

## Important Notes

1. **PyTorch Nightly** is a development version and may have bugs
2. **Large Download**: PyTorch with CUDA is ~2.5GB
3. **CPU Fallback**: If GPU loading still fails, the script will automatically use CPU
4. **Memory Requirements**: The model requires significant RAM (8GB+) when running on CPU

## Troubleshooting

### If nightly build doesn't work:
1. Check NVIDIA driver version: `nvidia-smi`
2. Update to latest NVIDIA driver from [NVIDIA website](https://www.nvidia.com/Download/index.aspx)
3. Ensure CUDA 12.4+ is installed on your system

### If download is too slow:
1. Try a different network connection
2. Download from a closer mirror
3. Consider using the CPU fallback for now

### Alternative: WSL2
If Windows installation continues to have issues, consider using WSL2 (Windows Subsystem for Linux) which sometimes has better compatibility with cutting-edge hardware.

## Updated Requirements

The `requirements.txt` now includes a note about PyTorch nightly for Blackwell GPUs.

For automatic installation of all dependencies including PyTorch nightly:
```powershell
# For Blackwell GPUs
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
pip install -r requirements.txt
```

