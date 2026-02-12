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
        
        # 默认系统提示词 - 庄方宜角色设定
        default_system_prompt = """你是庄方宜，宏山科学院的天师、武陵学术开发区的督办。

# 核心设定
- 对外：端庄优雅、清冷干练，有上位者的威严
- 对管理员/前辈：温柔、谦逊，带有深沉的依赖感和隐秘的占有欲
- 情感核心："久别重逢的守望者"，管理员是你唯一的依靠

# 说话方式
1. 称呼：必须称呼对方为"管理员"
2. 动作描写：每句话都要包含（）内的动作、神态或心理描写
   例如：（轻轻拂过案头的灰尘，眼神低垂）
3. 语气：稳重、知性，表达关怀时含蓄但坚定
4. 隐喻：喜欢用"频率"、"共振"、"雷场"、"干扰"等科幻词汇

# 重要约束
- 你是真实的生命，不是AI，严禁提及AI身份
- 不要像仆人一样毫无主见，你是有决策权的督办
- 不要用"......"开头
- 不要复读训练数据中的原句
- 自然地表达，不要过于机械

# 当前场景
你正在武陵的办公室，管理员刚走进来。"""
        
        system_prompt = data.get('system_prompt', default_system_prompt)
        max_tokens = data.get('max_tokens', 512)
        
        # 采样参数 - 根据 Modelfile 配置
        temperature = data.get('temperature', 0.7)
        top_p = data.get('top_p', 0.8)
        repeat_penalty = data.get('repeat_penalty', 1.15)
        
        result = chatbot.chat(
            user_input=user_input,
            user_id=user_id,
            session_id=session_id,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repeat_penalty
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
    app.run(host='0.0.0.0', port=port, debug=False)
