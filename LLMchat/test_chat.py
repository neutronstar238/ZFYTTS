"""
Test script for LLM Chat System
Demonstrates multi-user and multi-session functionality
"""

from chat_manager import ChatBot

def test_multi_user_chat():
    """Test multiple users with separate sessions"""
    print("=== Testing Multi-User Chat System ===\n")
    
    # Initialize chatbot
    chatbot = ChatBot("zhuang_fangyi_int4.gguf")
    
    # User 1 - First conversation
    print("--- User 1: Starting first conversation ---")
    result1 = chatbot.chat(
        user_input="你好，我是张三。",
        user_id="user_zhang"
    )
    print(f"Assistant: {result1['response']}")
    session1_id = result1['session_id']
    print(f"Session ID: {session1_id}\n")
    
    # User 2 - Independent conversation
    print("--- User 2: Starting independent conversation ---")
    result2 = chatbot.chat(
        user_input="你好，我是李四。",
        user_id="user_li"
    )
    print(f"Assistant: {result2['response']}")
    session2_id = result2['session_id']
    print(f"Session ID: {session2_id}\n")
    
    # User 1 - Continue first conversation
    print("--- User 1: Continuing first conversation ---")
    result3 = chatbot.chat(
        user_input="你还记得我的名字吗？",
        user_id="user_zhang",
        session_id=session1_id
    )
    print(f"Assistant: {result3['response']}\n")
    
    # User 1 - Start new conversation
    print("--- User 1: Starting new conversation ---")
    result4 = chatbot.chat(
        user_input="帮我写一首诗。",
        user_id="user_zhang"
    )
    print(f"Assistant: {result4['response']}")
    session3_id = result4['session_id']
    print(f"New Session ID: {session3_id}\n")
    
    # List User 1's sessions
    print("--- User 1: Listing all sessions ---")
    sessions = chatbot.get_sessions("user_zhang")
    print(f"Total sessions: {len(sessions)}")
    for i, session in enumerate(sessions, 1):
        print(f"\nSession {i}:")
        print(f"  ID: {session['session_id']}")
        print(f"  Preview: {session['preview']}")
        print(f"  Messages: {session['message_count']}")
        print(f"  Last updated: {session['last_updated']}")
    
    print("\n=== Test completed successfully! ===")


if __name__ == "__main__":
    test_multi_user_chat()
