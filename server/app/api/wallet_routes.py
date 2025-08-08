from fastapi import APIRouter
from core.wallet import Wallet
from core.transaction import Transaction
from core.blockchain import Blockchain

wallet_router = APIRouter()
blockchain = Blockchain()  # 실제 운영 시 전역 blockchain 객체 공유

@wallet_router.post('/wallet/create')
def create_wallet():
    wallet = Wallet()
    return {
        "private_key": wallet.private_key.to_string().hex(),
        "public_key": wallet.public_key.to_string().hex(),
        "address": wallet.address
    }

@wallet_router.post('/wallet/sign')
def sign_transaction(private_key_hex: str, from_address: str, to_address: str, amount: float):
    # 개인키로 Wallet 객체 재 생성
    from ecdsa import SigningKey, SECP256k1
    sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    wallet = Wallet()
    wallet.private_key = sk
    wallet.public_key = sk.get_verifying_key()
    wallet.address = from_address

    tx = Transaction(from_address, to_address, amount)
    tx.sign_transaction(wallet)
    
    return {
        "from_address": tx.from_address,
        "to_address": tx.to_address,
        "amount": tx.amount,
        "signature": tx.signature
    }


@wallet_router.post('/wallet/send')
def send_transaction(tx: dict):
    from core.transaction import Transaction
    new_tx = Transaction(tx['from_address'], tx['to_address'], tx['amount'])
    new_tx.signature = tx['signature']

    if not new_tx.is_valid():
        return {'error': "Invalid transaction signature"}
    
    blockchain.add_transaction(tx)
    return {"message": "Transaction added to pool"}


@wallet_router.post('/wallet/mine')
def mine_wallet_block(miner_address: str):
    blockchain.mining_pending_transactions(miner_address)
    return {"message": "Block mined", "chain_length": len(blockchain.chain)}