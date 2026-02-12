# 智能语音助手

基于庄方宜模型的 LLM 对话 + TTS 语音合成系统。

---

## 项目结构

```
.
├── LLMchat/                    # LLM 聊天模块
│   ├── chat_api.py             # REST API 服务
│   ├── chat_manager.py         # 核心管理器
│   └── zhuang_fangyi_int4.gguf # LLM 模型
│
├── text_to_speech/             # TTS 语音合成模块
│   ├── tts_api.py              # REST API 服务
│   ├── simple_tts.py           # TTS 核心实现
│   ├── GPT_weights_v2/         # GPT 模型权重
│   └── SoVITS_weights_v2/      # SoVITS 模型权重
│
├── API_DOCUMENTATION.md        # 完整 API 接口文档
├── requirements.txt            # 项目依赖
├── test_apis.py                # API 测试脚本
└── integration_example.py      # 集成使用示例
```

---

## 快速开始

### 0. 准备模型文件

**⚠️ 模型文件不包含在仓库中，需要单独下载并放置到指定位置。**

#### LLM 模型文件

```
LLMchat/zhuang_fangyi_int4.gguf    # 约 2-4 GB
```

#### TTS 模型文件

**微调模型（必需）:**
```
text_to_speech/GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt          # 约 500 MB
text_to_speech/SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth   # 约 300 MB
text_to_speech/logs/ZhuangFangyi_V1/reference_audio/
    └── zfy_raw_vocals.wav_0011840000_0012000960.wav            # 约 1 MB
```

**基础预训练模型（必需）:**
```
text_to_speech/GPT_SoVITS/pretrained_models/
├── chinese-hubert-base/
│   ├── config.json
│   ├── preprocessor_config.json
│   └── pytorch_model.bin                                       # 约 400 MB
├── chinese-roberta-wwm-ext-large/
│   ├── config.json
│   ├── pytorch_model.bin                                       # 约 1.2 GB
│   └── tokenizer.json
├── g2pw-chinese/
│   ├── config.json
│   ├── pytorch_model.bin                                       # 约 400 MB
│   └── [其他配置文件]
├── models--nvidia--bigvgan_v2_24khz_100band_256x/
│   ├── bigvgan_generator.pt                                    # 约 350 MB
│   └── config.json
├── v2Pro/
│   ├── s2Gv2Pro.pth                                           # 约 600 MB
│   └── s2Dv2Pro.pth                                           # 约 300 MB
├── sv/
│   └── pretrained_eres2netv2w24s4ep4.ckpt                     # 约 200 MB
├── fast_langdetect/
│   └── lid.176.bin                                            # 约 1 MB
├── s1v3.ckpt                                                  # 约 500 MB
├── s2Gv3.pth                                                  # 约 600 MB
└── [其他基础模型文件]
```

**总计大小:** 约 8-10 GB（包含所有模型）

**验证模型文件:**
```bash
# Windows
dir LLMchat\zhuang_fangyi_int4.gguf
dir text_to_speech\GPT_weights_v2\ZhuangFangyi_V1-e16.ckpt
dir text_to_speech\GPT_SoVITS\pretrained_models\chinese-hubert-base\pytorch_model.bin

# Linux/Mac
ls -lh LLMchat/zhuang_fangyi_int4.gguf
ls -lh text_to_speech/GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt
ls -lh text_to_speech/GPT_SoVITS/pretrained_models/chinese-hubert-base/pytorch_model.bin
```

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

**注意:** 默认安装 CPU 版本。GPU 版本安装见下方 "GPU/CPU 配置" 部分。

### 2. 启动服务

**终端 1 - LLM Chat API:**
```bash
cd LLMchat
python chat_api.py
```

**终端 2 - TTS API:**
```bash
cd text_to_speech
python tts_api.py
```

### 3. 测试

```bash
python test_apis.py
```

---

## API 服务

### LLM Chat API (端口 5000)

智能对话服务，支持多用户、多会话管理。

**主要端点:**
- `POST /api/chat` - 发送消息
- `GET /api/sessions/<user_id>` - 获取会话列表
- `GET /api/health` - 健康检查

**示例:**
```python
import requests

response = requests.post(
    "http://localhost:5000/api/chat",
    json={"message": "你好", "user_id": "user_001"},
    timeout=180
)
print(response.json()['data']['response'])
```

### TTS API (端口 5001)

文字转语音服务。

**主要端点:**
- `POST /api/tts/generate` - 生成语音
- `POST /api/tts/batch` - 批量生成
- `GET /api/tts/audio/<filename>` - 获取音频文件
- `GET /api/tts/health` - 健康检查

**示例:**
```python
import requests

response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={"text": "你好，这是测试", "speed": 1.0}
)
print(response.json()['data']['audio_url'])
```

