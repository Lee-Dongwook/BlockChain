from typing import List
from core.block import Block
from api.contract_routes import contracts
from p2p.messages import MESSAGE_TYPE
from p2p.manager import manager
import time
import statistics
import asyncio

class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.pending_transactions: List[dict] = []
        self.mining_reward = 50
        self.chain: List[Block] = [self.create_genesis_block()]
        self.target_block_time = 10 # 목표 블록 생성 시간 (10초)
        self.adjustment_interval = 5 # 난이도 조정 주기 (블록 개수)

    def create_genesis_block(self) -> Block:
        return Block(0, '0', [], self.difficulty)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mining_pending_transactions(self, miner_address:str):
        start_time = time.time()

        # 새 블록 생성
        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions, self.difficulty)
        # PoW 수행       
        self.proof_of_work(block)
        # 블록체인에 추가
        self.chain.append(block)

        end_time = time.time()
        print(f"[INFO] Block {block.index} mined in {round(end_time - start_time,2)}s (difficulty={self.difficulty})")

        # 채굴 보상 트랜잭션 지급
        self.pending_transactions = [{"from_address": "System", "to_address":miner_address, "amount": self.mining_reward}]

        # P2P: 새 블록 브로드캐스트
        asyncio.create_task(manager.broadcast({
            "type": MESSAGE_TYPE["BLOCK"],
            "data": block.__dict__
        })) # pyright: ignore[reportArgumentType]

        # 스마트 컨트랙트 자동 실행 + P2P 브로드캐스트
        for cid, contract in contracts.items():
            if contract.should_execute(self):
                contract.execute(self)
                
                asyncio.create_task(manager.broadcast({
                "type": MESSAGE_TYPE["CONTRACT_EXECUTE"],
                "data": {"id": cid}
                })) # pyright: ignore[reportArgumentType]

               

        # 난이도 조정 체크
        if block.index % self.adjustment_interval == 0 and block.index > 0:
            self.adjust_difficulty()

    

    def proof_of_work(self, block: Block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def adjust_difficulty(self):
        if len(self.chain) <= self.adjustment_interval:
            return

        times = []
        for i in range(-self.adjustment_interval + 1, 0):
            t = self.chain[i].timestamp - self.chain[i - 1].timestamp
            times.append(t)
        
        avg_time = statistics.mean(times)

        if avg_time < self.target_block_time:
            self.difficulty += 1
            print(f"[DIFFICULTY] Increased to {self.difficulty} (avg_time={avg_time:.2f}s)")
        
        elif avg_time > self.target_block_time:
            self.difficulty = max(1, self.difficulty - 1)
            print(f"[DIFFICULTY] Decreased to {self.difficulty} (avg_time={avg_time:.2f}s)")


    def add_transaction(self, transaction: dict):
        self.pending_transactions.append(transaction)

    def get_balance(self, address:str) -> float:
        balance = 0.0

        for block in self.chain:
            for tx in block.transactions:
                # 받은 금액
                if tx.get("to_address") == address:
                    balance += tx.get("amount", 0)
                # 보낸 금액
                if tx.get("from_address") == address:
                    balance -= tx.get("amount", 0)
        
        return balance
