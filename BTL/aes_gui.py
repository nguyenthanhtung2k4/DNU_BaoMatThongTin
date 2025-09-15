# aes_gui.py – chuẩn hóa thuật toán AES cho Flask game

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

def derive_aes_key(key: str) -> bytes:
    """Chuyển key tùy ý thành 16 byte bằng SHA256."""
    return SHA256.new(key.encode()).digest()[:16]

def encrypt_aes(plaintext: str, key: str) -> str:
    key_bytes = derive_aes_key(key)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=key_bytes)
    encrypted = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return b64encode(encrypted).decode()

def decrypt_aes(cipher_b64: str, key: str) -> str:
    try:
        key_bytes = derive_aes_key(key)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv=key_bytes)
        decrypted = unpad(cipher.decrypt(b64decode(cipher_b64)), AES.block_size)
        return decrypted.decode()
    except Exception as e:
        return ""

def get_aes_questions():
    key = "1234567890abcdef"

    q1_plain = "LABIOT"
    q2_plain = "CRYPTO"
    q3_plain = "HACKLAB"

    return [
        {
            "question": f"Giải mã AES: {encrypt_aes(q1_plain, key)}",
            "options": ["CRYPTO", "HACKLAB", "LABIOT"],
            "answer": q1_plain
        },
        {
            "question": f"Giải mã AES: {encrypt_aes(q2_plain, key)}",
            "options": ["CRYPTO", "AES", "LABIOT"],
            "answer": q2_plain
        },
        {
            "question": f"Giải mã AES: {encrypt_aes(q3_plain, key)}",
            "options": ["HACKLAB", "FITDNU", "AESLAB"],
            "answer": q3_plain
        },
    ]
