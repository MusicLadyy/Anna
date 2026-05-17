
import os
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'birthday_secret_key_2026')

@app.route('/')
def index():
    if 'choices' not in session:
        session['choices'] = {'fruit': '', 'choco': '', 'topping': ''}
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    q_idx = data.get('q_idx')
    ans_idx = int(data.get('ans_idx'))
    
    correct = {0: 1, 1: 1, 2: 2} 
    if ans_idx == correct.get(q_idx, 0):
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/select', methods=['POST'])
def select():
    data = request.json
    item_type = data.get('type')
    value = data.get('value')
    session['choices'][item_type] = value
    session.modified = True
    return jsonify({"success": True})

@app.route('/get_final')
def get_final():
    c = session.get('choices', {})
    filename = f"{c.get('fruit')}_{c.get('choco')}_{c.get('topping')}.png"
    return jsonify({"file": filename})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
