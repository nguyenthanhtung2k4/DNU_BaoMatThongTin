from flask import Flask, render_template, request, redirect, url_for, session, flash
from caesar_gui import get_caesar_questions
from vigenere_gui import get_vigenere_questions
from rsa_gui import get_rsa_questions
from aes_gui import get_aes_questions
from sha256_gui import get_sha256_questions
import random
import os

app = Flask(__name__, template_folder='tem')
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

def get_questions_for_level(level_id):
    if level_id == 1:
       return get_caesar_questions()
    elif level_id == 2:
        return get_vigenere_questions()
    elif level_id == 3:
        return get_rsa_questions()
    elif level_id == 4:
        return get_aes_questions()
    elif level_id == 5:
        return get_sha256_questions()
    return []

@app.route('/')
def index():
    session.clear()
    session['level'] = 1
    session['score'] = 0
    session['mistakes'] = 0
    session['questions'] = {}
    session['show_hint'] = False
    return redirect(url_for('level', level_id=1))

@app.route('/level/<int:level_id>')
def level(level_id):
    if level_id > 5:
        return redirect(url_for('end'))

    if str(level_id) not in session['questions']:
        session['questions'][str(level_id)] = get_questions_for_level(level_id)
        session['current_q'] = 0
        session['mistakes'] = 0

    current_q = session['current_q']
    question_list = session['questions'][str(level_id)]
    question_data = question_list[current_q]

    return render_template(
        'game.html',
        level_id=level_id,
        question=question_data['question'],
        options=question_data['options'],
        score=session['score'],
        mistakes=session['mistakes'],
        hint=question_data.get('hint', ''),
        show_hint=session.get('show_hint', True),
        total_questions=len(question_list),
        current_question_index=current_q + 1 
    )



@app.route('/check/<int:level_id>', methods=['POST'])
def check(level_id):
    answer = request.form.get('answer', '').strip()
    current_q = session.get('current_q')
    questions = session.get('questions', {}).get(str(level_id), [])

    if current_q is None or current_q >= len(questions):
        flash("Lỗi dữ liệu câu hỏi.", "error")
        return redirect(url_for('fail'))

    question_data = questions[current_q]
    correct_answer = question_data['answer'].strip()

    if answer not in question_data['options']:
        flash("Lựa chọn không hợp lệ!", "error")
        return redirect(url_for('level', level_id=level_id))

    if answer.lower() == correct_answer.lower():
        session['score'] += 10
        session['mistakes'] = 0
        session['current_q'] += 1
        flash("✅ Chính xác!", "success")
    else:
        session['mistakes'] += 1
        flash("❌ Sai rồi! Hãy thử lại.", "error")
        if session['mistakes'] >= 2:
            return redirect(url_for('fail'))

    if session['current_q'] >= 3:
        session['level'] += 1
        return redirect(url_for('level', level_id=level_id + 1))

    return redirect(url_for('level', level_id=level_id))

@app.route('/fail')
def fail():
    return render_template('lose.html', score=session.get('score', 0))

@app.route('/end')
def end():
    return render_template('end.html', score=session.get('score', 0))
@app.route('/toggle_hint')
def toggle_hint():
    session['show_hint'] = not session.get('show_hint', True)
    return redirect(url_for('level', level_id=session.get('level', 1)))

if __name__ == '__main__':
    app.run(debug=True)
