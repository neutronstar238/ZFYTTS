# 智能语音助手 API 接口文档

版本: 1.0  
更新时间: 2026-02-12

---

## 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [LLM Chat API](#llm-chat-api)
- [TTS API](#tts-api)
- [错误处理](#错误处理)
- [示例代码](#示例代码)

---

## 概述

本系统提供两个独立的 REST API 服务：

1. **LLM Chat API** - 基于庄方宜模型的智能对话服务
2. **TTS API** - 文字转语音服务

两个服务可以独立使用，也可以组合使用实现完整的语音对话功能。

### 服务地址

| 服务 | 默认地址 | 端口 |
|------|---------|------|
| LLM Chat API | http://localhost:5000 | 5000 |
| TTS API | http://localhost:5001 | 5001 |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 启动 LLM Chat API
cd LLMchat
python chat_api.py

# 启动 TTS API（新终端）
cd text_to_speech
python tts_api.py
```

### 3. 测试服务

```bash
python test_apis.py
```

---

## LLM Chat API

基于庄方宜 INT4 量化模型的智能对话服务，支持多用户、多会话管理。

### 基础信息

- **Base URL**: `http://localhost:5000`
- **Content-Type**: `application/json`
- **响应格式**: JSON

---

### 端点列表

#### 1. 健康检查

**GET** `/api/health`

检查服务状态。

**响应示例:**
```json
{
  "status": "healthy",
  "model": "zhuang_fangyi_int4.gguf"
}
```

---

#### 2. 发送消息

**POST** `/api/chat`

发送消息并获取 AI 回复。

**请求参数:**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| message | string | ✅ | - | 用户消息内容 |
| user_id | string | ❌ | "default_user" | 用户唯一标识 |
| session_id | string | ❌ | null | 会话ID（不提供则创建新会话） |
| system_prompt | string | ❌ | 庄方宜角色设定 | 系统提示词 |
| max_tokens | integer | ❌ | 512 | 最大生成token数 |
| temperature | float | ❌ | 0.7 | 采样温度 (0.0-2.0) |
| top_p | float | ❌ | 0.8 | Top-p 采样 |
| repeat_penalty | float | ❌ | 1.15 | 重复惩罚（避免复读） |

**请求示例:**
```json
{
  "message": "管理员，武陵的研究进展如何？",
  "user_id": "user_001",
  "temperature": 0.7,
  "top_p": 0.8,
  "repeat_penalty": 1.15
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "response": "（轻轻翻阅着手中的报告，抬眼看向你）管理员，武陵的研究进展...",
    "session_id": "3084ed8e-4da6-4914-b8a7-69b6478e2c53",
    "user_id": "user_001",
    "message_count": 3
  }
}
```

**注意事项:**
- 首次请求响应时间较长（30-120秒），这是正常的
- 建议设置较长的超时时间（180秒以上）
- 相同 user_id 和 session_id 的对话会保持上下文
- `repeat_penalty` 参数用于避免模型重复相同的话（推荐 1.15）
- 默认系统提示词包含完整的庄方宜角色设定

---

#### 3. 获取用户会话列表

**GET** `/api/sessions/<user_id>`

获取指定用户的所有会话。

**URL 参数:**
- `user_id`: 用户ID

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "session_id": "3084ed8e-4da6-4914-b8a7-69b6478e2c53",
      "preview": "你好，请介绍一下你自己",
      "last_updated": "2026-02-12T19:53:56",
      "message_count": 5
    }
  ]
}
```

---

#### 4. 获取会话历史

**GET** `/api/session/<user_id>/<session_id>`

获取指定会话的完整对话历史。

**URL 参数:**
- `user_id`: 用户ID
- `session_id`: 会话ID

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "role": "system",
      "content": "你是庄方宜，一个温柔体贴的AI助手...",
      "timestamp": "2026-02-12T19:50:00"
    },
    {
      "role": "user",
      "content": "你好",
      "timestamp": "2026-02-12T19:50:05"
    },
    {
      "role": "assistant",
      "content": "你好！很高兴遇见您...",
      "timestamp": "2026-02-12T19:50:08"
    }
  ]
}
```

---

#### 5. 删除会话

**DELETE** `/api/session/<user_id>/<session_id>`

删除指定会话及其所有历史记录。

