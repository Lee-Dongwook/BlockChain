from typing import List, Dict
import time

event_logs: List[Dict] = []

def add_event_log(event_type: str, details: dict):
    event_logs.append({
        "timestamp": time.time(),
        "type": event_type,
        "details": details
    })
    # 최근 100개만 유지
    if len(event_logs) > 100:
        event_logs.pop(0)

def get_event_logs():
    return list(event_logs)