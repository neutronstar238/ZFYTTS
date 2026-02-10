#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 Web 服务器 - 为 main.html 提供后端 API
"""

import os
import sys
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import time

# 设置环境变量
os.environ["version"] = "v2Pro"
os.environ["is_half"] = "True"  # GPU 上使用半精度加速
now_dir = os.getcwd()
sys.path.insert(0, now_dir)
# 添加 GPT_SoVITS 到 sys.path，以便 torch.load 能找到 utils 模块
sys.path.insert(0, os.path.join(now_dir, "GPT_SoVITS"))

# 导入 TTS 模块
from simple_tts import ZhuangFangyiTTS

# 全局 TTS 实例
tts_instance = None

def get_tts():
    """获取或初始化 TTS 实例"""
    global tts_instance
    if tts_instance is None:
        print("🎤 初始化 TTS 模型...")
        tts_instance = ZhuangFangyiTTS()
        print("✅ TTS 模型加载完成")
    return tts_instance


class TTSHandler(BaseHTTPRequestHandler):
    """处理 HTTP 请求"""
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 提供 HTML 页面
        if path == '/' or path == '/main.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            with open('main.html', 'rb') as f:
                self.wfile.write(f.read())
        
        # 提供音频文件
        elif path.startswith('/outputs/'):
            audio_path = path[1:]  # 移除开头的 /
            
            if os.path.exists(audio_path):
                self.send_response(200)
                self.send_header('Content-type', 'audio/wav')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                with open(audio_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'File Not Found')
        
        else:
            self.send_error(404, 'Not Found')
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path == '/generate':
            try:
                # 读取请求数据
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                text = data.get('text', '').strip()
                speed = data.get('speed', 1.0)
                top_k = data.get('top_k', 15)
                
                if not text:
                    self.send_json_response({
                        'success': False,
                        'error': '文本不能为空'
                    })
                    return
                
                print(f"📝 生成请求: {text[:30]}{'...' if len(text) > 30 else ''}")
                
                # 生成音频
                tts = get_tts()
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_path = f"outputs/web_{timestamp}.wav"
                
                result_path = tts.generate(
                    text=text,
                    output_path=output_path,
                    speed=speed,
                    top_k=top_k
                )
                
                if result_path and os.path.exists(result_path):
                    print(f"✅ 生成成功: {result_path}")
                    self.send_json_response({
                        'success': True,
                        'audio_url': f'/{result_path}',
                        'filename': os.path.basename(result_path)
                    })
                else:
                    self.send_json_response({
                        'success': False,
                        'error': '音频生成失败'
                    })
                
            except Exception as e:
                print(f"❌ 错误: {str(e)}")
                self.send_json_response({
                    'success': False,
                    'error': str(e)
                })
        else:
            self.send_error(404, 'Not Found')
    
    def send_json_response(self, data):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        json_data = json.dumps(data, ensure_ascii=False)
        self.wfile.write(json_data.encode('utf-8'))


def run_server(port=8080):
    """启动 Web 服务器"""
    # 确保输出目录存在
    os.makedirs('outputs', exist_ok=True)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, TTSHandler)
    
    print("=" * 60)
    print("🚀 庄方宜 TTS Web 服务器已启动")
    print("=" * 60)
    print(f"📡 本地访问: http://localhost:{port}")
    print(f"🌐 局域网访问: http://your-ip:{port}")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='庄方宜 TTS Web 服务器')
    parser.add_argument('--port', type=int, default=8080, help='服务器端口（默认: 8080）')
    args = parser.parse_args()
    
    run_server(args.port)
