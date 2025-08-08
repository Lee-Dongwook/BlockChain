from fastapi import APIRouter
from core.blockchain import Blockchain
from core.transaction import Transaction

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
def create_transaction(from_address:str, to_address:str, amount:float, signature:str):
    tx = Transaction(from_address, to_address, amount)
    tx.signature = signature
    if not tx.is_valid():
        return {'error': "Invalid transaction signature"}

    blockchain.add_transaction(tx.__dict__)
    return {"message": "Transaction added successfully"}