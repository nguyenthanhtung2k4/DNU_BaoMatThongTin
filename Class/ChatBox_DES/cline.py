# import tkinter as tk
# from tkinter import messagebox
# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad
# import binascii
# import socket
# import threading

# # Khóa DES (phải dài 8 bytes, giống nhau ở cả A và B)
# KEY = b'8bytekey'

# # Hàm mã hóa DES
# def des_encrypt(plaintext):
#     try:
#         cipher = DES.new(KEY, DES.MODE_ECB)
#         padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
#         ciphertext = cipher.encrypt(padded_text)
#         encrypted_text = binascii.hexlify(ciphertext).decode('utf-8')
#         return encrypted_text
#     except Exception as e:
#         messagebox.showerror("Lỗi", f"Lỗi mã hóa: {e}")
#         return None

# # Hàm giải mã DES
# def des_decrypt(ciphertext):
#     try:
#         cipher = DES.new(KEY, DES.MODE_ECB)
#         ciphertext_bytes = binascii.unhexlify(ciphertext)
#         padded_text = cipher.decrypt(ciphertext_bytes)
#         plaintext = unpad(padded_text, DES.block_size).decode('utf-8')
#         return plaintext
#     except Exception as e:
#         messagebox.showerror("Lỗi", f"Lỗi giải mã: {e}")
#         return None

# # Hàm gửi tin nhắn
# def send_message():
#     message = entry.get()
#     if not message:
#         messagebox.showwarning("Cảnh báo", "Vui lòng nhập tin nhắn!")
#         return
#     encrypted_message = des_encrypt(message)
#     if encrypted_message:
#         try:
#             client_socket.send(encrypted_message.encode('utf-8'))
#             text_area.config(state='normal')
#             text_area.insert(tk.END, f"A (gốc): {message}\n")
#             text_area.insert(tk.END, f"A (mã hóa): {encrypted_message}\n\n")
#             text_area.config(state='disabled')
#             entry.delete(0, tk.END)
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi gửi tin nhắn: {e}")

# # Hàm nhận tin nhắn (chạy trong luồng riêng)
# def receive_messages():
#     while True:
#         try:
#             encrypted_message = client_socket.recv(1024).decode('utf-8')
#             if encrypted_message:
#                 decrypted_message = des_decrypt(encrypted_message)
#                 if decrypted_message:
#                     text_area.config(state='normal')
#                     text_area.insert(tk.END, f"Clinet- (mã hóa): {encrypted_message}\n")
#                     text_area.insert(tk.END, f"Clinet- (giải mã): {decrypted_message}\n\n")
#                     text_area.config(state='disabled')
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi nhận tin nhắn: {e}")
#             break

# # Thiết lập GUI
# root = tk.Tk()
# root.title("Chat Client A")
# root.geometry("400x500")

# # Khu vực hiển thị tin nhắn
# text_area = tk.Text(root, height=20, width=40, state='disabled')
# text_area.pack(pady=10)

# # Ô nhập tin nhắn
# entry = tk.Entry(root, width=30)
# entry.pack(pady=5)

# # Nút gửi
# send_button = tk.Button(root, text="Gửi", command=send_message)
# send_button.pack(pady=5)

# # Thiết lập socket
# try:
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('172.20.10.2', 12345))  # Kết nối tới server B
# except Exception as e:            
#     messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")
#     root.destroy()

# # Chạy luồng nhận tin nhắn
# receive_thread = threading.Thread(target=receive_messages, daemon=True)
# receive_thread.start()

# # Chạy GUI
# root.mainloop()
# # python client.py


import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii
import socket
import threading
import os

KEY = b'8bytekey'

def des_encrypt(data):
    cipher = DES.new(KEY, DES.MODE_ECB)
    padded_data = pad(data, DES.block_size)
    return cipher.encrypt(padded_data)

def des_decrypt(data):
    cipher = DES.new(KEY, DES.MODE_ECB)
    decrypted_padded = cipher.decrypt(data)
    return unpad(decrypted_padded, DES.block_size)

def send_message():
    message = entry.get()
    if not message:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tin nhắn!")
        return
    try:
        encrypted = des_encrypt(message.encode())
        client_socket.send(b"MSG:" + encrypted)
        text_area.config(state='normal')
        text_area.insert(tk.END, f"A (gốc): {message}\n")
        text_area.insert(tk.END, f"A (mã hóa): {binascii.hexlify(encrypted).decode()}\n\n")
        text_area.config(state='disabled')
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi gửi tin nhắn", str(e))

def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted_data = des_encrypt(data)
        filename = os.path.basename(filepath)
        client_socket.send(b"FILE:" + filename.encode() + b"::" + encrypted_data)
        text_area.config(state='normal')
        text_area.insert(tk.END, f"Đã gửi file: {filename}\n")
        text_area.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Lỗi gửi file", str(e))

def receive_messages():
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            if data.startswith(b"MSG:"):
                decrypted = des_decrypt(data[4:]).decode()
                encrypted_hex = binascii.hexlify(data[4:]).decode()
                text_area.config(state='normal')
                text_area.insert(tk.END, f"Server - (mã hóa): {encrypted_hex}\n")
                text_area.insert(tk.END, f"Server - (giải mã): {decrypted}\n\n")
                text_area.config(state='disabled')
            elif data.startswith(b"FILE:"):
                parts = data[5:].split(b"::", 1)
                filename = parts[0].decode()
                decrypted_data = des_decrypt(parts[1])
                with open("client_received_" + filename, 'wb') as f:
                    f.write(decrypted_data)
                text_area.config(state='normal')
                text_area.insert(tk.END, f"Đã nhận file: client_received_{filename}\n\n")
                text_area.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Lỗi nhận", str(e))
            break

# GUI
root = tk.Tk()
root.title("Chat Client A")
root.geometry("400x550")

text_area = tk.Text(root, height=20, width=50, state='disabled')
text_area.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

send_button = tk.Button(root, text="Gửi tin nhắn", command=send_message)
send_button.pack(pady=5)

file_button = tk.Button(root, text="Gửi file", command=send_file)
file_button.pack(pady=5)

# Socket
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('172.16.31.0', 65535))
except Exception as e:
    messagebox.showerror("Lỗi kết nối", str(e))
    root.destroy()

threading.Thread(target=receive_messages, daemon=True).start()
root.mainloop()
