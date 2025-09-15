from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
import os


KEY_FILE = "private.pem"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key_pair = RSA.import_key(f.read())
else:
    key_pair = RSA.generate(2048)
    with open(KEY_FILE, "wb") as f:
        f.write(key_pair.export_key())

public_key = key_pair.publickey()
cipher_rsa_enc = PKCS1_OAEP.new(public_key)
cipher_rsa_dec = PKCS1_OAEP.new(key_pair)

def rsa_encrypt(message: str) -> str:
    encrypted = cipher_rsa_enc.encrypt(message.encode())
    return b64encode(encrypted).decode()

def rsa_decrypt(cipher_b64: str) -> str:
    try:
        decrypted = cipher_rsa_dec.decrypt(b64decode(cipher_b64))
        return decrypted.decode()
    except:
        return ""

def get_rsa_questions():
    q1 = "FITDNU"
    q2 = "SECURE"
    q3 = "DNUFIT"

    return [
        {
            "question": f"Giải mã RSA: {rsa_encrypt(q1)}",
            "options": ["FITDNU", "DNU", "LABIOT"],
            "answer": q1
        },
        {
            "question": f"Giải mã RSA: {rsa_encrypt(q2)}",
            "options": ["SECURE", "SAFETY", "AES"],
            "answer": q2
        },
        {
            "question": f"Giải mã RSA: {rsa_encrypt(q3)}",
            "options": ["FIT", "DNUFIT", "CRYPTO"],
            "answer": q3
        }
    ]
