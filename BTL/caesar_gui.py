import random


def encrypt(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)

_raw_caesar_questions = [
    {
        "cipher": encrypt("Python", 3),
        "expected": "Python",
        "hint": "Tên ngôn ngữ sử dụng nhiều trong AI (Key = 3)?"
    },
    {
        "cipher": encrypt("Hello world", 3),
        "expected": "Hello world",
        "hint": "Câu đầu tiên học lập trình?(Key = 3)"
    },
    {
        "cipher": encrypt("List", 3),
        "expected": "List",
        "hint": "Lưu danh sách thì dùng gì?( Key = 3)"
    }
]

def get_caesar_questions():
    questions = []
    for item in _raw_caesar_questions:
        options = [item['expected'], "Python", "Encrypt", "Hello"]
        random.shuffle(options)
        questions.append({
            "question": f"Giải mã Caesar: {item['cipher']}",
            "options": options,
            "answer": item['expected'],
            "hint": item['hint']  
        })
    random.shuffle(questions)
    return questions
