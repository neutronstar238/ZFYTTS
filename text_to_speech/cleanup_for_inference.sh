#!/bin/bash
# 清理脚本：只保留推理所需的核心文件

set -e

echo "🧹 开始清理 GPT-SoVITS 项目..."
echo "⚠️  将删除所有训练相关文件，只保留推理功能"
echo ""

cd /root/autodl-tmp/GPT-SoVITS

# 1. 删除训练日志和中间文件
echo "📝 删除训练日志..."
rm -rf logs/ZhuangFangyi_V1/logs_s2_v2 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/GPT_ckpt_v2 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/*.log 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/*.pid 2>/dev/null || true
rm -f *.log *.pid 2>/dev/null || true

# 2. 删除原始音频和处理中间文件
echo "🎵 删除原始音频..."
rm -rf raw_audio 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/0-raw_audio 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/1-vocals 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/2-asr 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/3-bert 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/4-cnhubert 2>/dev/null || true

# 保留一个参考音频即可，删除其他
echo "🎤 精简参考音频（只保留默认引子）..."
cd logs/ZhuangFangyi_V1/5-wav32k
# 保留默认参考音频
DEFAULT_REF="zfy_raw_vocals.wav_0011840000_0012000960.wav"
mkdir -p ../reference_audio
cp "$DEFAULT_REF" ../reference_audio/ 2>/dev/null || true
cd ../../..
# 删除整个 5-wav32k 目录
rm -rf logs/ZhuangFangyi_V1/5-wav32k 2>/dev/null || true

# 3. 删除训练数据文件
echo "📊 删除训练数据文件..."
rm -rf logs/ZhuangFangyi_V1/6-name2semantic-*.tsv 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/2-name2text.txt 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/s1.yaml 2>/dev/null || true
rm -rf logs/ZhuangFangyi_V1/s2.json 2>/dev/null || true

# 4. 删除训练脚本
echo "🔧 删除训练脚本..."
rm -f run_training.py run_training_1a.py 2>/dev/null || true
rm -f run_roformer_uvr5.py run_uvr5.py run_slicer.py 2>/dev/null || true
rm -f train_background.sh monitor_training.sh split_and_process.sh 2>/dev/null || true
rm -f uvr5_debug.py 2>/dev/null || true

# 5. 删除训练相关的其他权重文件
echo "💾 删除中间训练权重..."
rm -f *.pth 2>/dev/null || true  # 删除根目录的 pth 文件
rm -rf logs/ZhuangFangyi_V1/SoVITS_weights_v2 2>/dev/null || true  # 删除 logs 下的副本

# 6. 删除 WebUI 和 API（只保留 simple_tts.py）
echo "🌐 删除 WebUI 和 API..."
rm -f webui.py api.py api_v2.py 2>/dev/null || true
rm -f go-webui.bat go-webui.ps1 2>/dev/null || true

# 7. 删除文档和笔记本
echo "📚 删除文档和笔记本..."
rm -rf docs 2>/dev/null || true
rm -f *.ipynb 2>/dev/null || true
rm -f README.md LICENSE 2>/dev/null || true
rm -f 使用指南.md 推理测试指南.md 2>/dev/null || true

# 8. 删除 Docker 相关
echo "🐳 删除 Docker 文件..."
rm -rf Docker 2>/dev/null || true
rm -f Dockerfile docker-compose.yaml docker_build.sh 2>/dev/null || true
rm -f .dockerignore 2>/dev/null || true

# 9. 删除 Git 仓库
echo "📦 删除 Git 仓库..."
rm -rf .git .github 2>/dev/null || true
rm -f .gitignore .pre-commit-config.yaml 2>/dev/null || true

# 10. 删除安装脚本
echo "⚙️删除安装脚本..."
rm -f install.sh install.ps1 2>/dev/null || true
rm -f requirements.txt extra-req.txt 2>/dev/null || true

# 11. 删除临时文件和输出
echo "🗑️  删除临时文件..."
rm -rf TEMP output ._____temp .lock 2>/dev/null || true
rm -rf __pycache__ GPT_SoVITS/__pycache__ 2>/dev/null || true
rm -f test_batch.txt weight.json 2>/dev/null || true

# 12. 删除不需要的预训练模型
echo "🎯 清理预训练模型..."
rm -f G2PWModel.zip 2>/dev/null || true
# 只保留正在使用的 v2 预训练模型
rm -rf GPT_SoVITS/pretrained_models/gsv-v2final-pretrained 2>/dev/null || true
rm -f pretrained_models_v2.zip 2>/dev/null || true

# 13. 删除空的权重目录
echo "📂 删除空权重目录..."
rm -rf GPT_weights GPT_weights_v2Pro GPT_weights_v2ProPlus GPT_weights_v3 GPT_weights_v4 2>/dev/null || true
rm -rf SoVITS_weights SoVITS_weights_v2Pro SoVITS_weights_v2ProPlus SoVITS_weights_v3 SoVITS_weights_v4 2>/dev/null || true

# 14. 清理 GPT_SoVITS 目录中的训练相关代码
echo "🧬 清理训练相关代码..."
rm -rf GPT_SoVITS/prepare_datasets 2>/dev/null || true
rm -f GPT_SoVITS/s1_train.py GPT_SoVITS/s2_train.py 2>/dev/null || true
rm -rf GPT_SoVITS/__pycache__ 2>/dev/null || true

# 15. 清理 tools 目录（保留必要的推理工具）
echo "🔨 清理 tools 目录..."
# 删除 UVR5、ASR 等训练工具
rm -rf tools/uvr5 tools/asr tools/damo_asr 2>/dev/null || true
# 保留 i18n 和 assets（WebUI 需要，但我们用 simple_tts.py）
# 如果不需要多语言，也可以删除
rm -rf tools/i18n 2>/dev/null || true
rm -rf tools/assets 2>/dev/null || true

echo ""
echo "✅ 清理完成！"
echo ""
echo "📁 保留的核心文件："
echo "   - simple_tts.py                      ⭐ 推理主程序"
echo "   - README_使用说明.md                  📖 使用文档"
echo "   - GPT_weights_v2/                     🧠 GPT 模型"
echo "   - SoVITS_weights_v2/                  🎵 SoVITS 模型"
echo "   - logs/ZhuangFangyi_V1/reference_audio/ 🎤 参考音频"
echo "   - GPT_SoVITS/                         📦 核心推理库"
echo "   - tools/                              🔧 工具库（精简版）"
echo ""

# 显示清理后的大小
echo "💾 清理后的项目大小："
du -sh /root/autodl-tmp/GPT-SoVITS 2>/dev/null || true
echo ""
