# GPT-SoVITS 庄方宜 TTS 项目

基于 GPT-SoVITS 的中文语音合成项目，使用庄方宜的声音模型。

## 系统要求

- Python 3.14
- NVIDIA GPU (支持 CUDA 13.0+)
- Windows 10/11

## 快速开始

### 1. 激活虚拟环境

```cmd
.venv\Scripts\activate
```

### 2. 安装依赖（如果需要）

如果虚拟环境中没有安装依赖，运行：

```cmd
pip install -r requirements.txt
```

**注意**：对于 RTX 50 系列显卡，需要使用 PyTorch nightly 版本：

```cmd
pip install --pre torch torchaudio --index-url https://download.pytorch.org/whl/nightly/cu130
```

### 3. 下载 NLTK 数据

首次运行需要下载 NLTK 数据：

```cmd
python -c "import nltk; nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('cmudict')"
```

## 使用方法

### 命令行模式

#### 单句合成

```cmd
python simple_tts.py "你好，这是测试文本"
```

#### 指定输出文件

```cmd
python simple_tts.py "你好世界" -o hello.wav
```

**注意**：如果不指定输出路径，文件将自动保存到 `outputs/` 目录，文件名格式为 `zfy_YYYYMMDD_HHMMSS.wav`

#### 批量生成（从文件读取）

```cmd
python simple_tts.py -f texts.txt
```

#### 调整参数

```cmd
python simple_tts.py "快点说话" --speed 1.2 --temperature 0.8 --top-k 20
```

### Web 界面模式

启动 Web 服务器：

```cmd
python web_server.py
```

然后在浏览器中打开 `http://localhost:8080`

指定端口：

```cmd
python web_server.py --port 8888
```

### 自动清理服务

为避免 `outputs/` 目录文件过多，提供了自动清理功能。

#### 方式一：持续运行清理服务

```cmd
python cleanup_outputs.py --service
```

或使用启动脚本：

```cmd
启动清理服务.bat
```

#### 方式二：安装 Windows 定时任务（推荐）

以管理员身份运行：

```cmd
安装定时清理任务.bat
```

这将创建一个每天凌晨 3 点自动清理的定时任务。

卸载定时任务：

```cmd
卸载定时清理任务.bat
```

#### 方式三：手动清理

```cmd
python cleanup_outputs.py --once
```

#### 清理参数说明

- `--service`: 持续运行清理服务
- `--once`: 执行一次清理后退出
- `--days N`: 设置文件保留天数（默认 1 天）
- `--interval N`: 设置检查间隔秒数（默认 3600 秒）
- `--dir PATH`: 指定要清理的目录（默认 outputs）

示例：

```cmd
# 保留 2 天的文件
python cleanup_outputs.py --service --days 2

# 每 2 小时检查一次
python cleanup_outputs.py --service --interval 7200
```

## 项目结构

```
.
├── simple_tts.py                # 命令行 TTS 工具
├── web_server.py                # Web 服务器
├── main.html                    # Web 界面
├── cleanup_outputs.py           # 自动清理脚本
├── 启动TTS.bat                  # TTS 启动脚本
├── 启动清理服务.bat             # 清理服务启动脚本
├── 安装定时清理任务.bat         # 安装定时任务
├── 卸载定时清理任务.bat         # 卸载定时任务
├── GPT_SoVITS/                  # GPT-SoVITS 核心代码
├── GPT_weights_v2/              # GPT 模型权重
├── SoVITS_weights_v2/           # SoVITS 模型权重
├── logs/                        # 训练日志和参考音频
├── outputs/                     # 生成的音频输出（自动清理）
├── requirements.txt             # Python 依赖
└── README.md                    # 项目文档
```

## 模型说明

### GPT 模型
- 位置：`GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt`
- 用于：文本到语义特征的转换

### SoVITS 模型
- 位置：`SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth`
- 用于：语义特征到音频波形的转换

### 参考音频
- 位置：`logs/ZhuangFangyi_V1/reference_audio/`
- 文本：不用太拘谨，像从前一样，随意称呼就好

## 参数说明

### 命令行参数

- `text`: 要合成的文本
- `-o, --output`: 输出文件路径
- `-f, --file`: 从文件读取文本（每行一句）
- `--ref-audio`: 参考音频路径（覆盖默认）
- `--ref-text`: 参考文本（覆盖默认）
- `--speed`: 语速 (0.5-2.0，默认 1.0)
- `--top-k`: GPT 采样参数 (默认 15)
- `--top-p`: GPT 采样参数 (默认 1.0)
- `--temperature`: GPT 采样参数 (默认 1.0)

### 生成参数说明

- **speed**: 控制语速，值越大语速越快
- **top_k**: 控制采样多样性，值越小越保守
- **top_p**: 核采样参数，控制生成质量
- **temperature**: 温度参数，控制随机性

## 常见问题

### 1. CUDA 不可用

确保安装了正确的 PyTorch CUDA 版本：

```cmd
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

如果显示 `False`，需要重新安装 CUDA 版本的 PyTorch。

### 2. 导入错误

如果遇到模块导入错误，确保：
- 虚拟环境已激活
- 所有依赖已安装
- Python 版本正确 (3.14)

### 3. 内存不足

如果 GPU 内存不足，可以：
- 减小 batch size
- 使用 CPU 模式（修改 `simple_tts.py` 中的 `is_half` 为 `False`）

### 4. 生成速度慢

- 确保使用 GPU 加速
- 检查 CUDA 是否正确安装
- 使用半精度模式（`is_half=True`）

### 5. outputs 目录文件过多

使用自动清理功能：
- 安装定时任务：`安装定时清理任务.bat`（推荐）
- 或持续运行清理服务：`启动清理服务.bat`
- 或手动清理：`python cleanup_outputs.py --once`

### 6. 清理服务无法启动

确保：
- 虚拟环境已激活
- `outputs` 目录存在
- 有足够的权限访问该目录

### 7. 定时任务安装失败

- 以管理员身份运行 `安装定时清理任务.bat`
- 检查 Windows 任务计划程序服务是否正常运行

## 技术细节

### 导入路径修复

原项目存在大量绝对导入问题，已修复为相对导入：
- `from text import` → `from . import`
- `from module import` → `from . import`
- `from tools import` → 添加到 `sys.path`

### 依赖包补充

原 requirements.txt 缺少以下包，已补充：
- matplotlib
- peft
- psutil
- 其他必要的依赖

### jieba_fast 兼容

添加了 jieba_fast 的回退机制，如果未安装则使用 jieba。

## 性能优化

- 使用 GPU 加速（CUDA）
- 半精度浮点运算（FP16）
- 进程优先级提升（Windows）
- 模型权重缓存

## 许可证

本项目采用 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

### 重要声明

- 本项目代码部分采用 MIT 许可证
- 基于 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 开源项目
- 声音模型（庄方宜）仅供个人学习和研究使用
- 商业使用需获得适当授权

## 免责声明

1. 本项目仅供学习交流使用
2. 使用本项目生成的语音内容，使用者需自行承担相关责任
3. 禁止将本项目用于任何违法违规用途
4. 禁止用于制作虚假信息、诈骗等不当用途

## 致谢

- [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 项目团队
- 庄方宜声音模型训练者
- 所有贡献者和使用者
