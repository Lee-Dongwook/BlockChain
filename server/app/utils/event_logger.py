from utils.redis_client import r , LOG_KEY, LOG_LIMIT, CHANNEL
from typing import Any, List, Dict, Iterator
import json, time

def add_event_log(event_type: str, details: dict, publish:bool = True):
    """Redis 리스트에 이벤트 로그 추가 및 Pub/Sub 전파"""
    event:Dict[str,Any] = {"timestamp": time.time(), "type": event_type, "details": details}
    
    # 리스트에 push + 최대 길이 제한
    r.lpush(LOG_KEY, json.dump(event)) # pyright: ignore[reportCallIssue]
    r.ltrim(LOG_KEY, 0 , LOG_LIMIT -1)

    # Pub/Sub으로 실시간 전파
    if publish:
        r.publish(CHANNEL, json.dumps(event))



def get_event_logs(limit: int = 100) -> Iterator[Dict[str,Any]]:
    """최근 이벤트 로그를 최신순으로 반환"""
    raw:List[str] = r.lrange(LOG_KEY, 0, limit - 1) # pyright: ignore[reportAssignmentType]
    for entry in raw:
        yield json.loads(entry)

def subscribe_event_logs() -> Iterator[Dict[str, Any]]:
    """Redis Pub/Sub으로 실시간 이벤트 로그 구독"""
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)
    for message in pubsub.listen():
        if message["type"] == "message": 
            yield json.loads(message["data"])