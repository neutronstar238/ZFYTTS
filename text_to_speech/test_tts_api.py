#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS API 测试脚本
演示如何使用 TTS REST API
"""

import requests
import json
import time

# API 基础 URL
BASE_URL = "http://localhost:5001"


def test_health_check():
    """测试健康检查"""
    print("=== 测试健康检查 ===")
    response = requests.get(f"{BASE_URL}/api/tts/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_get_info():
    """测试获取系统信息"""
    print("=== 测试获取系统信息 ===")
    response = requests.get(f"{BASE_URL}/api/tts/info")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_single_generation():
    """测试单个语音生成"""
    print("=== 测试单个语音生成 ===")
    
    data = {
        "text": "管理员，好久不见。不用太拘谨，像从前一样，随意称呼就好。",
        "speed": 1.0,
        "top_k": 15,
        "temperature": 1.0
    }
    
    print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/api/tts/generate",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    elapsed_time = time.time() - start_time
    
    print(f"状态码: {response.status_code}")
    print(f"请求耗时: {elapsed_time:.2f}s")
    
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get('success'):
        audio_url = result['data']['audio_url']
        filename = result['data']['filename']
        print(f"\n✅ 生成成功!")
        print(f"   文件名: {filename}")
        print(f"   访问地址: {BASE_URL}{audio_url}")
        print(f"   本地路径: {result['data']['audio_path']}")
        
        # 可以下载音频文件
        # audio_response = requests.get(f"{BASE_URL}{audio_url}")
        # with open(f"downloaded_{filename}", 'wb') as f:
        #     f.write(audio_response.content)
        # print(f"   已下载到: downloaded_{filename}")
    
    print()


def test_batch_generation():
    """测试批量语音生成"""
    print("=== 测试批量语音生成 ===")
    
    data = {
        "texts": [
            "你好，我是庄方宜。",
            "今天天气真不错。",
            "很高兴见到你。"
        ],
        "speed": 1.0,
        "top_k": 15
    }
    
    print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/api/tts/batch",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    elapsed_time = time.time() - start_time
    
    print(f"状态码: {response.status_code}")
    print(f"请求耗时: {elapsed_time:.2f}s")
    
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    if result.get('success'):
        data = result['data']
        print(f"\n✅ 批量生成完成!")
        print(f"   总数: {data['total']}")
        print(f"   成功: {data['succeeded']}")
        print(f"   失败: {data['failed']}")
    
    print()


def test_list_files():
    """测试列出文件"""
    print("=== 测试列出文件 ===")
    
    response = requests.get(f"{BASE_URL}/api/tts/files?limit=5")
    print(f"状态码: {response.status_code}")
    
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    print()


def test_custom_parameters():
    """测试自定义参数"""
    print("=== 测试自定义参数 ===")
    
    data = {
        "text": "这是一段测试语音，使用了自定义参数。",
        "speed": 1.2,  # 加快语速
        "temperature": 0.8,  # 降低随机性
        "filename": "custom_test.wav"  # 自定义文件名
    }
    
    print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(
        f"{BASE_URL}/api/tts/generate",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    print()


def main():
    """运行所有测试"""
    print("=" * 70)
    print("TTS API 测试")
    print("=" * 70)
    print()
    
    try:
        # 1. 健康检查
        test_health_check()
        
        # 2. 获取系统信息
        test_get_info()
        
        # 3. 单个语音生成
        test_single_generation()
        
        # 4. 自定义参数
        test_custom_parameters()
        
        # 5. 批量生成
        test_batch_generation()
        
        # 6. 列出文件
        test_list_files()
        
        print("=" * 70)
        print("✅ 所有测试完成!")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到 API 服务器")
        print("请确保 API 服务器正在运行:")
        print("  python tts_api.py")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
