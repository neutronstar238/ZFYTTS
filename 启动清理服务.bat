@echo off
chcp 65001 >nul
echo ========================================
echo   自动清理服务
echo ========================================
echo.
echo 此服务将自动清理 outputs 目录下
echo 超过 1 天的音频文件
echo.
echo 按 Ctrl+C 可以停止服务
echo.
pause

.venv\Scripts\python.exe cleanup_outputs.py --service

pause
