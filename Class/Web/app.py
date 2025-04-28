from flask import Flask, render_template, request, flash
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cần thiết cho flash messages

def des_encrypt(plaintext, key):
    try:
        key_bytes = key.encode('utf-8')
        if len(key_bytes) != 8:
            flash('Khóa phải là 8 byte!', 'error')
            return None
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
        ciphertext = cipher.encrypt(padded_text)
        return binascii.hexlify(ciphertext).decode('utf-8')
    except Exception as e:
        flash(f'Lỗi mã hóa: {e}', 'error')
        return None

def des_decrypt(ciphertext, key):
    try:
        key_bytes = key.encode('utf-8')
        if len(key_bytes) != 8:
            flash('Khóa phải là 8 byte!', 'error')
            return None
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        ciphertext_bytes = binascii.unhexlify(ciphertext)
        padded_text = cipher.decrypt(ciphertext_bytes)
        plaintext = unpad(padded_text, DES.block_size).decode('utf-8')
        return plaintext
    except Exception as e:
        flash(f'Lỗi giải mã: {e}', 'error')
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    ciphertext = None
    plaintext = None

    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        action = request.form['action']

        if action == 'encrypt':
            ciphertext = des_encrypt(text, key)
        elif action == 'decrypt':
            plaintext = des_decrypt(text, key)

    return render_template('index.html', ciphertext=ciphertext, plaintext=plaintext)

if __name__ == '__main__':
    app.run(debug=True)