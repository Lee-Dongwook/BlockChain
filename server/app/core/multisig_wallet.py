from typing import List
from utils.crypto import verify_signature

class MultisigWallet:
    def __init__(self, public_keys: List[str], required_signatures: int):
        if required_signatures > len(public_keys):
            raise ValueError('Required signatures cannot exceed number of public keys')
        
        self.public_keys = public_keys
        self.required_signatures = required_signatures
    
    def verify_signatures(self, message: str, signatures: List[str]) -> bool:
        unique_signers = set()
        
        for sig_hex in signatures:
            for pk_hex in self.public_keys:
                if verify_signature(pk_hex, sig_hex, message):
                    unique_signers.add(pk_hex)
                    break # 해당 서명은 이미 유효, 다음 서명 검사로 이동
        
        return len(unique_signers) >= self.required_signatures