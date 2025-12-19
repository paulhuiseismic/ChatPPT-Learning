@echo off
echo ============================================
echo Fixing CUDA and bitsandbytes setup
echo ============================================
echo.

echo Step 1: Checking current PyTorch installation...
.\.venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
echo.

echo Step 2: Uninstalling current PyTorch (CPU version)...
.\.venv\Scripts\python.exe -m pip uninstall -y torch torchvision torchaudio
echo.

echo Step 3: Installing PyTorch with CUDA 12.1 support...
.\.venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
echo.

echo Step 4: Upgrading bitsandbytes to latest version with GPU support...
.\.venv\Scripts\python.exe -m pip install --upgrade bitsandbytes
echo.

echo Step 5: Verifying CUDA is now available...
.\.venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); import bitsandbytes; print('bitsandbytes:', bitsandbytes.__version__)"
echo.

echo ============================================
echo Setup complete!
echo ============================================
pause

