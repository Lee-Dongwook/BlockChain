from fastapi import APIRouter
from core.blockchain import Blockchain

router = APIRouter()
blockchain = Blockchain()

@router.get("/blocks")
def get_blocks():
    return [block.__dict__ for block in blockchain.chain]

@router.post('/mine')
def mine_block(miner_address: str):
    blockchain.mining_pending_transactions(miner_address)
    return {"message": "Block mined successfully"}

@router.post('/transactions')
def create_transaction(tx: dict):
    blockchain.add_transaction(tx)
    return {"message": "Transaction added successfully"}