**URL 参数:**
- `user_id`: 用户ID
- `session_id`: 会话ID

**响应示例:**
```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

---

## TTS API

文字转语音服务，基于庄方宜语音模型。

### 基础信息

- **Base URL**: `http://localhost:5001`
- **Content-Type**: `application/json`
- **响应格式**: JSON
- **音频格式**: WAV

---

### 端点列表

#### 1. 健康检查

**GET** `/api/tts/health`

检查服务状态。

**响应示例:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "output_dir": "outputs",
  "version": "v2Pro"
}
```

---

#### 2. 生成语音

**POST** `/api/tts/generate`

将文本转换为语音文件。

**请求参数:**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| text | string | ✅ | - | 要合成的文本 |
| speed | float | ❌ | 1.0 | 语速 (0.5-2.0) |
| top_k | integer | ❌ | 15 | GPT采样参数 |
| top_p | float | ❌ | 1.0 | GPT采样参数 |
| temperature | float | ❌ | 1.0 | 采样温度 |
| reference_audio | string | ❌ | 默认 | 自定义参考音频路径 |
| reference_text | string | ❌ | 默认 | 自定义参考文本 |
| filename | string | ❌ | 自动生成 | 自定义输出文件名 |

**请求示例:**
```json
{
  "text": "你好，这是一个测试",
  "speed": 1.0,
  "temperature": 0.8
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "audio_path": "outputs/tts_20260212_195358_dc4dc891.wav",
    "filename": "tts_20260212_195358_dc4dc891.wav",
    "audio_url": "/api/tts/audio/tts_20260212_195358_dc4dc891.wav",
    "text": "你好，这是一个测试",
    "duration": 2.42,
    "generation_time": 4.31,
    "generated_at": "2026-02-12T19:53:58"
  }
}
```

---

#### 3. 批量生成语音

**POST** `/api/tts/batch`

批量生成多个文本的语音文件。

**请求参数:**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| texts | array | ✅ | - | 文本数组 |
| speed | float | ❌ | 1.0 | 语速 |
| top_k | integer | ❌ | 15 | GPT采样参数 |
| top_p | float | ❌ | 1.0 | GPT采样参数 |
| temperature | float | ❌ | 1.0 | 采样温度 |

**请求示例:**
```json
{
  "texts": [
    "你好，我是庄方宜",
    "今天天气真不错",
    "很高兴见到你"
  ],
  "speed": 1.0
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "total": 3,
    "succeeded": 3,
    "failed": 0,
    "results": [
      {
        "index": 0,
        "text": "你好，我是庄方宜",
        "success": true,
        "audio_path": "outputs/batch_20260212_195400_000.wav",
        "filename": "batch_20260212_195400_000.wav",
        "audio_url": "/api/tts/audio/batch_20260212_195400_000.wav"
      }
    ]
  }
}
```

---

#### 4. 获取音频文件

**GET** `/api/tts/audio/<filename>`

下载或播放生成的音频文件。

**URL 参数:**
- `filename`: 音频文件名

**响应:**
- Content-Type: `audio/wav`
- 返回 WAV 格式音频文件

**示例:**
```
GET http://localhost:5001/api/tts/audio/tts_20260212_195358_dc4dc891.wav
```

---

#### 5. 列出所有文件

**GET** `/api/tts/files`

列出所有生成的音频文件。

**查询参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | integer | 100 | 返回数量限制 |
| offset | integer | 0 | 偏移量 |

**响应示例:**
```json
{
  "success": true,
  "data": {
    "total": 10,
    "limit": 100,
    "offset": 0,
    "files": [
      {
        "filename": "tts_20260212_195358_dc4dc891.wav",
        "path": "outputs/tts_20260212_195358_dc4dc891.wav",
        "url": "/api/tts/audio/tts_20260212_195358_dc4dc891.wav",
        "size": 123456,
        "created_at": "2026-02-12T19:53:58"
      }
    ]
  }
}
```

---

#### 6. 获取系统信息

**GET** `/api/tts/info`

获取 TTS 系统配置信息。

**响应示例:**
```json
{
  "success": true,
  "data": {
    "model_version": "v2Pro",
    "gpt_model": "GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt",
    "sovits_model": "SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth",
    "reference_audio": "logs/ZhuangFangyi_V1/reference_audio/...",
    "reference_text": "不用太拘谨，像从前一样，随意称呼就好"
  }
}
```

---

## 错误处理

所有 API 在出错时返回统一格式：

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 示例代码

### Python 示例

#### 1. LLM 对话

```python
import requests

