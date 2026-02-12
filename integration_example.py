#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成示例: LLM Chat + TTS
演示如何将聊天机器人的文字回复转换为语音
"""

import sys
import os
import requests
import json

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'LLMchat'))

from LLMchat.chat_manager import ChatBot


class VoiceAssistant:
    """语音助手 - 集成 LLM 和 TTS"""
    
    def __init__(self, 
                 llm_model_path="LLMchat/zhuang_fangyi_int4.gguf",
                 tts_api_url="http://localhost:5001"):
        """
        初始化语音助手
        
        Args:
            llm_model_path: LLM 模型路径
            tts_api_url: TTS API 服务地址
        """
        print("🤖 初始化语音助手...")
        
        # 初始化 LLM
        print("📚 加载 LLM 模型...")
        self.chatbot = ChatBot(llm_model_path)
        
        # TTS API 配置
        self.tts_api_url = tts_api_url
        
        print("✅ 语音助手初始化完成!\n")
    
    def chat_with_voice(self, 
                       user_input: str,
                       user_id: str = "default_user",
                       session_id: str = None,
                       generate_audio: bool = True,
                       tts_speed: float = 1.0) -> dict:
        """
        与语音助手对话
        
        Args:
            user_input: 用户输入文本
            user_id: 用户 ID
            session_id: 会话 ID
            generate_audio: 是否生成语音
            tts_speed: 语速
            
        Returns:
            包含文字回复和音频信息的字典
        """
        # 1. 获取 LLM 文字回复
        print(f"💬 用户: {user_input}")
        print("🤔 思考中...")
        
        chat_result = self.chatbot.chat(
            user_input=user_input,
            user_id=user_id,
            session_id=session_id
        )
        
        text_response = chat_result['response']
        print(f"💭 助手: {text_response}")
        
        result = {
            'text_response': text_response,
            'session_id': chat_result['session_id'],
            'user_id': chat_result['user_id'],
            'audio_generated': False
        }
        
        # 2. 生成语音（如果需要）
        if generate_audio:
            print("🎤 生成语音中...")
            
            try:
                tts_response = requests.post(
                    f"{self.tts_api_url}/api/tts/generate",
                    json={
                        "text": text_response,
                        "speed": tts_speed
                    },
                    timeout=60
                )
                
                if tts_response.status_code == 200:
                    tts_data = tts_response.json()
                    
                    if tts_data.get('success'):
                        audio_info = tts_data['data']
                        result['audio_generated'] = True
                        result['audio_path'] = audio_info['audio_path']
                        result['audio_url'] = f"{self.tts_api_url}{audio_info['audio_url']}"
                        result['audio_filename'] = audio_info['filename']
                        result['audio_duration'] = audio_info.get('duration')
                        
                        print(f"🔊 语音已生成: {audio_info['filename']}")
                        print(f"   访问地址: {result['audio_url']}")
                    else:
                        print(f"⚠️ TTS 生成失败: {tts_data.get('error')}")
                else:
                    print(f"⚠️ TTS API 请求失败: {tts_response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("⚠️ 无法连接到 TTS API 服务器")
                print("   请确保 TTS API 正在运行: python text_to_speech/tts_api.py")
            except Exception as e:
                print(f"⚠️ TTS 生成错误: {e}")
        
        return result
    
    def interactive_mode(self):
        """交互模式"""
        print("\n" + "=" * 60)
        print("🎙️  语音助手交互模式")
        print("=" * 60)
        print("命令:")
        print("  /voice on  - 开启语音生成")
        print("  /voice off - 关闭语音生成")
        print("  /new       - 开始新会话")
        print("  /quit      - 退出")
        print("=" * 60)
        
        user_id = input("\n请输入用户 ID (回车使用默认): ").strip() or "default_user"
        session_id = None
        generate_audio = True
        
        print(f"\n👤 当前用户: {user_id}")
        print(f"🔊 语音生成: {'开启' if generate_audio else '关闭'}\n")
        
        while True:
            try:
                user_input = input(f"[{user_id}] 你: ").strip()
                
                if not user_input:
                    continue
                
                # 处理命令
                if user_input.startswith('/'):
                    cmd = user_input.lower()
                    
                    if cmd == '/quit':
                        print("👋 再见!")
                        break
                    
                    elif cmd == '/new':
                        session_id = None
                        print("✨ 已开始新会话")
                        continue
                    
                    elif cmd == '/voice on':
                        generate_audio = True
                        print("🔊 语音生成已开启")
                        continue
                    
                    elif cmd == '/voice off':
                        generate_audio = False
                        print("🔇 语音生成已关闭")
                        continue
                    
                    else:
                        print(f"❓ 未知命令: {cmd}")
                        continue
                
                # 处理对话
                result = self.chat_with_voice(
                    user_input=user_input,
                    user_id=user_id,
                    session_id=session_id,
                    generate_audio=generate_audio
                )
                
                session_id = result['session_id']
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 再见!")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='语音助手 - LLM + TTS 集成')
    parser.add_argument('--llm-model', type=str, 
                       default='LLMchat/zhuang_fangyi_int4.gguf',
                       help='LLM 模型路径')
    parser.add_argument('--tts-api', type=str,
                       default='http://localhost:5001',
                       help='TTS API 地址')
    parser.add_argument('--text', type=str,
                       help='直接输入文本（非交互模式）')
    parser.add_argument('--no-audio', action='store_true',
                       help='不生成语音')
    
    args = parser.parse_args()
    
    # 初始化助手
    assistant = VoiceAssistant(
        llm_model_path=args.llm_model,
        tts_api_url=args.tts_api
    )
    
    # 非交互模式
    if args.text:
        result = assistant.chat_with_voice(
            user_input=args.text,
            generate_audio=not args.no_audio
        )
        
        print("\n" + "=" * 60)
        print("结果:")
        print(f"  文字回复: {result['text_response']}")
        if result['audio_generated']:
            print(f"  音频文件: {result['audio_path']}")
            print(f"  访问地址: {result['audio_url']}")
        print("=" * 60)
    
    # 交互模式
    else:
        assistant.interactive_mode()


if __name__ == "__main__":
    main()
