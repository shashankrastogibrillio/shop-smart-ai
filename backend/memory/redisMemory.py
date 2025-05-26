from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
import os

def get_redis_connection():
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')  # Default to local Redis
    try:
        return redis.StrictRedis.from_url(redis_url)
    except Exception as e:
        raise Exception(f"Failed to connect to Redis: {str(e)}")


def load_memory(session_id):
    try:
        message_history = RedisChatMessageHistory(
            url=os.getenv("REDIS_URL"),
            session_id=session_id
        )
        memory = ConversationBufferMemory(
            chat_memory=message_history,
            return_messages=True,
            memory_key="chat_history"
        )
        return memory
    except Exception as e:
        raise Exception(f"Failed to connect to Redis memory store: {str(e)}")
