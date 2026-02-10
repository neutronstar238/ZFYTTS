# 庄方宜 GPT-SoVITS 训练配置说明

## 🎤 训练概况

- **实验名称**: ZhuangFangyi_V1
- **基底模型**: GPT-SoVITS-v2-276h (276小时高质量预训练)
- **数据量**: 180 条高质量人工校对标注
- **显存**: 48GB NVIDIA vGPU
- **训练状态**: ✅ 后台运行中 (SSH 断开后继续)

---

## 📊 训练参数配置

### SoVITS 训练 (声学模型)
根据 180 条数据量和 48GB 显存，优化配置如下：

- **Batch Size**: 14 (充分利用显存，稳定训练)
- **Total Epochs**: 22 (避免过拟合)
- **Save Every**: 5 epochs
- **Learning Rate**: 0.0001
- **Text Low LR Rate**: 0.4 (文本编码器降低学习率)
- **FP16**: 启用 (混合精度训练)
- **基底模型**: `s2G2333k.pth` (v2-276h, 2333k steps)

**训练时长预估**: 约 15-20 分钟

### GPT 训练 (语言模型)
GPT 对韵律敏感，轮数不宜过高：

- **Batch Size**: 12 (GPT 显存占用较大)
- **Total Epochs**: 16 (避免"复读机"现象)
- **Save Every**: 4 epochs  
- **Learning Rate**: 0.0001
- **Gradient Accumulation**: 4 steps
- **Precision**: FP32
- **基底模型**: `s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt` (v2-276h)

**训练时长预估**: 约 10-15 分钟

---

## 📂 文件结构

```
logs/ZhuangFangyi_V1/
├── s2.json                      # SoVITS 配置文件
├── s1.yaml                      # GPT 配置文件
├── 2-name2text.txt              # 文本标注文件 (180条)
├── 3-bert/                      # BERT 特征 (180个.pt)
├── 4-cnhubert/                  # CNHubert 特征 (180个.pt)
├── 5-wav32k/                    # 32kHz 音频 (180个.wav)
├── 6-name2semantic-0.tsv        # 语义 token 映射
├── logs_s2_v2/                  # SoVITS checkpoint 目录
├── SoVITS_weights_v2/           # SoVITS 训练权重保存目录
│   └── ZhuangFangyi_V1-e*.pth   # 每 5 轮保存一次
├── GPT_ckpt_v2/                 # GPT checkpoint 目录
├── GPT_weights_v2/              # GPT 训练权重保存目录
│   └── ZhuangFangyi_V1-e*.ckpt  # 每 4 轮保存一次
├── training_all.log             # 完整训练日志
├── sovits_train.log             # SoVITS 训练日志
└── gpt_train.log                # GPT 训练日志
```

---

## 🔧 训练管理命令

### 启动训练（已自动启动）
```bash
cd /root/autodl-tmp/GPT-SoVITS
bash train_background.sh
```

### 监控训练状态
```bash
# 查看完整状态
bash monitor_training.sh

# 实时查看日志
tail -f logs/ZhuangFangyi_V1/training_all.log

# 查看 GPU 使用
watch -n 1 nvidia-smi
```

### 查看训练进程
```bash
ps aux | grep "run_training.py\|s2_train.py\|s1_train.py"
```

### 停止训练
```bash
# 读取保存的 PID
kill $(cat logs/ZhuangFangyi_V1/train.pid)

# 或者手动终止
pkill -9 -f "run_training.py"
```

### 启动 TensorBoard
```bash
tensorboard --logdir=logs/ZhuangFangyi_V1 --port=6006
```

---

## 📈 训练进度追踪

### SoVITS 训练
- **Epoch 1-5**: 探索阶段，Loss 快速下降
- **Epoch 5**: 第一个 checkpoint 保存
- **Epoch 6-10**: 稳定学习
- **Epoch 10**: 第二个 checkpoint 保存
- **Epoch 11-15**: 精细调整
- **Epoch 15**: 第三个 checkpoint 保存
- **Epoch 16-20**: 收敛阶段
- **Epoch 20**: 第四个 checkpoint 保存
- **Epoch 21-22**: 最终优化

### GPT 训练
- **Epoch 1-4**: 学习韵律和节奏，第一个 checkpoint
- **Epoch 5-8**: 学习语气和停顿，第二个 checkpoint
- **Epoch 9-12**: 精细化控制，第三个 checkpoint
- **Epoch 13-16**: 最终收敛，第四个 checkpoint

---

## ⚠️ 注意事项

1. **过拟合预防**:
   - SoVITS 22 轮：数据量 180 条，适中
   - GPT 16 轮：避免"复读机"现象
   - 定期检查验证集 Loss

2. **欠拟合检查**:
   - 如果 Loss 持续下降，可适当增加轮数
   - 观察 TensorBoard 曲线

3. **模型选择**:
   - 通常最后几个 epoch 的模型最好
   - 也可以测试中间 checkpoint (epoch 15, 20)

4. **后台运行**:
   - 训练使用 `nohup` 后台运行
   - SSH 断开不影响训练
   - 日志持续保存到文件

---

## 🎯 训练完成后

### 1. 检查模型文件
```bash
ls -lh logs/ZhuangFangyi_V1/SoVITS_weights_v2/
ls -lh logs/ZhuangFangyi_V1/GPT_weights_v2/
```

### 2. 模型测试
使用 WebUI 或 API 进行推理测试：
- SoVITS 模型: `logs/ZhuangFangyi_V1/SoVITS_weights_v2/ZhuangFangyi_V1-e22.pth`
- GPT 模型: `logs/ZhuangFangyi_V1/GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt`

### 3. 推理使用
在 WebUI 的推理页面加载以上模型进行测试。

---

## 📝 日志文件说明

- **training_all.log**: 完整训练日志，包含配置信息、训练进度、错误信息
- **sovits_train.log**: SoVITS 详细训练日志，包含每个 batch 的 Loss
- **gpt_train.log**: GPT 详细训练日志，包含验证集性能
- **TensorBoard logs**: 可视化训练曲线（Loss、学习率、音频对比等）

---

## 🚀 优化说明

相比推荐参数的调整：

1. **Batch Size**: 
   - 推荐: 12-16
   - 实际: SoVITS 14, GPT 12
   - 原因: 平衡速度和稳定性

2. **Epochs**:
   - 推荐: SoVITS 20, GPT 15
   - 实际: SoVITS 22, GPT 16
   - 原因: 180 条数据，略微增加训练充分度

3. **基底模型**:
   - 使用: v2-276h (276小时高质量数据)
   - 优势: 更强的泛化能力和音质

---

**训练时间**: 2025-02-09 18:31  
**预计完成**: 2025-02-09 19:15 (约 45 分钟)  
**状态**: ✅ 运行中，可安全断开 SSH
