@echo off
echo ============================================
echo Installing PyTorch for Blackwell GPU (sm_120)
echo ============================================
echo.

echo Your GPU: NVIDIA RTX PRO 3000 Blackwell Generation
echo CUDA Capability: sm_120
echo.

echo Step 1: Uninstalling old PyTorch...
call .\.venv\Scripts\python.exe -m pip uninstall -y torch torchvision torchaudio
echo.

echo Step 2: Trying PyTorch nightly with CUDA 12.4 support...
echo (This may take several minutes, file size is ~2.5GB)
call .\.venv\Scripts\python.exe -m pip install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cu124
if errorlevel 1 (
    echo.
    echo Nightly build failed, trying CUDA 12.1 stable...
    call .\.venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
)
echo.

echo Step 3: Upgrading bitsandbytes to latest version...
call .\.venv\Scripts\python.exe -m pip install --upgrade bitsandbytes
echo.

echo Step 4: Verifying installation...
call .\.venv\Scripts\python.exe -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda if torch.cuda.is_available() else 'N/A'); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
if errorlevel 1 (
    echo.
    echo ERROR: PyTorch installation verification failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo.

echo Step 5: Testing bitsandbytes...
call .\.venv\Scripts\python.exe -c "import bitsandbytes; print('bitsandbytes version:', bitsandbytes.__version__)"
echo.

echo ============================================
echo Installation complete!
echo ============================================
echo.
echo NOTE: Your Blackwell GPU (sm_120) may still show compatibility warnings.
echo The model will automatically fall back to CPU mode if needed.
echo.
echo You can now run: python src\minicpm_v_model.py images\forecast.png
echo.
pause

