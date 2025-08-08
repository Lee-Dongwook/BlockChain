import time
from typing import Optional
from core.blockchain import Blockchain
from utils.crypto import sha256

class SmartContract:
    def __init__(self, condition:dict, action:dict, expire_block: Optional[int] = None):
        self.id = sha256(str(time.time()) + str(condition) + str(action))
        self.condition = condition 
        self.action = action
        self.expire_block = expire_block
        self.executed = False

    def should_execute(self, blockchain:Blockchain) -> bool:
        if self.executed:
            return False
        if self.expire_block and blockchain.get_latest_block().index > self.expire_block:
            return False
        
        # 조건 타입별 평가
        if self.condition['type'] == 'block_height':
            return blockchain.get_latest_block().index >= self.condition['value']
        
        if self.condition['type'] == 'balance_gte':
            address = self.condition['address']
            required = self.condition['value']
            return blockchain.get_balance(address) >= required
        
        return False
    
    def execute(self, blockchain):
        blockchain.add_transaction({
            "from_address": "System",
            "to_address": self.action["to_address"],
            "amount": self.action["amount"]
        })
        self.executed = True
        return True