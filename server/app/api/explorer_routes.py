from fastapi import APIRouter
from core.blockchain import Blockchain

explorer_router = APIRouter()
blockchain = Blockchain() # 운영에서는 전역 BlockChain 객체 공유

@explorer_router.get("/blocks")
def get_all_blocks():
    return [block.__dict__ for block in blockchain.chain]

@explorer_router.get("/blocks/{index}")
def get_block_by_index(index: int):
    if index < 0 or index >= len(blockchain.chain):
        return {"error": "Block not found"}
    return blockchain.chain[index].__dict__

@explorer_router.get("/address/{address}/transactions")
def get_transactions_by_address(address: str):
    txs = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.get("from_address") == address or tx.get("to_address") == address:
                txs.append(tx)
    return txs