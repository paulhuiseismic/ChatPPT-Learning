@echo off
echo Installing PyTorch (CPU version - fast and reliable)...
echo.
call .\.venv\Scripts\python.exe -m pip install torch torchvision
echo.
echo Testing installation...
call .\.venv\Scripts\python.exe -c "import torch; print('SUCCESS: PyTorch', torch.__version__, 'installed')"
echo.
echo Done! You can now run: python src\minicpm_v_model.py images\forecast.png
pause

