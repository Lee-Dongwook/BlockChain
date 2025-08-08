from ecdsa import SigningKey, SECP256k1
import binascii
from utils.crypto import sha256

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = sha256(self.public_key.to_string().hex())
    
    def sign(self, message: str) -> str:
        signature = self.private_key.sign(message.encode())
        return binascii.hexlify(signature).decode()
    
    @staticmethod
    def verify_signature(public_key_hex: str, message: str, signature_hex: str) -> bool:
        from ecdsa import VerifyingKey
        try:
            public_key_bytes = bytes.fromhex(public_key_hex)
            vk = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)
            return vk.verify(binascii.unhexlify(signature_hex), message.encode())
        except Exception:
            return False