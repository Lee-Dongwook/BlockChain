from typing import Optional
from utils.crypto import sha256

class Transaction:
    def __init__(self, from_address: Optional[str], to_address: str, amount:float):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.signature = None

    def calculate_hash(self) -> str:
        return sha256(f"{self.from_address}{self.to_address}{self.amount}")
    
    def sign_transaction(self,wallet):
        if wallet.address != self.from_address:
            raise Exception('You cannot sign transactions for other wallets')
        self.signature = wallet.sign(self.calculate_hash())

    def is_valid(self) -> bool:
        if self.from_address is None:
            return True
        if not self.signature:
            raise Exception("No signature in this transaction")
        from core.wallet import Wallet
        return Wallet.verify_signature(public_key_hex=self.from_address, message=self.calculate_hash(), signature_hex=self.signature)