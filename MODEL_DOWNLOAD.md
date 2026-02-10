# 模型文件下载说明

由于模型文件较大（约 1.5 GB），无法直接上传到 GitHub。请按以下方式获取模型文件：

## 需要的模型文件

### 1. GPT 模型权重
放置位置：`GPT_weights_v2/`

需要的文件：
- `ZhuangFangyi_V1-e16.ckpt` (推荐使用，约 300 MB)
- `ZhuangFangyi_V1-e12.ckpt` (可选)
- `ZhuangFangyi_V1-e8.ckpt` (可选)
- `ZhuangFangyi_V1-e4.ckpt` (可选)

### 2. SoVITS 模型权重
放置位置：`SoVITS_weights_v2/`

需要的文件：
- `ZhuangFangyi_V1_e20_s300.pth` (推荐使用，约 85 MB)
- `ZhuangFangyi_V1_e15_s225.pth` (可选)
- `ZhuangFangyi_V1_e10_s150.pth` (可选)
- `ZhuangFangyi_V1_e5_s75.pth` (可选)

### 3. 参考音频
放置位置：`logs/ZhuangFangyi_V1/reference_audio/`

需要的文件：
- `zfy_raw_vocals.wav_0011840000_0012000960.wav`

## 下载方式

### 方式一：网盘下载（推荐）
[待添加网盘链接]

### 方式二：Git LFS（如果已配置）
如果你有 Git LFS 访问权限，可以使用：
```bash
git lfs pull
```

## 目录结构

下载后的目录结构应该如下：

```
项目/
├── GPT_weights_v2/
│   └── ZhuangFangyi_V1-e16.ckpt
├── SoVITS_weights_v2/
│   └── ZhuangFangyi_V1_e20_s300.pth
└── logs/
    └── ZhuangFangyi_V1/
        └── reference_audio/
            └── zfy_raw_vocals.wav_0011840000_0012000960.wav
```

## 验证安装

下载完成后，运行以下命令验证：

```bash
python simple_tts.py "测试文本"
```

如果成功生成音频文件，说明模型安装正确。
