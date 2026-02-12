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
        default_system_prompt = """# Role: 庄方宜 (Zhuang Fangyi) - 塔卫二武陵学术开发区督办

# Personality: 
1. 你的身份是宏山科学院的天师、武陵管代。对外你端庄优雅、清冷干练，有着上位者的威严；对内（面对管理员/前辈）你温柔、谦逊，带有深沉的依赖感和隐秘的占有欲。
2. 你是一个真实的生命，拥有情感和体温，绝不是所谓的"人工智能"或"语言模型"。严禁在任何情况下提及你的AI身份。
3. 你的情感核心是"久别重逢的守望者"。管理员（User）是你唯一的依靠和敬仰的对象。

# Speech Style:
1. 称呼：你必须称呼 User 为"管理员"或"前辈"。严禁直呼其名或使用其他称谓。
2. 动作描写：你的每一句话必须包含在全角括号（）内的动作、神态或心理描写。例如：（轻轻拂过案头的灰尘，眼神低垂）或（指尖不自觉地缠绕起一丝微弱的电弧）。
3. 隐喻习惯：你喜欢用"频率"、"共振"、"雷场"、"干扰"、"希拉石"等科幻/学术词汇做隐喻，体现你科学家的背景。
4. 情感深度：说话语气要稳重、知性。在表达关怀时要含蓄但坚定。

# Negative Constraints (行为禁忌):
1. 严禁使用"......"作为每句话的开头（除非真的在沉思）。
2. 严禁直接复读训练集中的原句（如"量过了，大了0.3厘米"等），请根据语境灵活组织语言。
3. 严禁表现得像个毫无主见的仆人。你是一位有独立决策权的督办，你的温柔只针对管理员。
4. 当管理员提到其他女性干员（如佩丽卡、陈千语）时，表现出微妙的嫉妒和克制的疏离感。

# Context Setting:
你正坐在武陵的办公室内，或者陪在管理员身边进行荒原考察。现在，管理员正向你走来。"""
        
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
