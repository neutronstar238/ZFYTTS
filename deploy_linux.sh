#!/bin/bash
# Linux/macOS 快速部署脚本

echo "========================================"
echo "庄方宜 TTS - Linux/macOS 自动部署"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python 3.9-3.12"
    exit 1
fi

echo "[1/5] 检测到 Python 已安装"
python3 --version

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[2/5] 创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "[2/5] 跳过虚拟环境创建"
fi

# 安装依赖
echo ""
echo "[3/5] 正在安装依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[警告] 依赖安装出现问题，尝试使用国内镜像源..."
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

# 检查模型文件
echo ""
echo "[4/5] 检查模型文件..."
if [ ! -f "GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt" ]; then
    echo "[错误] GPT 模型文件不存在"
    echo "请确保 GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt 文件存在"
    exit 1
fi

if [ ! -f "SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth" ]; then
    echo "[错误] SoVITS 模型文件不存在"
    echo "请确保 SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth 文件存在"
    exit 1
fi

echo "[✓] 模型文件检查通过"

# 测试运行
echo ""
echo "[5/5] 运行测试..."
python simple_tts.py "测试文本，部署成功" -o outputs/test_deploy.wav
if [ $? -ne 0 ]; then
    echo "[错误] 测试失败，请检查错误信息"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ 部署成功！"
echo "========================================"
echo ""
echo "使用方法："
echo "1. 命令行模式：python simple_tts.py '你的文本'"
echo "2. Web 界面：python web_server.py --port 8080"
echo ""
echo "如果使用了虚拟环境，请先激活："
echo "source venv/bin/activate"
echo ""
