# import tkinter as tk
# from tkinter import messagebox
# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad
# import binascii
# import socket
# import threading

# # Khóa DES (phải giống với client)
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
# def send_message(client_socket):
#     message = entry.get()
#     if not message:
#         messagebox.showwarning("Cảnh báo", "Vui lòng nhập tin nhắn!")
#         return
#     encrypted_message = des_encrypt(message)
#     if encrypted_message:
#         try:
#             client_socket.send(encrypted_message.encode('utf-8'))
#             text_area.config(state='normal')
#             text_area.insert(tk.END, f"B (gốc): {message}\n")
#             text_area.insert(tk.END, f"B (mã hóa): {encrypted_message}\n\n")
#             text_area.config(state='disabled')
#             entry.delete(0, tk.END)
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi gửi tin nhắn: {e}")

# # Hàm nhận tin nhắn
# def receive_messages(client_socket):
#     while True:
#         try:
#             encrypted_message = client_socket.recv(1024).decode('utf-8')
#             if encrypted_message:
#                 decrypted_message = des_decrypt(encrypted_message)
#                 if decrypted_message:
#                     text_area.config(state='normal')
#                     text_area.insert(tk.END, f"Sever - (mã hóa): {encrypted_message}\n")
#                     text_area.insert(tk.END, f"Sever - (giải mã): {decrypted_message}\n\n")
#                     text_area.config(state='disabled')
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi nhận tin nhắn: {e}")
#             break

# # Thiết lập GUI
# root = tk.Tk()
# root.title("Chat Server B")
# root.geometry("400x500")

# # Khu vực hiển thị tin nhắn
# text_area = tk.Text(root, height=20, width=40, state='disabled')
# text_area.pack(pady=10)

# # Ô nhập tin nhắn
# entry = tk.Entry(root, width=30)
# entry.pack(pady=5)

# # Thiết lập socket server
# try:
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('172.20.10.2', 12345))
#     server_socket.listen(1)
#     text_area.config(state='normal')
#     text_area.insert(tk.END, "Đang chờ kết nối từ ...\n")
#     text_area.config(state='disabled')
#     client_socket, addr = server_socket.accept()
#     text_area.config(state='normal')
#     text_area.insert(tk.END, f"Đã kết nối với : {addr}\n")
#     text_area.config(state='disabled')
# except Exception as e:
#     messagebox.showerror("Lỗi", f"Lỗi server: {e}")
#     root.destroy()

# # Nút gửi (truyền client_socket vào hàm send_message)
# send_button = tk.Button(root, text="Gửi", command=lambda: send_message(client_socket))
# send_button.pack(pady=5)

# # Chạy luồng nhận tin nhắn
# receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
# receive_thread.start()

# # Chạy GUI
# root.mainloop()
# # python server.py


import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii
import socket
import threading
import os

KEY = b'8bytekey'  # Khóa DES

def des_encrypt(data):
    cipher = DES.new(KEY, DES.MODE_ECB)
    padded_data = pad(data, DES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def des_decrypt(data):
    cipher = DES.new(KEY, DES.MODE_ECB)
    decrypted_padded = cipher.decrypt(data)
    return unpad(decrypted_padded, DES.block_size)

def send_message(client_socket):
    message = entry.get()
    if not message:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tin nhắn!")
        return
    try:
        encrypted = des_encrypt(message.encode())
        client_socket.send(b"MSG:" + encrypted)
        text_area.config(state='normal')
        text_area.insert(tk.END, f"B (gốc): {message}\n")
        text_area.insert(tk.END, f"B (mã hóa): {binascii.hexlify(encrypted).decode()}\n\n")
        text_area.config(state='disabled')
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def send_file(client_socket):
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

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break

            if data.startswith(b"MSG:"):
                decrypted = des_decrypt(data[4:]).decode()
                encrypted_hex = binascii.hexlify(data[4:]).decode()
                text_area.config(state='normal')
                text_area.insert(tk.END, f"Client - (mã hóa): {encrypted_hex}\n")
                text_area.insert(tk.END, f"Client - (giải mã): {decrypted}\n\n")
                text_area.config(state='disabled')
            elif data.startswith(b"FILE:"):
                parts = data[5:].split(b"::", 1)
                filename = parts[0].decode()
                decrypted_data = des_decrypt(parts[1])
                with open("server_received_" + filename, 'wb') as f:
                    f.write(decrypted_data)
                text_area.config(state='normal')
                text_area.insert(tk.END, f"Đã nhận file: server_received_{filename}\n\n")
                text_area.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Lỗi nhận", str(e))
            break

# GUI
root = tk.Tk()
root.title("Chat Server B")
root.geometry("400x550")

text_area = tk.Text(root, height=20, width=50, state='disabled')
text_area.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

send_button = tk.Button(root, text="Gửi tin nhắn", command=lambda: send_message(client_socket))
send_button.pack(pady=5)

file_button = tk.Button(root, text="Gửi file", command=lambda: send_file(client_socket))
file_button.pack(pady=5)

# Socket setup
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('172.20.10.2', 29205))
    server_socket.listen(1)
    text_area.config(state='normal')
    text_area.insert(tk.END, "Đang chờ kết nối từ client...\n")
    text_area.config(state='disabled')
    client_socket, addr = server_socket.accept()
    text_area.config(state='normal')
    text_area.insert(tk.END, f"Đã kết nối với: {addr}\n")
    text_area.config(state='disabled')
except Exception as e:
    messagebox.showerror("Lỗi server", str(e))
    root.destroy()

# Nhận dữ liệu từ client
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
root.mainloop()
