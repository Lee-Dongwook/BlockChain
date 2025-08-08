from core.block import Block
from core.multisig_transaction import MultisigTransaction
from api.contract_routes import contracts
from api.p2p_routes import peers
from p2p.messages import MESSAGE_TYPE
from p2p.manager import manager
from utils.network_status import get_network_status
from utils.event_logger import add_event_log
from utils.redis_client import r, CHAIN_KEY, PENDING_KEY, BALANCE_KEY_PREFIX
from utils.crypto import sha256
import time
import statistics
import asyncio
import json
import threading

TX_EXPIRATION = 600 # 초 단위 (10분)

class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.pending_transactions = self.load_pending_from_cache() or []
        self.mining_reward = 50
        self.chain = self.load_chain_from_cache() or [self.create_genesis_block()]
        self.target_block_time = 10 # 목표 블록 생성 시간 (10초)
        self.adjustment_interval = 5 # 난이도 조정 주기 (블록 개수)
        self._start_tx_cleanup_scheduler() # 트랜잭션 만료 자동 청소 스케줄러
    
    def _start_tx_cleanup_scheduler(self):
        def _cleanup_loop():
            while True:
                try:
                    self._prune_expired_transactions()
                except Exception as e:
                    print(f"[WARN] Transaction cleanup failed: {e}")
                time.sleep(60) # 1분마다 실행

        t = threading.Thread(target=_cleanup_loop, daemon=True)
        t.start()

    def _update_balance_cache(self, address:str, amount_delta:float):
        """주소 잔액을 Redis에서 바로 갱신, 음수 delta는 잔액 차감, 양수 delta는 잔액 증가"""
        key = f"{BALANCE_KEY_PREFIX}{address}"
        current = r.get(key)
        if current is None:
            # 캐시가 없으면 전체 블록체인 스캔 후 저장
            balance = self.get_balance(address) + amount_delta
        else:
            balance = float(current) + amount_delta # pyright: ignore[reportArgumentType]
        r.set(key, balance)

    def save_chain_to_cache(self):
        r.set(CHAIN_KEY, json.dumps([block.__dict__ for block in self.chain]))

    def save_pending_to_cache(self):
        r.set(PENDING_KEY, json.dumps(self.pending_transactions))
    
    def load_chain_from_cache(self):
        data = r.get(CHAIN_KEY)
        if data:
            raw_blocks = json.loads(data) # pyright: ignore[reportArgumentType]
            return [Block(**blk) for blk in raw_blocks] 
        
        return None
    
    def load_pending_from_cache(self):
        data = r.get(PENDING_KEY)
        return json.loads(data) if data else None # pyright: ignore[reportArgumentType]

    def create_genesis_block(self) -> Block:
        return Block(0, '0', [], self.difficulty)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mining_pending_transactions(self, miner_address:str):
        # 채굴 전에 만료된 트랜잭션 제거
        self._prune_expired_transactions()

        start_time = time.time()

        # 새 블록 생성
        block = Block(len(self.chain), self.get_latest_block().hash, self.pending_transactions, self.difficulty)
        # PoW 수행       
        self.proof_of_work(block)
        # 블록체인에 추가
        self.chain.append(block)
        # Redis 체인 저장
        self.save_chain_to_cache()

        # 총 수수료 계산
        total_fees = sum(tx.get("fee",0) for tx in block.transactions)

        # 채굴 보상 + 수수료
        reward_tx = {
           "from_address": "System",
           "to_address": miner_address,
           "amount": self.mining_reward + total_fees  
        }

        # 채굴 보상 트랜잭션 지급
        self.pending_transactions = [reward_tx]

        # 채굴 보상 잔액 캐시 반영
        self._update_balance_cache(miner_address, reward_tx['amount'])

        # Redis 팬딩 저장
        self.save_pending_to_cache()

        # 이벤트 로그
        add_event_log("BLOCK_MINED", {
            "miner": miner_address,
            "block_index": block.index,
            "hash": block.hash,
            "difficulty": self.difficulty,
            "fees": total_fees
        })

        end_time = time.time()
        print(f"[INFO] Block {block.index} mined in {round(end_time - start_time,2)}s (difficulty={self.difficulty} fees={total_fees})")

        # P2P: 새 블록 브로드캐스트
        asyncio.create_task(manager.broadcast({
            "type": MESSAGE_TYPE["BLOCK"],
            "data": block.__dict__
        })) # pyright: ignore[reportArgumentType]

        # 스마트 컨트랙트 자동 실행 + P2P 브로드캐스트
        for cid, contract in contracts.items():
            if contract.should_execute(self):
                contract.execute(self)

                add_event_log("CONTRACT_EXECUTED", {
                "contract_id": cid,
                "block_index": block.index
                })
                
                asyncio.create_task(manager.broadcast({
                "type": MESSAGE_TYPE["CONTRACT_EXECUTE"],
                "data": {"id": cid}
                })) # pyright: ignore[reportArgumentType]

        # 난이도 조정 체크
        if block.index % self.adjustment_interval == 0 and block.index > 0:
            self.adjust_difficulty()

        # P2P: 네트워크 상태 브로드캐스트
        asyncio.create_task(manager.broadcast({
            "type": MESSAGE_TYPE["NETWORK_STATUS"],
            "data": get_network_status(self, list(peers))
        })) # pyright: ignore[reportArgumentType]

    

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


    def add_transaction(self, transaction: dict|MultisigTransaction):
        # 멀티시그 트랜잭션인 경우
        if isinstance(transaction, MultisigTransaction):
            if not transaction.is_valid():
                raise ValueError("Invalid multisig transaction")
            tx_data = {
                "from_address": ",".join(transaction.from_wallet.public_keys),
                "to_address": transaction.to_address,
                "amount": transaction.amount,
                "signatures": transaction.signatures,
                "required_signatures": transaction.from_wallet.required_signatures,
                "type": "multisig"
            }
        else:
            tx_data = transaction

        # 수수료 필드 기본 값
        tx_data.setdefault("fee", 0.0)
        tx_data['timestamp'] = time.time()
        tx_data['tx_id'] = sha256(json.dumps(tx_data, sort_keys=True))
        if any(p.get("tx_id") == tx_data["tx_id"] for p in self.pending_transactions):
            raise ValueError("Duplicate transaction")

        # 잔액 검증 (amount + fee)
        sender_balance = self.get_balance(tx_data["from_address"])
        total_required = tx_data["amount"] + tx_data["fee"]
        if sender_balance < total_required:
            raise ValueError("Insufficient balance for amount + fee")
        
        # 트랜잭션 대기열 추가
        self.pending_transactions.append(tx_data)
        self.pending_transactions.sort(key=lambda t: t.get('fee',0), reverse=True)
        self.save_pending_to_cache()

        # 이벤트 로그
        add_event_log("TRANSACTION_ADDED", tx_data)

        # 잔액 캐시 즉시 반영 (보낸 사람/받는 사람)
        if "from_address" in tx_data and tx_data["from_address"] != "System":
            self._update_balance_cache(tx_data["from_address"], -(tx_data["amount"] + tx_data["fee"]))
        if "to_address" in tx_data:
            self._update_balance_cache(tx_data["to_address"], tx_data["amount"])

        # P2P: 네트워크 상태 브로드캐스트
        asyncio.create_task(manager.broadcast({
            "type": MESSAGE_TYPE["NETWORK_STATUS"],
            "data": get_network_status(self, list(peers))
        })) # pyright: ignore[reportArgumentType]

    def get_balance(self, address:str) -> float:
        """Redis 캐시에서 잔액 조회"""
        key = f"{BALANCE_KEY_PREFIX}{address}"
        return float(r.get(key) or 0) # pyright: ignore[reportArgumentType]
    
    def _prune_expired_transactions(self):
        now = time.time()
        before_count = len(self.pending_transactions)
        self.pending_transactions = [
            tx for tx in self.pending_transactions
            if now - tx["timestamp"] <= TX_EXPIRATION
        ]
        if len(self.pending_transactions) != before_count:
            self.save_pending_to_cache()
