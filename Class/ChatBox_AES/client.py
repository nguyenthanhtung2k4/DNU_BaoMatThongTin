import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii
import socket
import threading
import os

# Khóa AES (chuỗi tiếng Việt, mã hóa thành bytes, phải dài 16/24/32 bytes)
KEY = 'khóa_bí_mật_tiếng_việt_1'.encode('utf-8')  # 32 bytes

# Hàm mã hóa AES
def aes_encrypt(data):
    try:
        cipher = AES.new(KEY, AES.MODE_CBC)
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        # Gửi cả IV và ciphertext
        encrypted_data = binascii.hexlify(cipher.iv + ciphertext).decode('utf-8')
        return encrypted_data
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi mã hóa: {e}")
        return None

# Hàm giải mã AES
def aes_decrypt(ciphertext):
    try:
        ciphertext_bytes = binascii.unhexlify(ciphertext)
        # Tách IV (16 bytes đầu) và ciphertext
        iv = ciphertext_bytes[:16]
        ciphertext = ciphertext_bytes[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv=iv)
        padded_data = cipher.decrypt(ciphertext)
        data = unpad(padded_data, AES.block_size)
        return data
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi giải mã: {e}")
        return None

# Hàm gửi tin nhắn
def send_message():
    message = entry.get()
    if not message:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tin nhắn!")
        return
    encrypted_message = aes_encrypt(message.encode('utf-8'))
    if encrypted_message:
        try:
            # Gửi loại dữ liệu (MESSAGE) và nội dung
            client_socket.send(f"MESSAGE:{encrypted_message}".encode('utf-8'))
            text_area.config(state='normal')
            text_area.insert(tk.END, f"A (gốc): {message}\n")
            text_area.insert(tk.END, f"A (mã hóa): {encrypted_message}\n\n")
            text_area.config(state='disabled')
            entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi gửi tin nhắn: {e}")

# Hàm gửi file
def send_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    file_name = os.path.basename(file_path)
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        encrypted_file = aes_encrypt(file_data)
        if encrypted_file:
            # Gửi loại dữ liệu (FILE), tên file, và nội dung file
            client_socket.send(f"FILE:{file_name}:{encrypted_file}".encode('utf-8'))
            text_area.config(state='normal')
            text_area.insert(tk.END, f"A (gốc - file): {file_name}\n")
            text_area.insert(tk.END, f"A (mã hóa - file): {encrypted_file[:50]}...\n\n")
            text_area.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi gửi file: {e}")

# Hàm nhận dữ liệu (chạy trong luồng riêng)
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                # Phân tích loại dữ liệu
                data_type, content = data.split(':', 1)
                if data_type == "MESSAGE":
                    decrypted_message = aes_decrypt(content)
                    if decrypted_message:
                        decrypted_message = decrypted_message.decode('utf-8')
                        text_area.config(state='normal')
                        text_area.insert(tk.END, f"B (mã hóa): {content}\n")
                        text_area.insert(tk.END, f"B (giải mã): {decrypted_message}\n\n")
                        text_area.config(state='disabled')
                elif data_type == "FILE":
                    file_name, encrypted_file = content.split(':', 1)
                    decrypted_file = aes_decrypt(encrypted_file)
                    if decrypted_file:
                        save_path = os.path.join(os.getcwd(), f"received_{file_name}")
                        with open(save_path, 'wb') as f:
                            f.write(decrypted_file)
                
                        text_area.config(state='normal')
                        text_area.insert(tk.END, f"A (mã hóa - file): {encrypted_file[:50]}...\n")
                        text_area.insert(tk.END, f"A (giải mã - file): Đã lưu file {file_name} thành received_{file_name}\n")
                
                        # Thử đọc nội dung nếu là file văn bản
                        try:
                            decoded_text = decrypted_file.decode('utf-8')
                            text_area.insert(tk.END, f"Nội dung file:\n{decoded_text}\n\n")
                        except UnicodeDecodeError:
                            text_area.insert(tk.END, "Nội dung file: [Không phải văn bản hoặc không đọc được bằng UTF-8]\n\n")
                
                        text_area.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi nhận dữ liệu: {e}")
            break

# Thiết lập GUI
root = tk.Tk()
root.title("Chat Client A (Bạn của bạn)")
root.geometry("400x500")

# Khu vực hiển thị tin nhắn
text_area = tk.Text(root, height=20, width=40, state='disabled')
text_area.pack(pady=10)

# Ô nhập tin nhắn
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Nút gửi tin nhắn và file
send_message_button = tk.Button(root, text="Gửi tin nhắn", command=send_message)
send_message_button.pack(pady=5)

send_file_button = tk.Button(root, text="Gửi file", command=send_file)
send_file_button.pack(pady=5)

# Thiết lập socket
IP_SERVER = '172.16.70.70'  # Chạy trên cùng máy (localhost)
PORT = 54321

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP_SERVER, PORT))
    text_area.config(state='normal')
    text_area.insert(tk.END, f"Đã kết nối đến B tại {IP_SERVER}:{PORT}\n")
    text_area.config(state='disabled')
except Exception as e:
    messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")
    root.destroy()

# Chạy luồng nhận dữ liệu
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Chạy GUI
root.mainloop()
# python client.py