**完整 API 文档:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## GPU/CPU 配置

两个服务默认使用 GPU 加速。如需使用 CPU，修改配置文件：

### LLM Chat API

编辑 `LLMchat/chat_api.py`:
```python
USE_GPU = False  # 改为 False 使用 CPU
N_GPU_LAYERS = 0
```

### TTS API

编辑 `text_to_speech/tts_api.py`:
```python
USE_GPU = False  # 改为 False 使用 CPU
USE_HALF_PRECISION = False
```

**性能对比:**

| 服务 | GPU 模式 | CPU 模式 |
|------|---------|---------|
| LLM Chat | 5-15秒 | 30-120秒 |
| TTS | 2-4秒 | 5-10秒 |

**GPU 要求:**
- NVIDIA GPU with CUDA 11.8+
- 显存: 4GB+ (推荐 6GB+)

**安装 GPU 版本 PyTorch:**
```bash
pip uninstall torch torchaudio
pip install torch==2.9.1+cu130 torchaudio==2.9.1 --extra-index-url https://download.pytorch.org/whl/nightly/cu130
```

---

## 集成使用

完整示例见 `integration_example.py`：

```python
import requests

# 1. LLM 对话
chat_response = requests.post(
    "http://localhost:5000/api/chat",
    json={"message": "给我讲个笑话", "user_id": "user_001"},
    timeout=180
)
text_reply = chat_response.json()['data']['response']

# 2. 转为语音
tts_response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={"text": text_reply[:50], "speed": 1.0}
)
audio_url = tts_response.json()['data']['audio_url']
print(f"音频: http://localhost:5001{audio_url}")
```

---

## 常见问题

### Q: LLM 响应很慢？
A: 使用 CPU 模式时响应时间为 30-120 秒，这是正常的。建议：
- 启用 GPU 加速（响应时间降至 5-15 秒）
- 增加超时时间到 180 秒以上

### Q: 如何验证 GPU 是否启用？
A: 查看服务启动日志：
```
# LLM Chat API
🚀 GPU 加速已启用 (offloading 35 layers)

# TTS API
TTS API 配置:
  GPU 加速: ✅ 启用
  半精度: ✅ 启用
```

### Q: 显存不足怎么办？
A: 
- LLM: 减少 `N_GPU_LAYERS` (如改为 20)
- TTS: 设置 `USE_HALF_PRECISION = False`
- 或使用 CPU 模式

### Q: 如何管理多个用户？
A: 每个用户使用唯一的 `user_id`，系统自动隔离数据：
```python
# 用户1
requests.post("http://localhost:5000/api/chat", 
    json={"message": "你好", "user_id": "user_001"})

# 用户2
requests.post("http://localhost:5000/api/chat", 
    json={"message": "你好", "user_id": "user_002"})
```

### Q: 模型文件放在哪里？
A: 
**LLM 模型:**
- `LLMchat/zhuang_fangyi_int4.gguf`

**TTS 微调模型:**
- `text_to_speech/GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt`
- `text_to_speech/SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth`

**TTS 基础模型:**
- `text_to_speech/GPT_SoVITS/pretrained_models/` 目录下的所有文件

文件名和路径必须完全匹配，路径区分大小写。总计约 8-10 GB。

---

## 系统要求

- Python 3.9+
- CPU: 4核以上
- 内存: 8GB+ (CPU模式) / 4GB+ (GPU模式)
- 显存: 4GB+ (GPU模式)
- 磁盘: 10GB+

---

## 生产部署

使用 Gunicorn:

```bash
# LLM Chat API
cd LLMchat
gunicorn -w 4 -b 0.0.0.0:5000 chat_api:app --timeout 180

# TTS API
cd text_to_speech
gunicorn -w 2 -b 0.0.0.0:5001 tts_api:app --timeout 120
```

---

## 文件说明

- `API_DOCUMENTATION.md` - 完整 API 接口文档
- `requirements.txt` - 项目依赖列表
- `test_apis.py` - API 测试脚本
- `integration_example.py` - LLM + TTS 集成示例

---

## 技术栈

- **LLM**: llama-cpp-python (INT4 量化模型)
- **TTS**: GPT-SoVITS (v2Pro)
- **Web 框架**: Flask
- **深度学习**: PyTorch

---

## 许可证

请参考各子项目的许可证文件。

---

## 更新日志

### v1.0 (2026-02-12)
- ✅ LLM Chat API 完整功能
- ✅ TTS API 完整功能
- ✅ 多用户、多会话支持
- ✅ GPU/CPU 配置支持
- ✅ 完整 API 文档

---

**快速链接:**
- [API 文档](API_DOCUMENTATION.md)
- [测试脚本](test_apis.py)
- [集成示例](integration_example.py)
