from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import os




def encode():
    # Tạo một đối tượng DES cipher ở chế độ ECB (Electronic Codebook)
    cipher = DES.new(key, DES.MODE_ECB)
    # Độ dài khối của DES là 8 byte. Dữ liệu cần được đệm để có độ dài là bội số của 8
    padded_data = pad(data, DES.block_size)

    # Mã hóa dữ liệu
    global ciphered_data  # Khai báo biến toàn cục để decode() có thể truy cập
    ciphered_data = cipher.encrypt(padded_data)

    print(f"Dữ liệu đã mã hóa: {ciphered_data.hex()}")

# --- Giải mã ---
def decode():
    # Tạo lại đối tượng DES cipher cho quá trình giải mã, sử dụng cùng khóa
    cipher_dec = DES.new(key, DES.MODE_ECB)

    # Giải mã dữ liệu
    decrypted_padded_data = cipher_dec.decrypt(ciphered_data)

    # Loại bỏ phần đệm để lấy lại dữ liệu gốc
    try:
        decrypted_data = unpad(decrypted_padded_data, DES.block_size)
        print(f"Dữ liệu đã giải mã: {decrypted_data.decode()}")
    except ValueError as e:
        print(f"Lỗi giải mã: {e}")



# key = os.urandom(8)
key = ("12345678").encode('utf-8')
if len(key) !=8 :
    print("Khong du  8 bit ")

data = b"TUNG thanh "

encode()
decode()