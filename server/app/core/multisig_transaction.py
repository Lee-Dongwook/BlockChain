from typing import List
from utils.crypto import sha256
from core.multisig_wallet import MultisigWallet

class MultisigTransaction:
    def __init__ (self, from_wallet: MultisigWallet, to_address: str, amount: float):
        self.from_wallet = from_wallet
        self.to_address = to_address
        self.amount = amount
        self.signatures: List[str] = []

    def calculate_hash(self) -> str:
        return sha256(f"{','.join(self.from_wallet.public_keys)}{self.to_address}{self.amount}")

    def add_signature(self, signature: str):
        if signature not in self.signatures:
            self.signatures.append(signature)
    
    def is_valid(self) -> bool:
        return self.from_wallet.verify_signatures(self.calculate_hash(), self.signatures)