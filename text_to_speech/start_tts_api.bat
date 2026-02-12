@echo off
chcp 65001 >nul
echo ========================================
echo   启动 TTS REST API 服务器
echo ========================================
echo.

cd /d "%~dp0"

if exist .venv\Scripts\activate.bat (
    echo 激活虚拟环境...
    call .venv\Scripts\activate.bat
) else (
    echo 警告: 未找到虚拟环境，使用全局 Python
)

echo.
echo 启动 API 服务器...
python tts_api.py --host 0.0.0.0 --port 5001

pause
