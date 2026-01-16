from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة البيانات والجداول عند تشغيل النظام
def init_db():
    conn = sqlite3.connect('exchange_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_name TEXT,
            receiver_name TEXT,
            amount REAL,
            currency TEXT,
            fee REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/transfers')
def transfers_page():
    return render_template('transfers.html')

@app.route('/add_transfer', methods=['POST'])
def add_transfer():
    sender = request.form.get('sender_name')
    receiver = request.form.get('receiver_name')
    amount = request.form.get('amount')
    currency = request.form.get('currency')
    fee = float(amount) * 0.01  # حساب العمولة 1%

    conn = sqlite3.connect('exchange_system.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transfers (sender_name, receiver_name, amount, currency, fee) VALUES (?, ?, ?, ?, ?)',
                   (sender, receiver, amount, currency, fee))
    conn.commit()
    conn.close()
    return "تم حفظ الحوالة بنجاح في قاعدة البيانات!"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)


