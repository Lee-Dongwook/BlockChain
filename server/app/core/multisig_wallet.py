from typing import List
from ecdsa import VerifyingKey, SECP256k1
import binascii

class MultisigWallet:
    def __init__(self, public_keys: List[str], required_signatures: int):
        if required_signatures > len(public_keys):
            raise ValueError('Required signatures cannot exceed number of public keys')
        
        self.public_keys = public_keys
        self.required_signatures = required_signatures
    
    def verify_signatures(self, message: str, signatures: List[str]) -> bool:
        unique_signers = set()
        valid_count = 0

        for sig_hex in signatures:
            for pk_hex in self.public_keys:
                try:
                    pk_bytes = bytes.fromhex(pk_hex)
                    vk = VerifyingKey.from_string(pk_bytes, curve=SECP256k1)
                    if vk.verify(binascii.unhexlify(sig_hex), bytes.fromhex(message)):
                        unique_signers.add(pk_hex)
                        break
                except Exception:
                    continue
        
        valid_count = len(unique_signers)
        return valid_count >= self.required_signatures