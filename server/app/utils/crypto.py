import binascii
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError
import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def verify_signature(public_key_hex:str, signature_hex:str, message:str) -> bool:
    try:
        pk_bytes = bytes.fromhex(public_key_hex)
        sig_bytes = binascii.unhexlify(signature_hex)
        vk = VerifyingKey.from_string(pk_bytes, curve=SECP256k1)
        return vk.verify(sig_bytes,message.encode())
    except(ValueError, BadSignatureError, binascii.Error):
        return False