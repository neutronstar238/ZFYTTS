#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""完整集成测试: LLM Chat + TTS"""

import requests
import json

print("=" * 70)
print("集成测试: LLM Chat + TTS")
print("=" * 70)

# 步骤 1: 与 LLM 对话
print("\n步骤 1: 与 LLM 对话")
print("-" * 70)

user_message = "你好"  # 使用更短的输入
print(f"用户: {user_message}")
print("⏳ 等待 LLM 响应（可能需要 1-2 分钟，请耐心等待）...")

chat_response = requests.post(
    "http://localhost:5000/api/chat",
    json={
        "message": user_message,
        "user_id": "integration_test"
    },
    timeout=180  # 增加到 3 分钟
)

if chat_response.status_code == 200:
    chat_data = chat_response.json()
    if chat_data.get('success'):
        llm_reply = chat_data['data']['response']
        session_id = chat_data['data']['session_id']
        
        print(f"LLM: {llm_reply[:100]}{'...' if len(llm_reply) > 100 else ''}")
        print(f"会话ID: {session_id}")
        
        # 步骤 2: 将 LLM 回复转为语音
        print("\n步骤 2: 将 LLM 回复转为语音")
        print("-" * 70)
        
        # 截取前30个字符用于TTS（避免太长）
        tts_text = llm_reply[:30] if len(llm_reply) > 30 else llm_reply
        print(f"TTS 文本: {tts_text}")
        print("⏳ 生成语音中...")
        
        tts_response = requests.post(
            "http://localhost:5001/api/tts/generate",
            json={
                "text": tts_text,
                "speed": 1.0
            },
            timeout=120  # 增加到 2 分钟
        )
        
        if tts_response.status_code == 200:
            tts_data = tts_response.json()
            if tts_data.get('success'):
                audio_info = tts_data['data']
                
                print(f"✅ 语音生成成功!")
                print(f"   文件名: {audio_info['filename']}")
                print(f"   路径: {audio_info['audio_path']}")
                print(f"   时长: {audio_info.get('duration', 'N/A')} 秒")
                print(f"   访问地址: http://localhost:5001{audio_info['audio_url']}")
                
                print("\n" + "=" * 70)
                print("✅ 集成测试成功!")
                print("=" * 70)
                print("\n总结:")
                print(f"1. LLM 成功生成回复 ({len(llm_reply)} 字符)")
                print(f"2. TTS 成功生成语音 ({audio_info.get('duration', 'N/A')} 秒)")
                print(f"3. 会话已保存 (ID: {session_id[:8]}...)")
            else:
                print(f"❌ TTS 生成失败: {tts_data.get('error')}")
        else:
            print(f"❌ TTS API 请求失败: {tts_response.status_code}")
    else:
        print(f"❌ LLM 对话失败: {chat_data.get('error')}")
else:
    print(f"❌ LLM API 请求失败: {chat_response.status_code}")
