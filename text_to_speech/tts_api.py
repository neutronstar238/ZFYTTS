#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-to-Speech REST API Service
Provides RESTful API endpoints for TTS generation
"""

import os
import sys
import json
import time
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# ============================================
# 配置项
# ============================================

# GPU 配置
USE_GPU = True  # 设置为 False 使用 CPU
USE_HALF_PRECISION = True  # GPU 半精度加速（仅GPU模式有效）

# 设置环境变量
os.environ["version"] = "v2Pro"
os.environ["is_half"] = "True" if (USE_GPU and USE_HALF_PRECISION) else "False"

# ============================================
# 初始化
# ============================================

now_dir = os.getcwd()
sys.path.insert(0, now_dir)
sys.path.insert(0, os.path.join(now_dir, "GPT_SoVITS"))

# 导入 TTS 模块
from simple_tts import ZhuangFangyiTTS

app = Flask(__name__)
CORS(app)

# 全局 TTS 实例
tts_instance = None
OUTPUT_DIR = "outputs"

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 打印配置信息
print("=" * 70)
print("TTS API 配置:")
print(f"  GPU 加速: {'✅ 启用' if USE_GPU else '❌ 禁用'}")
if USE_GPU:
    print(f"  半精度: {'✅ 启用' if USE_HALF_PRECISION else '❌ 禁用'}")
print("=" * 70)


def get_tts():
    """获取或初始化 TTS 实例（单例模式）"""
    global tts_instance
    if tts_instance is None:
        print("🎤 初始化 TTS 模型...")
        tts_instance = ZhuangFangyiTTS()
        print("✅ TTS 模型加载完成")
    return tts_instance


@app.route('/api/tts/generate', methods=['POST'])
def generate_speech():
    """
    生成语音 API
    
    Request Body (JSON):
    {
        "text": "要合成的文本",
        "speed": 1.0,           // 可选，语速 (0.5-2.0)
        "top_k": 15,            // 可选，GPT采样参数
        "top_p": 1.0,           // 可选，GPT采样参数
        "temperature": 1.0,     // 可选，GPT采样参数
        "reference_audio": "",  // 可选，自定义参考音频路径
        "reference_text": "",   // 可选，自定义参考文本
        "filename": ""          // 可选，自定义输出文件名
    }
    
    Response (JSON):
    {
        "success": true,
        "data": {
            "audio_path": "outputs/xxx.wav",
            "filename": "xxx.wav",
            "audio_url": "/api/tts/audio/xxx.wav",
            "text": "原始文本",
            "duration": 3.5,
            "generated_at": "2026-02-12T19:30:00"
        }
    }
    """
    try:
        # 解析请求数据
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必需参数: text'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': '文本不能为空'
            }), 400
        
        # 获取可选参数
        speed = float(data.get('speed', 1.0))
        top_k = int(data.get('top_k', 15))
        top_p = float(data.get('top_p', 1.0))
        temperature = float(data.get('temperature', 1.0))
        reference_audio = data.get('reference_audio')
        reference_text = data.get('reference_text')
        custom_filename = data.get('filename')
        
        # 参数验证
        if not (0.5 <= speed <= 2.0):
            return jsonify({
                'success': False,
                'error': 'speed 参数必须在 0.5 到 2.0 之间'
            }), 400
        
        # 生成输出文件名
        if custom_filename:
            filename = secure_filename(custom_filename)
            if not filename.endswith('.wav'):
                filename += '.wav'
        else:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"tts_{timestamp}_{unique_id}.wav"
        
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        print(f"📝 TTS 请求: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # 获取 TTS 实例并生成音频
        tts = get_tts()
        start_time = time.time()
        
        result_path = tts.generate(
            text=text,
            output_path=output_path,
            reference_audio=reference_audio,
            reference_text=reference_text,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            speed=speed
        )
        
        generation_time = time.time() - start_time
        
        if result_path and os.path.exists(result_path):
            # 获取音频时长
            try:
                import soundfile as sf
                audio_data, sample_rate = sf.read(result_path)
                duration = len(audio_data) / sample_rate
            except Exception:
                duration = None
            
            print(f"✅ 生成成功: {filename} (耗时: {generation_time:.2f}s)")
            
            return jsonify({
                'success': True,
                'data': {
                    'audio_path': result_path,
                    'filename': filename,
                    'audio_url': f'/api/tts/audio/{filename}',
                    'text': text,
                    'duration': duration,
                    'generation_time': round(generation_time, 2),
                    'generated_at': time.strftime("%Y-%m-%dT%H:%M:%S")
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': '音频生成失败'
            }), 500
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tts/audio/<filename>', methods=['GET'])
def get_audio(filename):
    """
    获取生成的音频文件
    
    URL: /api/tts/audio/<filename>
    Method: GET
    
    Returns: 音频文件 (audio/wav)
    """
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        return send_file(
            file_path,
            mimetype='audio/wav',
            as_attachment=False,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tts/batch', methods=['POST'])
def batch_generate():
    """
    批量生成语音 API
    
    Request Body (JSON):
    {
        "texts": ["文本1", "文本2", "文本3"],
        "speed": 1.0,
        "top_k": 15,
        "top_p": 1.0,
        "temperature": 1.0
    }
    
    Response (JSON):
    {
        "success": true,
        "data": {
            "total": 3,
            "succeeded": 3,
            "failed": 0,
            "results": [
                {
                    "index": 0,
                    "text": "文本1",
                    "success": true,
                    "audio_path": "outputs/xxx.wav",
                    "filename": "xxx.wav",
                    "audio_url": "/api/tts/audio/xxx.wav"
                },
                ...
            ]
        }
    }
    """
    try:
        data = request.json
        
        if not data or 'texts' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必需参数: texts'
            }), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list) or not texts:
            return jsonify({
                'success': False,
                'error': 'texts 必须是非空数组'
            }), 400
        
        # 获取可选参数
        speed = float(data.get('speed', 1.0))
        top_k = int(data.get('top_k', 15))
        top_p = float(data.get('top_p', 1.0))
        temperature = float(data.get('temperature', 1.0))
        
        print(f"📦 批量生成请求: {len(texts)} 条文本")
        
        # 获取 TTS 实例
        tts = get_tts()
        
        results = []
        succeeded = 0
        failed = 0
        
        for idx, text in enumerate(texts):
            text = text.strip()
            
            if not text:
                results.append({
                    'index': idx,
                    'text': text,
                    'success': False,
                    'error': '文本为空'
                })
                failed += 1
                continue
            
            try:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"batch_{timestamp}_{idx:03d}.wav"
                output_path = os.path.join(OUTPUT_DIR, filename)
                
                result_path = tts.generate(
                    text=text,
                    output_path=output_path,
                    top_k=top_k,
                    top_p=top_p,
                    temperature=temperature,
                    speed=speed
                )
                
                if result_path and os.path.exists(result_path):
                    results.append({
                        'index': idx,
                        'text': text,
                        'success': True,
                        'audio_path': result_path,
                        'filename': filename,
                        'audio_url': f'/api/tts/audio/{filename}'
                    })
                    succeeded += 1
                else:
                    results.append({
                        'index': idx,
                        'text': text,
                        'success': False,
                        'error': '生成失败'
                    })
                    failed += 1
                    
            except Exception as e:
                results.append({
                    'index': idx,
                    'text': text,
                    'success': False,
                    'error': str(e)
                })
                failed += 1
        
        print(f"✅ 批量生成完成: 成功 {succeeded}, 失败 {failed}")
        
        return jsonify({
            'success': True,
            'data': {
                'total': len(texts),
                'succeeded': succeeded,
                'failed': failed,
                'results': results
            }
        })
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tts/files', methods=['GET'])
def list_files():
    """
    列出所有生成的音频文件
    
    Query Parameters:
        - limit: 返回数量限制（默认100）
        - offset: 偏移量（默认0）
    
    Response (JSON):
    {
        "success": true,
        "data": {
            "total": 10,
            "files": [
                {
                    "filename": "xxx.wav",
                    "path": "outputs/xxx.wav",
                    "url": "/api/tts/audio/xxx.wav",
                    "size": 123456,
                    "created_at": "2026-02-12T19:30:00"
                },
                ...
            ]
        }
    }
    """
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        files = []
        
        if os.path.exists(OUTPUT_DIR):
            for filename in sorted(os.listdir(OUTPUT_DIR), reverse=True):
                if filename.endswith('.wav'):
                    file_path = os.path.join(OUTPUT_DIR, filename)
                    stat = os.stat(file_path)
                    
                    files.append({
                        'filename': filename,
                        'path': file_path,
                        'url': f'/api/tts/audio/{filename}',
                        'size': stat.st_size,
                        'created_at': time.strftime(
                            "%Y-%m-%dT%H:%M:%S",
                            time.localtime(stat.st_ctime)
                        )
                    })
        
        total = len(files)
        files = files[offset:offset + limit]
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'files': files
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tts/health', methods=['GET'])
def health_check():
    """
    健康检查端点
    
    Response (JSON):
    {
        "status": "healthy",
        "model_loaded": true,
        "output_dir": "outputs"
    }
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': tts_instance is not None,
        'output_dir': OUTPUT_DIR,
        'version': 'v2Pro'
    })


