from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    total, count, transfers = 0.0, 0, []
    try:
        conn = sqlite3.connect('exchange_system.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        row = cursor.execute('SELECT SUM(amount) FROM transfers').fetchone()
        if row and row[0]: total = row[0]
        count = cursor.execute('SELECT COUNT(*) FROM transfers').fetchone()[0]
        transfers = cursor.execute('SELECT * FROM transfers ORDER BY id DESC LIMIT 10').fetchall()
        conn.close()
    except: pass
    return render_template('index.html', total=total, count=count, transfers=transfers)

@app.route('/add_transfer', methods=['POST'])
def add_transfer():
    sender = request.form.get('sender_name')
    amount = request.form.get('amount')
    currency = request.form.get('currency')
    if sender and amount:
        conn = sqlite3.connect('exchange_system.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transfers (sender_name, receiver_name, amount, currency) VALUES (?, ?, ?, ?)',
                       (sender, "عميل عام", float(amount), currency))
        conn.commit()
        conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
