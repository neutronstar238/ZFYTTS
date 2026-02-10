#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本 - 在部署前运行，检查环境是否满足要求
"""

import sys
import os

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 9 or version.minor > 12:
        print("❌ Python 版本不符合要求（需要 3.9-3.12）")
        return False
    print("✅ Python 版本正常")
    return True

def check_dependencies():
    """检查关键依赖"""
    required = ['torch', 'torchaudio', 'soundfile', 'transformers', 'pypinyin']
    missing = []
    
    print("\n检查关键依赖...")
    for module in required:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module} (缺失)")
            missing.append(module)
    
    if missing:
        print(f"\n缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    return True

def check_model_files():
    """检查模型文件"""
    print("\n检查模型文件...")
    
    files = [
        ("GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt", "GPT 模型"),
        ("SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth", "SoVITS 模型"),
        ("logs/ZhuangFangyi_V1/reference_audio/zfy_raw_vocals.wav_0011840000_0012000960.wav", "参考音频")
    ]
    
    all_exist = True
    for file_path, name in files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) / (1024*1024)
            print(f"  ✅ {name} ({size:.1f} MB)")
        else:
            print(f"  ❌ {name} (不存在)")
            all_exist = False
    
    return all_exist

def check_cuda():
    """检查 CUDA 支持"""
    print("\n检查 GPU 支持...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  ✅ CUDA 可用")
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("  ⚠️  CUDA 不可用，将使用 CPU 推理（速度较慢）")
    except:
        print("  ⚠️  无法检查 CUDA 状态")

def main():
    print("=" * 60)
    print("庄方宜 TTS - 环境检查")
    print("=" * 60)
    print()
    
    results = []
    results.append(("Python 版本", check_python_version()))
    results.append(("依赖库", check_dependencies()))
    results.append(("模型文件", check_model_files()))
    check_cuda()
    
    print("\n" + "=" * 60)
    if all(r[1] for r in results):
        print("✅ 所有检查通过，环境准备完毕！")
        print("\n可以开始使用：")
        print("  python simple_tts.py '你的文本'")
        print("  python web_server.py --port 8080")
    else:
        print("❌ 环境检查未通过，请解决上述问题")
        for name, result in results:
            if not result:
                print(f"  - {name} 需要修复")
    print("=" * 60)

if __name__ == "__main__":
    main()
