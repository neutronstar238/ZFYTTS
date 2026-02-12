#!/bin/bash
# 启动 Web UI 服务器

cd /root/autodl-tmp/GPT-SoVITS

echo "🚀 正在启动 Web UI..."
python web_server.py --port 8080
