#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
庄方宜 TTS - 简易命令行工具
用法：python simple_tts.py "你好，这是测试文本"
"""

import os
import sys
import argparse
from pathlib import Path

# 必须在导入 torch 和其他模块之前设置环境变量
os.environ["version"] = "v2Pro"
os.environ["is_half"] = "True"  # GPU 上使用半精度加速
now_dir = os.getcwd()
sys.path.insert(0, now_dir)
# 添加 GPT_SoVITS 到 sys.path，以便 torch.load 能找到 utils 模块
sys.path.insert(0, os.path.join(now_dir, "GPT_SoVITS"))

import torch

class ZhuangFangyiTTS:
    def __init__(self):
        """初始化 TTS 模型"""
        print("🎤 正在加载庄方宜语音模型...")
        
        # 配置路径
        self.gpt_model_path = "GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt"
        self.sovits_model_path = "SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth"
        
        # 默认参考音频（内置引子）
        self.reference_audio = "logs/ZhuangFangyi_V1/reference_audio/zfy_raw_vocals.wav_0011840000_0012000960.wav"
        self.reference_text = "不用太拘谨，像从前一样，随意称呼就好"
        
        # 检查模型文件
        if not os.path.exists(self.gpt_model_path):
            raise FileNotFoundError(f"GPT 模型未找到: {self.gpt_model_path}")
        if not os.path.exists(self.sovits_model_path):
            raise FileNotFoundError(f"SoVITS 模型未找到: {self.sovits_model_path}")
        if not os.path.exists(self.reference_audio):
            raise FileNotFoundError(f"参考音频未找到: {self.reference_audio}")
        
        # 导入推理模块
        from GPT_SoVITS.inference_webui import get_tts_wav, change_sovits_weights, change_gpt_weights
        
        self.get_tts_wav = get_tts_wav
        
        # 加载模型
        print("📦 加载 GPT 模型...")
        change_gpt_weights(self.gpt_model_path)
        
        print("📦 加载 SoVITS 模型...")
        # change_sovits_weights 是生成器，需要遍历执行
        # 传入语言参数以避免未初始化的变量错误
        for _ in change_sovits_weights(self.sovits_model_path, prompt_language="中文", text_language="中文"):
            pass
        
        print("✅ 模型加载完成！\n")
    
    def generate(self, text, output_path=None, reference_audio=None, reference_text=None,
                 top_k=15, top_p=1.0, temperature=1.0, speed=1.0):
        """
        生成语音
        
        参数:
            text: 要合成的文本
            output_path: 输出文件路径（默认自动生成）
            reference_audio: 参考音频路径（默认使用内置）
            reference_text: 参考文本（默认使用内置）
            top_k: GPT 采样参数
            top_p: GPT 采样参数
            temperature: GPT 采样参数
            speed: 语速调节
        
        返回:
            生成的音频文件路径
        """
        
        # 使用默认参考音频
        ref_audio = reference_audio or self.reference_audio
        ref_text = reference_text or self.reference_text
        
        # 生成输出路径
        if output_path is None:
            os.makedirs("outputs", exist_ok=True)
            import time
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"outputs/zfy_{timestamp}.wav"
        
        print(f"🎯 开始合成: {text[:30]}{'...' if len(text) > 30 else ''}")
        print(f"📝 参考文本: {ref_text[:30]}{'...' if len(ref_text) > 30 else ''}")
        
        try:
            # 调用推理函数
            result = self.get_tts_wav(
                ref_wav_path=ref_audio,
                prompt_text=ref_text,
                prompt_language="中文",  # 使用中文键名
                text=text,
                text_language="中文",  # 使用中文键名
                how_to_cut="不切",
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                ref_free=False,
                speed=speed,
                if_freeze=""
            )
            
            # 获取生成的音频
            for sr, audio_data in result:
                if audio_data is not None:
                    # 保存音频
                    import soundfile as sf
                    sf.write(output_path, audio_data, sr)
                    print(f"✅ 音频已保存: {output_path}")
                    return output_path
            
            raise RuntimeError("生成失败，没有返回音频数据")
            
        except Exception as e:
            print(f"❌ 生成失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def batch_generate(self, texts, output_dir="outputs"):
        """批量生成语音"""
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for i, text in enumerate(texts, 1):
            print(f"\n[{i}/{len(texts)}] 处理中...")
            output_path = os.path.join(output_dir, f"zfy_{i:03d}.wav")
            result = self.generate(text, output_path)
            results.append(result)
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="庄方宜 TTS 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单句生成
  python simple_tts.py "管理员，好久不见"
  
  # 指定输出文件
  python simple_tts.py "你好世界" -o hello.wav
  
  # 批量生成（从文件读取）
  python simple_tts.py -f texts.txt
  
  # 调整语速和参数
  python simple_tts.py "快点说话" --speed 1.2 --temperature 0.8
        """
    )
    
    parser.add_argument("text", nargs="?", help="要合成的文本")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-f", "--file", help="从文件读取文本（每行一句）")
    parser.add_argument("--ref-audio", help="参考音频路径（覆盖默认）")
    parser.add_argument("--ref-text", help="参考文本（覆盖默认）")
    parser.add_argument("--speed", type=float, default=1.0, help="语速 (0.5-2.0)")
    parser.add_argument("--top-k", type=int, default=15, help="GPT top_k")
    parser.add_argument("--top-p", type=float, default=1.0, help="GPT top_p")
    parser.add_argument("--temperature", type=float, default=1.0, help="GPT temperature")
    
    args = parser.parse_args()
    
    # 参数验证
    if not args.text and not args.file:
        parser.print_help()
        sys.exit(1)
    
    try:
        # 初始化 TTS
        tts = ZhuangFangyiTTS()
        
        # 批量处理
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
            print(f"📄 从文件读取了 {len(texts)} 行文本\n")
            tts.batch_generate(texts)
        
        # 单句处理
        elif args.text:
            tts.generate(
                text=args.text,
                output_path=args.output,
                reference_audio=args.ref_audio,
                reference_text=args.ref_text,
                top_k=args.top_k,
                top_p=args.top_p,
                temperature=args.temperature,
                speed=args.speed
            )
        
        print("\n🎉 全部完成！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
