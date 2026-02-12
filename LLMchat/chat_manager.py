"""
LLM Chat Manager with Multi-User and Multi-Session Support
Supports memory management for multiple users and chat sessions
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from llama_cpp import Llama


class MemoryManager:
    """Manages chat memories for multiple users and sessions"""
    
    def __init__(self, memory_dir: str = "memories"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
    def _get_memory_path(self, user_id: str, session_id: str) -> Path:
        """Get the memory file path for a specific user and session"""
        user_dir = self.memory_dir / user_id
        user_dir.mkdir(exist_ok=True)
        return user_dir / f"{session_id}.json"
    
    def load_memory(self, user_id: str, session_id: str) -> List[Dict]:
        """Load chat history for a specific user and session"""
        memory_path = self._get_memory_path(user_id, session_id)
        
        if memory_path.exists():
            try:
                with open(memory_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                return []
        return []
    
    def save_memory(self, user_id: str, session_id: str, messages: List[Dict]):
        """Save chat history for a specific user and session"""
        memory_path = self._get_memory_path(user_id, session_id)
        
        try:
            with open(memory_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def list_sessions(self, user_id: str) -> List[Dict]:
        """List all sessions for a user"""
        user_dir = self.memory_dir / user_id
        
        if not user_dir.exists():
            return []
        
        sessions = []
        for file_path in user_dir.glob("*.json"):
            session_id = file_path.stem
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    if messages:
                        first_msg = messages[0].get('content', '')[:50]
                        last_time = messages[-1].get('timestamp', '')
                        sessions.append({
                            'session_id': session_id,
                            'preview': first_msg,
                            'last_updated': last_time,
                            'message_count': len(messages)
                        })
            except Exception:
                continue
        
        return sorted(sessions, key=lambda x: x.get('last_updated', ''), reverse=True)
    
    def delete_session(self, user_id: str, session_id: str):
        """Delete a specific session"""
        memory_path = self._get_memory_path(user_id, session_id)
        if memory_path.exists():
            memory_path.unlink()


class ChatBot:
    """LLM Chat Bot with context management"""
    
    def __init__(self, 
                 model_path: str, 
                 max_context_length: int = 2048,
                 use_gpu: bool = True,
                 n_gpu_layers: int = 35):
        """
        Initialize the chatbot
        
        Args:
            model_path: Path to the GGUF model file
            max_context_length: Maximum context length for the model
            use_gpu: Whether to use GPU acceleration (default: True)
            n_gpu_layers: Number of layers to offload to GPU (default: 35, 0 for CPU only)
        """
        print(f"Loading model from {model_path}...")
        
        # 根据 use_gpu 参数决定是否使用 GPU
        gpu_layers = n_gpu_layers if use_gpu else 0
        
        if use_gpu:
            print(f"🚀 GPU 加速已启用 (offloading {gpu_layers} layers)")
        else:
            print("💻 使用 CPU 模式")
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=max_context_length,
            n_threads=4,
            n_gpu_layers=gpu_layers,
            verbose=False
        )
        self.memory_manager = MemoryManager()
        print("Model loaded successfully!")
    
    def _format_messages_for_prompt(self, messages: List[Dict]) -> str:
        """Format message history into a prompt string"""
        prompt = ""
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == 'system':
                prompt += f"System: {content}\n\n"
            elif role == 'user':
                prompt += f"User: {content}\n\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n\n"
        return prompt
    
    def chat(self, 
             user_input: str, 
             user_id: str = "default_user",
             session_id: Optional[str] = None,
             system_prompt: str = "你是庄方宜，一个温柔体贴的AI助手。请用庄方宜的身份和语气回答问题。",
             max_tokens: int = 512,
             temperature: float = 0.7) -> Dict:
        """
        Process user input and generate response
        
        Args:
            user_input: User's message
            user_id: Unique identifier for the user
            session_id: Session ID (creates new if None)
            system_prompt: System prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dict containing response and session info
        """
        # Create new session if not provided
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # Load existing conversation history
        messages = self.memory_manager.load_memory(user_id, session_id)
        
        # Add system prompt if this is a new conversation
        if not messages:
            messages.append({
                'role': 'system',
                'content': system_prompt,
                'timestamp': datetime.now().isoformat()
            })
        
        # Add user message
        messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Format prompt for the model
        prompt = self._format_messages_for_prompt(messages)
        prompt += "Assistant: "
        
        # Generate response
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["User:", "\n\n\n"],
            echo=False
        )
        
        assistant_message = response['choices'][0]['text'].strip()
        
        # Add assistant response to history
        messages.append({
            'role': 'assistant',
            'content': assistant_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save updated conversation
        self.memory_manager.save_memory(user_id, session_id, messages)
        
        return {
            'response': assistant_message,
            'session_id': session_id,
            'user_id': user_id,
            'message_count': len(messages)
        }
    
    def get_sessions(self, user_id: str) -> List[Dict]:
        """Get all sessions for a user"""
        return self.memory_manager.list_sessions(user_id)
    
    def delete_session(self, user_id: str, session_id: str):
        """Delete a specific session"""
        self.memory_manager.delete_session(user_id, session_id)
    
    def get_conversation_history(self, user_id: str, session_id: str) -> List[Dict]:
        """Get full conversation history for a session"""
        return self.memory_manager.load_memory(user_id, session_id)


def main():
    """Interactive chat interface"""
    # Initialize chatbot
    model_path = "zhuang_fangyi_int4.gguf"
    chatbot = ChatBot(model_path)
    
    print("\n=== LLM Chat System ===")
    print("Commands:")
    print("  /new - Start a new chat session")
    print("  /list - List all your sessions")
    print("  /load <session_id> - Load a specific session")
    print("  /quit - Exit the chat")
    print("=" * 50)
    
    user_id = input("\nEnter your user ID (or press Enter for 'default'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    session_id = None
    
    while True:
        user_input = input(f"\n[{user_id}] You: ").strip()
        
        if not user_input:
            continue
        
        # Handle commands
        if user_input.startswith('/'):
            cmd_parts = user_input.split()
            cmd = cmd_parts[0].lower()
            
            if cmd == '/quit':
                print("Goodbye!")
                break
            
            elif cmd == '/new':
                session_id = None
                print("Started new session!")
                continue
            
            elif cmd == '/list':
                sessions = chatbot.get_sessions(user_id)
                if not sessions:
                    print("No sessions found.")
                else:
                    print("\nYour sessions:")
                    for s in sessions:
                        print(f"  ID: {s['session_id']}")
                        print(f"  Preview: {s['preview']}")
                        print(f"  Messages: {s['message_count']}")
                        print(f"  Last updated: {s['last_updated']}")
                        print("-" * 40)
                continue
            
            elif cmd == '/load':
                if len(cmd_parts) < 2:
                    print("Usage: /load <session_id>")
                else:
                    session_id = cmd_parts[1]
                    history = chatbot.get_conversation_history(user_id, session_id)
                    if history:
                        print(f"\nLoaded session: {session_id}")
                        print(f"Messages in history: {len(history)}")
                    else:
                        print("Session not found.")
                        session_id = None
                continue
            
            else:
                print(f"Unknown command: {cmd}")
                continue
        
        # Process chat message
        try:
            result = chatbot.chat(user_input, user_id=user_id, session_id=session_id)
            session_id = result['session_id']
            
            print(f"\nAssistant: {result['response']}")
            print(f"\n[Session: {session_id[:8]}... | Messages: {result['message_count']}]")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
