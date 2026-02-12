# Text-to-Speech REST API 文档

基于庄方宜语音模型的 TTS REST API 服务。

## 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors soundfile
```

### 2. 启动 API 服务器

```bash
cd text_to_speech
python tts_api.py
```

默认运行在 `http://localhost:5001`

### 3. 测试 API

```bash
python test_tts_api.py
```

## API 端点

### 1. 生成单个语音

**POST** `/api/tts/generate`

生成单个文本的语音文件。

#### 请求体 (JSON)

```json
{
  "text": "要合成的文本",
  "speed": 1.0,
  "top_k": 15,
  "top_p": 1.0,
  "temperature": 1.0,
  "reference_audio": "",
  "reference_text": "",
  "filename": ""
}
```

**参数说明:**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| text | string | ✅ | - | 要合成的文本 |
| speed | float | ❌ | 1.0 | 语速 (0.5-2.0) |
| top_k | int | ❌ | 15 | GPT 采样参数 |
| top_p | float | ❌ | 1.0 | GPT 采样参数 |
| temperature | float | ❌ | 1.0 | GPT 采样参数 (控制随机性) |
| reference_audio | string | ❌ | 默认 | 自定义参考音频路径 |
| reference_text | string | ❌ | 默认 | 自定义参考文本 |
| filename | string | ❌ | 自动生成 | 自定义输出文件名 |

#### 响应 (JSON)

```json
{
  "success": true,
  "data": {
    "audio_path": "outputs/tts_20260212_193000_abc123.wav",
    "filename": "tts_20260212_193000_abc123.wav",
    "audio_url": "/api/tts/audio/tts_20260212_193000_abc123.wav",
    "text": "要合成的文本",
    "duration": 3.5,
    "generation_time": 2.3,
    "generated_at": "2026-02-12T19:30:00"
  }
}
```

#### cURL 示例

```bash
curl -X POST http://localhost:5001/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "管理员，好久不见",
    "speed": 1.0
  }'
```

#### Python 示例

```python
import requests

response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": "管理员，好久不见",
        "speed": 1.0,
        "temperature": 0.8
    }
)

result = response.json()
if result['success']:
    audio_url = result['data']['audio_url']
    print(f"音频地址: http://localhost:5001{audio_url}")
```

---

### 2. 批量生成语音

**POST** `/api/tts/batch`

批量生成多个文本的语音文件。

#### 请求体 (JSON)

```json
{
  "texts": ["文本1", "文本2", "文本3"],
  "speed": 1.0,
  "top_k": 15,
  "top_p": 1.0,
  "temperature": 1.0
}
```

#### 响应 (JSON)

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
        "text": "文本1",
        "success": true,
        "audio_path": "outputs/batch_20260212_193000_000.wav",
        "filename": "batch_20260212_193000_000.wav",
        "audio_url": "/api/tts/audio/batch_20260212_193000_000.wav"
      },
      ...
    ]
  }
}
```

#### Python 示例

```python
import requests

response = requests.post(
    "http://localhost:5001/api/tts/batch",
    json={
        "texts": [
            "你好，我是庄方宜。",
            "今天天气真不错。",
            "很高兴见到你。"
        ],
        "speed": 1.0
    }
)

result = response.json()
if result['success']:
    print(f"成功: {result['data']['succeeded']}")
    print(f"失败: {result['data']['failed']}")
```

---

### 3. 获取音频文件

**GET** `/api/tts/audio/<filename>`

下载或播放生成的音频文件。

#### 响应

返回 WAV 格式的音频文件 (`audio/wav`)

#### 示例

```bash
# 下载音频文件
curl -O http://localhost:5001/api/tts/audio/tts_20260212_193000_abc123.wav

# 在浏览器中直接访问播放
http://localhost:5001/api/tts/audio/tts_20260212_193000_abc123.wav
```

---

### 4. 列出所有文件

**GET** `/api/tts/files`

列出所有生成的音频文件。

#### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | int | 100 | 返回数量限制 |
| offset | int | 0 | 偏移量 |

#### 响应 (JSON)

```json
{
  "success": true,
  "data": {
    "total": 10,
    "limit": 100,
    "offset": 0,
    "files": [
      {
        "filename": "tts_20260212_193000_abc123.wav",
        "path": "outputs/tts_20260212_193000_abc123.wav",
        "url": "/api/tts/audio/tts_20260212_193000_abc123.wav",
        "size": 123456,
        "created_at": "2026-02-12T19:30:00"
      },
      ...
    ]
  }
}
```

#### 示例

```bash
# 获取最近的 5 个文件
curl http://localhost:5001/api/tts/files?limit=5

# 分页获取
curl http://localhost:5001/api/tts/files?limit=10&offset=10
```

---

### 5. 健康检查

**GET** `/api/tts/health`

检查 API 服务器状态。

#### 响应 (JSON)

```json
{
  "status": "healthy",
  "model_loaded": true,
  "output_dir": "outputs",
  "version": "v2Pro"
}
```

---

### 6. 获取系统信息

**GET** `/api/tts/info`

获取 TTS 系统配置信息。

#### 响应 (JSON)

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

所有 API 在出错时返回以下格式：

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

常见 HTTP 状态码：

- `200` - 成功
- `400` - 请求参数错误
- `404` - 资源不存在
- `500` - 服务器内部错误

---

## 高级用法

### 自定义参考音频

```python
response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": "这是使用自定义参考音频的测试",
        "reference_audio": "path/to/custom/audio.wav",
        "reference_text": "参考音频的文本内容"
    }
)
```

### 调整语速和音质

```python
# 快速语音
response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": "快速说话",
        "speed": 1.5  # 1.5倍速
    }
)

# 慢速语音
response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": "慢速说话",
        "speed": 0.7  # 0.7倍速
    }
)

# 更稳定的输出（降低随机性）
response = requests.post(
    "http://localhost:5001/api/tts/generate",
    json={
        "text": "稳定的语音",
        "temperature": 0.5  # 降低随机性
    }
)
```

---

## 部署建议

### 生产环境部署

使用 Gunicorn 或 uWSGI 部署：

```bash
# 安装 gunicorn
pip install gunicorn

# 启动服务（4个工作进程）
gunicorn -w 4 -b 0.0.0.0:5001 tts_api:app
```

### Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "tts_api.py", "--host", "0.0.0.0", "--port", "5001"]
```

构建并运行：

```bash
docker build -t tts-api .
docker run -p 5001:5001 tts-api
```

---

## 性能优化

1. **模型预加载**: API 启动时自动加载模型（单例模式）
2. **并发处理**: 使用 Flask 的 `threaded=True` 支持并发请求
3. **批量处理**: 使用 `/api/tts/batch` 端点批量生成可提高效率

---

## 注意事项

1. 首次请求会触发模型加载，可能需要较长时间
2. 生成的音频文件保存在 `outputs/` 目录
3. 建议定期清理 `outputs/` 目录以节省磁盘空间
4. 长文本建议分段处理以获得更好的效果

---

## 故障排查

### 问题: 模型加载失败

检查模型文件是否存在：
- `GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt`
- `SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth`

### 问题: 生成速度慢

- 确保使用 GPU（设置 `is_half=True`）
- 减少 `max_tokens` 参数
- 使用批量接口处理多个文本

### 问题: 音频质量不佳

- 调整 `temperature` 参数（推荐 0.7-1.0）
- 尝试不同的 `top_k` 值（推荐 10-20）
- 使用更合适的参考音频
