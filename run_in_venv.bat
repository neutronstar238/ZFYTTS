@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
call .venv\Scripts\activate
echo 虚拟环境已激活，Python版本：
python --version
echo.
echo 测试TTS系统...
python simple_tts.py "这是一个测试" -o test_output.wav
echo.
echo 如果生成成功，可以启动Web服务器：
echo python web_server.py --port 8080
pause