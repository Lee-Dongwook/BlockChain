import os 
import redis

REDIS_URL = os.getenv('REDIS_URL', "redis://localhost:6379")

# decode_responses=True 로 str <-> json 편하게
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

CHANNEL = os.getenv("REDIS_CHANNEL", "event_channel")
LOG_KEY = os.getenv("REDIS_LOG_KEY", "event_logs")
LOG_LIMIT = int(os.getenv("REDIS_LOG_LIMIT", "100"))