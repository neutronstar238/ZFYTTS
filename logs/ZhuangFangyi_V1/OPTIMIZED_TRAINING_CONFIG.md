# 🚀 优化训练配置 - 庄方宜语音模型

## ✅ 当前使用参数（优化版）

### SoVITS 训练（音色模型）
- **Batch Size**: **24** ← 从 14 提升到 24
  - 理由：48GB 显存充足，更大批次 = 音色更稳定，减少电流麦
- **Total Epochs**: **20**
- **Save Frequency**: 每 5 轮保存
- **基底模型**: GPT-SoVITS-v2-276h (s2G2333k.pth)

### GPT 训练（韵律/语气模型）
- **Batch Size**: **24** ← 从 12 提升到 24
  - 理由：48GB 显存充足，更大批次 = 训练更稳定
- **Total Epochs**: **15** ← 从 16 降到 15
  - 理由：15 轮是经验黄金值，避免"复读机"现象
- **Save Frequency**: 每 5 轮保存
- **基底模型**: GPT-SoVITS-v2-276h (s1bert25hz-5kh-longer)

## 📊 参数优化说明

### 为什么 Batch Size 越大越好？
1. **音色稳定性**：更大的批次让模型看到更多样化的数据，学习到的音色特征更鲁棒
2. **减少电流麦**：小批次容易导致训练不稳定，产生电流音/杂音
3. **训练速度**：48GB 显存完全可以支持更大批次，充分利用硬件

### 参数对比

| 参数 | 保守配置 | **优化配置** | 效果提升 |
|------|---------|------------|---------|
| SoVITS Batch | 14 | **24** | 音色更稳定，减少电流麦 |
| SoVITS Epochs | 22 | **20** | 避免过拟合 |
| GPT Batch | 12 | **24** | 训练更稳定 |
| GPT Epochs | 16 | **15** | 最佳韵律，避免复读机 |

## 🔥 GPU 使用情况

训练中实时监控：
- **显存占用**: 10.4GB / 48GB（仅 21%）
- **GPU 利用率**: 68%
- **功耗**: 151W / 450W
- **温度**: 46°C（非常健康）

**结论**：显存还有大量余量，Batch Size 24 完全合理，甚至可以更大！

## 📈 预期训练时间

- **SoVITS**: 20 轮 × 12-15 秒/轮 ≈ **4-5 分钟**
- **GPT**: 15 轮 × 15-20 秒/轮 ≈ **4-5 分钟**
- **总计**: 约 **8-10 分钟**

（比之前的配置快约 30%）

## 📁 模型保存路径

### SoVITS 权重
- `logs/ZhuangFangyi_V1/SoVITS_weights_v2/ZhuangFangyi_V1_e5.pth`
- `logs/ZhuangFangyi_V1/SoVITS_weights_v2/ZhuangFangyi_V1_e10.pth`
- `logs/ZhuangFangyi_V1/SoVITS_weights_v2/ZhuangFangyi_V1_e15.pth`
- `logs/ZhuangFangyi_V1/SoVITS_weights_v2/ZhuangFangyi_V1_e20.pth` ⭐

### GPT 权重
- `logs/ZhuangFangyi_V1/GPT_weights_v2/ZhuangFangyi_V1-e5.ckpt`
- `logs/ZhuangFangyi_V1/GPT_weights_v2/ZhuangFangyi_V1-e10.ckpt`
- `logs/ZhuangFangyi_V1/GPT_weights_v2/ZhuangFangyi_V1-e15.ckpt` ⭐

## 💡 使用建议

1. **推荐模型组合**:
   - SoVITS: `ZhuangFangyi_V1_e15.pth` 或 `e20.pth`
   - GPT: `ZhuangFangyi_V1-e15.ckpt`

2. **测试方法**:
   - 先测试 e15，如果音色不够可以试 e20
   - GPT 建议使用最终版 e15（避免过拟合）

3. **问题排查**:
   - 如果有电流音 → 使用更后期的 checkpoint（e15-e20）
   - 如果语气不对 → 调整 GPT 的 top_p/top_k 参数
   - 如果复读机 → 使用 e10 或 e5 的 GPT 模型

---

**配置更新时间**: 2026-02-09 18:44  
**训练状态**: 进行中（Epoch 16/20）  
**预计完成**: 18:50
