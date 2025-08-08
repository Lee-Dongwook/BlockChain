from typing import List
from core.block import Block

class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.pending_transactions: List[dict] = []
        self.mining_reward = 50
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        return Block(0, '0', [], self.difficulty)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mining_pending_transactions(self, miner_address:str):
        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions, self.difficulty)
        self.proof_of_work(block)
        self.chain.append(block)
        self.pending_transactions = [{"from": "System", "to":miner_address, "amount": self.mining_reward}]

    def proof_of_work(self, block: Block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def add_transaction(self, transaction: dict):
        self.pending_transactions.append(transaction)