# 发送消息
response = requests.post(
    "http://localhost:5000/api/chat",
    json={
        "message": "你好，请介绍一下你自己",
        "user_id": "user_001"
    },
    timeout=180
)

result = response.json()
if result['success']:
    print(f"回复: {result['data']['response']}")
    session_id = result['data']['session_id']
    
    # 继续对话
    response = requests.post(
        "http://localhost:5000/api/chat",
        json={
            "message": "你有什么特长？",
            "user_id": "user_001",
            "session_id": session_id
        },
        timeout=180
    )
```

#### 2. TTS 生成语音

```python
import requests

# 生成语音
response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": "你好，这是一个测试",
        "speed": 1.0
    }
)

result = response.json()
if result['success']:
    audio_url = result['data']['audio_url']
    print(f"音频地址: http://localhost:5001{audio_url}")
    
    # 下载音频
    audio_response = requests.get(f"http://localhost:5001{audio_url}")
    with open("output.wav", "wb") as f:
        f.write(audio_response.content)
```

#### 3. 完整集成（LLM + TTS）

```python
import requests

# 1. 与 LLM 对话
chat_response = requests.post(
    "http://localhost:5000/api/chat",
    json={
        "message": "给我讲个笑话",
        "user_id": "user_001"
    },
    timeout=180
)

text_reply = chat_response.json()['data']['response']
print(f"文字回复: {text_reply}")

# 2. 将回复转为语音
tts_response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": text_reply[:50],  # 截取前50字
        "speed": 1.0
    }
)

audio_info = tts_response.json()['data']
print(f"音频文件: {audio_info['filename']}")
print(f"访问地址: http://localhost:5001{audio_info['audio_url']}")
```

---

### cURL 示例

#### LLM 对话

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "user_id": "user_001"
  }'
```

#### TTS 生成

```bash
curl -X POST http://localhost:5001/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，这是测试",
    "speed": 1.0
  }'
```

---

## 性能说明

### LLM Chat API

- **首次响应**: 30-120秒（CPU推理 + INT4量化模型）
- **后续响应**: 30-120秒
- **建议超时**: 180秒以上
- **优化建议**: 使用GPU可显著提升速度

### TTS API

- **首次生成**: 4-6秒（包含模型加载）
- **后续生成**: 2-4秒
- **音频质量**: 24kHz, 16-bit WAV
- **优化建议**: 使用GPU可提升速度

---

## 配置说明

### GPU 加速

两个服务都支持 GPU 加速：

**LLM Chat API:**
```python
# 在 chat_manager.py 中
chatbot = ChatBot(
    model_path="zhuang_fangyi_int4.gguf",
    n_gpu_layers=35  # 使用GPU加速
)
```

**TTS API:**
```python
# 在 simple_tts.py 中
os.environ["is_half"] = "True"  # 启用GPU半精度
```

详见各服务的配置文件。

---

## 常见问题

### Q: LLM 响应很慢？
A: 这是正常的。使用 CPU + INT4 量化模型时，响应时间为 30-120 秒。建议：
- 使用 GPU 加速
- 增加超时时间到 180 秒以上
- 使用更小的模型

### Q: TTS 生成失败？
A: 检查：
- 模型文件是否完整
- GPU 驱动是否正常（如使用 GPU）
- 文本是否包含特殊字符

### Q: 如何管理多个用户？
A: 每个用户使用唯一的 `user_id`，系统会自动隔离不同用户的数据和会话。

### Q: 会话记录保存在哪里？
A: 
- LLM 会话: `LLMchat/memories/<user_id>/<session_id>.json`
- TTS 音频: `text_to_speech/outputs/*.wav`

---

## 更新日志

### v1.0 (2026-02-12)
- 初始版本发布
- LLM Chat API 完整功能
- TTS API 完整功能
- 多用户、多会话支持
- GPU/CPU 配置支持

---

## 技术支持

如有问题，请查看：
- `PROJECT_README.md` - 项目总览
- `API_TEST_REPORT.md` - 测试报告
- `test_apis.py` - 测试脚本

或通过 Issue 联系我们。
