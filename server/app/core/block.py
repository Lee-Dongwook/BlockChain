import hashlib
import json
import time
from typing import List

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[dict], difficulty: int, nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "difficulty": self.difficulty
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    