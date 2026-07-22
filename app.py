import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = 'caffeine.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_coffee_types():
    conn = get_db()
    types = [row['type'] for row in conn.execute('SELECT DISTINCT type FROM coffee ORDER BY type').fetchall()]
    conn.close()
    return types

def get_sizes():
    conn = get_db()
    sizes = [row['size'] for row in conn.execute('SELECT DISTINCT size FROM coffee ORDER BY size').fetchall()]
    conn.close()
    return sizes

def get_caffeine_for_drink(coffee_type, size):
    conn = get_db()
    row = conn.execute('SELECT caffeine_mg FROM coffee WHERE type = ? AND size = ?', (coffee_type, size)).fetchone()
    conn.close()
    return row['caffeine_mg'] if row else 0

def get_age_recommendation(age):
    conn = get_db()
    row = conn.execute('SELECT max_caffeine_mg FROM age_recommendations WHERE age_min <= ? AND age_max >= ?', (age, age)).fetchone()
    conn.close()
    return row['max_caffeine_mg'] if row else 400

def get_total_caffeine():
    conn = get_db()
    row = conn.execute('SELECT COALESCE(SUM(caffeine_mg), 0) as total FROM user_drinks').fetchone()
    conn.close()
    return row['total']

def get_user_age():
    conn = get_db()
    row = conn.execute('SELECT age FROM user_profile ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    return row['age'] if row else None

def get_drink_log():
    conn = get_db()
    rows = conn.execute('SELECT coffee_type, size, caffeine_mg, timestamp FROM user_drinks ORDER BY id DESC').fetchall()
    conn.close()
    return rows

@app.route('/')
def home():
    total_caffeine = get_total_caffeine()
    age = get_user_age()
    max_caffeine = get_age_recommendation(age) if age else 400
    percentage = round((total_caffeine / max_caffeine) * 100, 1) if max_caffeine > 0 else 0
    drink_log = get_drink_log()
    return render_template('home.html', total_caffeine=total_caffeine, max_caffeine=max_caffeine, percentage=percentage, age=age, drink_log=drink_log)

@app.route('/add_drink', methods=['GET', 'POST'])
def add_drink():
    if request.method == 'POST':
        coffee_type = request.form['coffee_type']
        size = request.form['size']
        caffeine_mg = get_caffeine_for_drink(coffee_type, size)
        conn = get_db()
        conn.execute('INSERT INTO user_drinks (coffee_type, size, caffeine_mg) VALUES (?, ?, ?)',
                     (coffee_type, size, caffeine_mg))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    types = get_coffee_types()
    sizes = get_sizes()
    return render_template('add_drink.html', types=types, sizes=sizes)

@app.route('/set_age', methods=['GET', 'POST'])
def set_age():
    if request.method == 'POST':
        age = int(request.form['age'])
        conn = get_db()
        # Clear old age and set new one
        conn.execute('DELETE FROM user_profile')
        conn.execute('INSERT INTO user_profile (age) VALUES (?)', (age,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('set_age.html')

@app.route('/reset', methods=['POST'])
def reset():
    conn = get_db()
    conn.execute('DELETE FROM user_drinks')
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)