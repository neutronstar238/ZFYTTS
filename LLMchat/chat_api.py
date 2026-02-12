"""
Simple Flask API for LLM Chat System
Provides REST API endpoints for multi-user chat
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_manager import ChatBot
import os

app = Flask(__name__)
CORS(app)

# ============================================
# 配置项
# ============================================

# 模型路径
MODEL_PATH = "zhuang_fangyi_int4.gguf"

# GPU 配置
USE_GPU = True  # 设置为 False 使用 CPU
N_GPU_LAYERS = 35  # GPU 层数，0 表示全部使用 CPU

# ============================================
# 初始化 Chatbot
# ============================================

chatbot = ChatBot(
    MODEL_PATH,
    use_gpu=USE_GPU,
    n_gpu_layers=N_GPU_LAYERS
)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint
    
    Request body:
    {
        "message": "user message",
        "user_id": "user_001",
        "session_id": "optional-session-id",
        "system_prompt": "optional system prompt",
        "max_tokens": 512,
        "temperature": 0.7
    }
    """
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_input = data['message']
        user_id = data.get('user_id', 'default_user')
        session_id = data.get('session_id')
        system_prompt = data.get('system_prompt', '你是庄方宜，一个温柔体贴的AI助手。请用庄方宜的身份和语气回答问题。')
        max_tokens = data.get('max_tokens', 512)
        temperature = data.get('temperature', 0.7)
        
        result = chatbot.chat(
            user_input=user_input,
            user_id=user_id,
            session_id=session_id,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sessions/<user_id>', methods=['GET'])
def get_sessions(user_id):
    """Get all sessions for a user"""
    try:
        sessions = chatbot.get_sessions(user_id)
        return jsonify({
            'success': True,
            'data': sessions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/session/<user_id>/<session_id>', methods=['GET'])
def get_session_history(user_id, session_id):
    """Get conversation history for a specific session"""
    try:
        history = chatbot.get_conversation_history(user_id, session_id)
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/session/<user_id>/<session_id>', methods=['DELETE'])
def delete_session(user_id, session_id):
    """Delete a specific session"""
    try:
        chatbot.delete_session(user_id, session_id)
        return jsonify({
            'success': True,
            'message': 'Session deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': MODEL_PATH
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
