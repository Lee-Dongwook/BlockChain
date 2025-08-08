import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()