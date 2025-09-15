import random

def format_key(text: str, key: str) -> str:
    key = key.upper()
    result = ''
    key_index = 0
    for char in text:
        if char.isalpha():
            result += key[key_index % len(key)]
            key_index += 1
        else:
            result += char
    return result

def encrypt_vigenere(text: str, key: str) -> str:
    result = ''
    key_formatted = format_key(text, key)
    for i, char in enumerate(text):
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            key_char = key_formatted[i].upper()
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def decrypt_vigenere(text: str, key: str) -> str:
    result = ''
    key_formatted = format_key(text, key)
    for i, char in enumerate(text):
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            key_char = key_formatted[i].upper()
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            result += char
    return result

vigenere_questions = [
    {
        "question": "Ngôn ngữ nào thường dùng nhất trong lập trình AI?",
        "options": ["Java", "C++", "Python", "Ruby"],
        "answer": "Python"
    },
    {
        "question": "Từ khóa để giải mã chuỗi Vigenère thường được gọi là gì?",
        "options": ["Seed", "Key", "Shift", "Hash"],
        "answer": "Key"
    },
    {
        "question": "Chuỗi sau khi mã hóa Vigenère sẽ có đặc điểm gì?",
        "options": [
            "Chỉ dùng số",
            "Không thể giải mã",
            "Có thể giải bằng khóa",
            "Bị mất dữ liệu gốc"
        ],
        "answer": "Có thể giải bằng khóa"
    }
]

def get_vigenere_questions():
    return random.sample(vigenere_questions, len(vigenere_questions))
