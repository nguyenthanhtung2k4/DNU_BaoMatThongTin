import hashlib
import random

def get_sha256_questions():
    raw_data = [
        ("Python", "Ngôn ngữ lập trình phổ biến trong AI"),
        ("HASHING", "Thuật ngữ liên quan đến băm SHA256"),
        ("DNU", "Tên viết tắt một trường đại học ở Việt Nam")
    ]

    questions = []
    for correct, hint in raw_data:
        hash_val = hashlib.sha256(correct.encode()).hexdigest()

        fake_answers = ["Java", "Encrypt", "Hello", "AES", "Flask"]
        distractors = random.sample(fake_answers, 3)
        options = distractors + [correct]
        random.shuffle(options)

        questions.append({
            "question": f"🔐 Chuỗi nào tạo ra mã SHA256 sau?\n{hash_val}",
            "options": options,
            "answer": correct,
            "hint": hint
        })

    random.shuffle(questions)
    return questions
