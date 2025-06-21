
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('database.db')

@app.route('/')
def home():
    conn = connect_db()
    stock = conn.execute("SELECT * FROM blood_stock").fetchall()
    conn.close()
    return render_template('index.html', stock=stock)

@app.route('/donors')
def donors():
    conn = connect_db()
    donors = conn.execute("SELECT * FROM donors").fetchall()
    conn.close()
    return render_template('donors.html', donors=donors)

@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        last_donation = request.form['last_donation']

        conn = connect_db()
        conn.execute("INSERT INTO donors (name, age, gender, blood_group, phone, last_donation) VALUES (?, ?, ?, ?, ?, ?)",
                     (name, age, gender, blood_group, phone, last_donation))
        conn.execute("UPDATE blood_stock SET units = units + 1 WHERE blood_group = ?", (blood_group,))
        conn.commit()
        conn.close()
        return redirect('/donors')
    return render_template('donor_form.html')

@app.route('/requests')
def requests():
    conn = connect_db()
    reqs = conn.execute("SELECT * FROM requests").fetchall()
    conn.close()
    return render_template('requests.html', requests=reqs)

@app.route('/add-request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        hospital = request.form['hospital']
        blood_group = request.form['blood_group']
        units = int(request.form['units'])

        conn = connect_db()
        stock = conn.execute("SELECT units FROM blood_stock WHERE blood_group = ?", (blood_group,)).fetchone()
        status = "Fulfilled" if stock and stock[0] >= units else "Pending"

        if status == "Fulfilled":
            conn.execute("UPDATE blood_stock SET units = units - ? WHERE blood_group = ?", (units, blood_group))

        conn.execute("INSERT INTO requests (hospital_name, blood_group, units_required, request_date, status) VALUES (?, ?, ?, ?, ?)",
                     (hospital, blood_group, units, datetime.now().date(), status))
        conn.commit()
        conn.close()
        return redirect('/requests')
    return render_template('request_form.html')

if __name__ == '__main__':
    app.run(debug=True)
