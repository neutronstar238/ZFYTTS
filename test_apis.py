#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 测试脚本
测试 LLM Chat API 和 TTS API 的基本功能
"""

import requests
import json
import time

def test_llm_api():
    """测试 LLM Chat API"""
    print("\n" + "=" * 70)
    print("测试 LLM Chat API (http://localhost:5000)")
    print("=" * 70)
    
    # 健康检查
    print("\n1. 健康检查...")
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"   ✅ 状态: {response.json()['status']}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False
    
    # 对话测试
    print("\n2. 对话测试...")
    print("   问题: 你好，请介绍一下你自己")
    print("   ⏳ 等待回复（约1-2分钟）...")
    try:
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={
                "message": "你好，请介绍一下你自己",
                "user_id": "test_user"
            },
            timeout=180
        )
        result = response.json()
        if result.get('success'):
            reply = result['data']['response']
            print(f"   ✅ 回复: {reply[:100]}{'...' if len(reply) > 100 else ''}")
            print(f"   会话ID: {result['data']['session_id'][:16]}...")
            return True
        else:
            print(f"   ❌ 错误: {result.get('error')}")
            return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False


def test_tts_api():
    """测试 TTS API"""
    print("\n" + "=" * 70)
    print("测试 TTS API (http://localhost:5001)")
    print("=" * 70)
    
    # 健康检查
    print("\n1. 健康检查...")
    try:
        response = requests.get("http://localhost:5001/api/tts/health", timeout=5)
        print(f"   ✅ 状态: {response.json()['status']}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False
    
    # 语音生成测试
    print("\n2. 语音生成测试...")
    print("   文本: 你好，这是一个测试")
    print("   ⏳ 生成中...")
    try:
        response = requests.post(
            "http://localhost:5001/api/tts/generate",
            json={
                "text": "你好，这是一个测试",
                "speed": 1.0
            },
            timeout=60
        )
        result = response.json()
        if result.get('success'):
            data = result['data']
            print(f"   ✅ 生成成功!")
            print(f"   文件: {data['filename']}")
            print(f"   时长: {data.get('duration', 'N/A')} 秒")
            print(f"   URL: http://localhost:5001{data['audio_url']}")
            return True
        else:
            print(f"   ❌ 错误: {result.get('error')}")
            return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 70)
    print("智能语音助手 API 测试")
    print("=" * 70)
    
    llm_ok = test_llm_api()
    tts_ok = test_tts_api()
    
    print("\n" + "=" * 70)
    print("测试结果总结")
    print("=" * 70)
    print(f"LLM Chat API: {'✅ 通过' if llm_ok else '❌ 失败'}")
    print(f"TTS API:      {'✅ 通过' if tts_ok else '❌ 失败'}")
    print("=" * 70)
    
    if llm_ok and tts_ok:
        print("\n🎉 所有测试通过！系统运行正常。")
    else:
        print("\n⚠️ 部分测试失败，请检查服务是否正常运行。")


if __name__ == "__main__":
    main()
