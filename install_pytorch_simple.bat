@echo off
echo ============================================
echo Simple PyTorch Installation (CUDA 12.1)
echo ============================================
echo.
echo This installs stable PyTorch with CUDA 12.1 support.
echo Your Blackwell GPU may not be fully supported, but CPU fallback will work.
echo.

echo Step 1: Uninstalling old PyTorch...
call .\.venv\Scripts\python.exe -m pip uninstall -y torch torchvision torchaudio
echo.

echo Step 2: Installing PyTorch with CUDA 12.1...
call .\.venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
echo.

echo Step 3: Upgrading bitsandbytes...
call .\.venv\Scripts\python.exe -m pip install --upgrade bitsandbytes
echo.

echo Step 4: Verifying installation...
call .\.venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"
echo.

echo ============================================
echo Installation complete!
echo ============================================
echo.
echo Your model will run with CPU fallback (GPU may not be fully supported).
echo Run: python src\minicpm_v_model.py images\forecast.png
echo.
pause