@app.route('/api/tts/info', methods=['GET'])
def get_info():
    """
    获取 TTS 系统信息
    
    Response (JSON):
    {
        "success": true,
        "data": {
            "model_version": "v2Pro",
            "gpt_model": "GPT_weights_v2/ZhuangFangyi_V1-e16.ckpt",
            "sovits_model": "SoVITS_weights_v2/ZhuangFangyi_V1_e20_s300.pth",
            "reference_audio": "logs/ZhuangFangyi_V1/reference_audio/...",
            "reference_text": "不用太拘谨，像从前一样，随意称呼就好"
        }
    }
    """
    try:
        tts = get_tts()
        
        return jsonify({
            'success': True,
            'data': {
                'model_version': 'v2Pro',
                'gpt_model': tts.gpt_model_path,
                'sovits_model': tts.sovits_model_path,
                'reference_audio': tts.reference_audio,
                'reference_text': tts.reference_text
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'success': False,
        'error': 'API endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


def main():
    """启动 API 服务器"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Text-to-Speech REST API Server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='服务器地址')
    parser.add_argument('--port', type=int, default=5001, help='服务器端口')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    args = parser.parse_args()
    
    print("=" * 70)
    print("🎤 Text-to-Speech REST API Server")
    print("=" * 70)
    print(f"📡 服务地址: http://{args.host}:{args.port}")
    print(f"📖 API 文档:")
    print(f"   - POST   /api/tts/generate      - 生成单个语音")
    print(f"   - POST   /api/tts/batch         - 批量生成语音")
    print(f"   - GET    /api/tts/audio/<file>  - 获取音频文件")
    print(f"   - GET    /api/tts/files         - 列出所有文件")
    print(f"   - GET    /api/tts/health        - 健康检查")
    print(f"   - GET    /api/tts/info          - 系统信息")
    print("=" * 70)
    print("按 Ctrl+C 停止服务器")
    print("=" * 70)
    print()
    
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        threaded=True
    )


if __name__ == '__main__':
    main()
