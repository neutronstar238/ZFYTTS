@echo off
chcp 65001 >nul
echo ========================================
echo   庄方宜 TTS 语音合成系统
echo ========================================
echo.
echo 请选择运行模式：
echo 1. 命令行模式
echo 2. Web 界面模式
echo 3. 退出
echo.
set /p choice=请输入选项 (1-3): 

if "%choice%"=="1" goto cli
if "%choice%"=="2" goto web
if "%choice%"=="3" goto end

:cli
echo.
echo 启动命令行模式...
echo.
set /p text=请输入要合成的文本: 
.venv\Scripts\python.exe simple_tts.py "%text%"
pause
goto end

:web
echo.
echo 启动 Web 服务器...
echo 浏览器将自动打开 http://localhost:8080
echo.
start http://localhost:8080
.venv\Scripts\python.exe web_server.py
goto end

:end
