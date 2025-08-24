@echo off
echo ========================================
echo    Heater Monitor System - Optimized
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8-3.13 and add to PATH
    pause
    exit /b 1
)

echo ✅ Python detected
python --version

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo ✅ Virtual environment created
)

REM Check and install dependencies
echo.
echo 🔍 Checking dependencies...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Installing dependencies...
    pip install -r requirements.txt
) else (
    echo ✅ Dependencies are installed
)

REM Run performance check
echo.
echo 🔧 Running performance check...
python -c "
import psutil
import sys
memory = psutil.virtual_memory()
print(f'💾 Available Memory: {memory.available / (1024**3):.1f} GB')
print(f'⚡ CPU Cores: {psutil.cpu_count()}')
if memory.available < 2 * (1024**3):
    print('⚠️ Warning: Low memory. Performance may be affected.')
else:
    print('✅ System resources OK')
"

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Set performance environment variables
set PYTHONOPTIMIZE=1
set MATPLOTLIB_BACKEND=Qt5Agg

echo.
echo 🚀 Starting Heater Monitor System with optimizations...
echo.
echo ⭐ Performance Features Enabled:
echo   - Memory optimization
echo   - Automatic data cleanup
echo   - Chart optimization
echo   - Auto-save every 10 minutes
echo   - Continuous operation support
echo.

REM Start the application
python heater_monitor.py

echo.
echo 📊 Application closed
pause