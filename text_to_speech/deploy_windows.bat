@echo off
REM Windows 快速部署脚本
echo ========================================
echo 庄方宜 TTS - Windows 自动部署
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9-3.12
    pause
    exit /b 1
)

echo [1/4] 检测到 Python 已安装
python --version

REM 安装依赖
echo.
echo [2/4] 正在安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] 依赖安装出现问题，尝试使用国内镜像源...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

REM 检查模型文件
echo.
echo [3/4] 检查模型文件...
if not exist "GPT_weights_v2\ZhuangFangyi_V1-e16.ckpt" (
    echo [错误] GPT 模型文件不存在
    echo 请确保 GPT_weights_v2\ZhuangFangyi_V1-e16.ckpt 文件存在
    pause
    exit /b 1
)

if not exist "SoVITS_weights_v2\ZhuangFangyi_V1_e20_s300.pth" (
    echo [错误] SoVITS 模型文件不存在
    echo 请确保 SoVITS_weights_v2\ZhuangFangyi_V1_e20_s300.pth 文件存在
    pause
    exit /b 1
)

echo [✓] 模型文件检查通过

REM 测试运行
echo.
echo [4/4] 运行测试...
python simple_tts.py "测试文本，部署成功" -o outputs/test_deploy.wav
if errorlevel 1 (
    echo [错误] 测试失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 部署成功！
echo ========================================
echo.
echo 使用方法：
echo 1. 命令行模式：python simple_tts.py "你的文本"
echo 2. Web 界面：python web_server.py --port 8080
echo.
pause
