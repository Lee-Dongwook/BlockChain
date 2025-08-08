from fastapi import APIRouter
from core.multisig_wallet import MultisigWallet
from core.multisig_transaction import MultisigTransaction
from core.blockchain import Blockchain

multisig_router = APIRouter()
blockchain = Blockchain()

wallets = {} # wallet_id -> MultiSigWallet
transactions = {} # tx_id -> MultiSigTransaction

@multisig_router.post('/create-wallet')
def create_multisig_wallet(public_keys: list[str], required_signatures: int):
    wallet_id = f"msw_{len(wallets) + 1}"
    wallets[wallet_id] = MultisigWallet(public_keys, required_signatures)
    return {"wallet_id": wallet_id, "public_keys": public_keys, "required_signatures": required_signatures}

@multisig_router.post('/create-transaction')
def create_multisig_transaction(wallet_id: str, to_address: str, amount: float):
    if wallet_id not in wallets:
        return {"error": "Wallet not found"}
    tx_id = f"mstx_{len(transactions)+1}"
    transactions[tx_id] = MultisigTransaction(wallets[wallet_id], to_address, amount)
    return {"tx_id": tx_id, "hash": transactions[tx_id].calculate_hash()}

@multisig_router.pos('/add-signature')
def add_signature(tx_id: str, signature: str):
    if tx_id not in transactions:
        return {"error": "Transaction not found"}
    transactions[tx_id].add_signature(signature)
    return {"message": "Signature added", "current_signatures": len(transactions[tx_id].signatures)}

@multisig_router.post('/submit-transaction')
def submit_multisig_transaction(tx_id: str):
    if tx_id not in transactions:
        return {"error": "Transaction not found"}
    tx = transactions[tx_id]
    if not tx.is_valid():
        return {"error": "Not enough valid signatures"}
    
    blockchain.add_transaction({
        "from_multisig": tx.from_wallet.public_keys,
        "to_address": tx.to_address,
        "amount": tx.amount,
        "signatures": tx.signatures,
    })
    
    return {"message": "Multisig transaction added"}