import binascii
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError
from ecdsa.util import sigdecode_der
import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def _decompress_pubkey(pk_bytes: bytes) -> bytes:
    if len(pk_bytes) == 33:
        from ecdsa.ecdsa import generator_secp256k1
        from ecdsa.ellipticcurve import Point

        prefix = pk_bytes[0]
        x = int.from_bytes(pk_bytes[1:], 'big')
        curve = generator_secp256k1.curve()
        p  = curve.p()
        
        # Solve y^2 = x^3 + 7 mod p (secp256k1 equation)
        alpha = (x * x * x + 7) % p
        beta = pow(alpha, (p + 1) // 4, p) 

        if (beta % 2 == 0 and prefix == 0x02) or (beta % 2 == 1 and prefix == 0x03):
            y = beta
        else:
            y = p - beta
        
        point = Point(curve, x, y)
        return point.x().to_bytes(32, 'big') + point.y().to_bytes(32, "big")
    elif len(pk_bytes) == 64:
        return pk_bytes
    
    else:
        raise ValueError("Invalid public key length")


def verify_signature(public_key_hex:str, signature_hex:str, message:str) -> bool:
    try:
        pk_bytes = bytes.fromhex(public_key_hex)
        pk_bytes = _decompress_pubkey(pk_bytes) # Ensure uncompressed 64-byte key

        sig_bytes = binascii.unhexlify(signature_hex)
        vk = VerifyingKey.from_string(pk_bytes, curve=SECP256k1)
        return vk.verify(sig_bytes,message.encode(), sigdecode=sigdecode_der)
    
    except(ValueError, BadSignatureError, binascii.Error):
        return False