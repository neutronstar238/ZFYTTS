# LLM Chat System

基于 GGUF 模型的多用户、多会话聊天系统。

## 特性

- ✅ 支持多用户同时使用
- ✅ 每个用户可以创建多个聊天会话
- ✅ 自动保存和加载对话历史
- ✅ 上下文记忆管理
- ✅ 会话列表和切换功能

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 命令行交互模式

```bash
python chat_manager.py
```

### 在代码中使用

```python
from chat_manager import ChatBot

# 初始化聊天机器人
chatbot = ChatBot("zhuang_fangyi_int4.gguf")

# 用户1的第一次对话（自动创建新会话）
result = chatbot.chat(
    user_input="你好！",
    user_id="user_001"
)
print(result['response'])
session_id = result['session_id']

# 继续同一会话
result = chatbot.chat(
    user_input="今天天气怎么样？",
    user_id="user_001",
    session_id=session_id
)
print(result['response'])

# 用户2的独立会话
result = chatbot.chat(
    user_input="帮我写一首诗",
    user_id="user_002"
)
print(result['response'])

# 查看用户的所有会话
sessions = chatbot.get_sessions("user_001")
for session in sessions:
    print(f"Session: {session['session_id']}")
    print(f"Preview: {session['preview']}")
```

## 命令

在交互模式下可用的命令：

- `/new` - 开始新的聊天会话
- `/list` - 列出当前用户的所有会话
- `/load <session_id>` - 加载指定的会话
- `/quit` - 退出程序

## 记忆存储结构

```
memories/
├── user_001/
│   ├── session-uuid-1.json
│   ├── session-uuid-2.json
│   └── ...
├── user_002/
│   ├── session-uuid-3.json
│   └── ...
└── ...
```

每个会话文件包含完整的对话历史，格式如下：

```json
[
  {
    "role": "system",
    "content": "你是一个有帮助的AI助手。",
    "timestamp": "2026-02-12T19:30:00"
  },
  {
    "role": "user",
    "content": "你好！",
    "timestamp": "2026-02-12T19:30:05"
  },
  {
    "role": "assistant",
    "content": "你好！有什么我可以帮助你的吗？",
    "timestamp": "2026-02-12T19:30:08"
  }
]
```

## 配置参数

在初始化 `ChatBot` 时可以调整以下参数：

- `model_path`: GGUF 模型文件路径
- `max_context_length`: 最大上下文长度（默认 2048）

在调用 `chat()` 方法时可以调整：

- `system_prompt`: 系统提示词
- `max_tokens`: 最大生成 token 数（默认 512）
- `temperature`: 采样温度（默认 0.7）

## 注意事项

1. 每个用户的会话是完全隔离的
2. 会话 ID 使用 UUID 自动生成，确保唯一性
3. 对话历史自动保存到 JSON 文件
4. 支持并发访问（不同用户/会话互不影响）
