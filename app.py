from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return redirect('/stock')

# ===================== DONORS =====================

@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        last_donation = request.form['last_donation']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO donors (name, age, gender, blood_group, phone, last_donation) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, age, gender, blood_group, phone, last_donation))
        cur.execute("UPDATE blood_stock SET units = units + 1 WHERE blood_group = ?", (blood_group,))
        conn.commit()
        conn.close()
        return redirect('/donors')
    return render_template('donor_form.html')

@app.route('/donors')
def donors():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM donors")
    donors = cur.fetchall()
    conn.close()
    return render_template('donors.html', donors=donors)

@app.route('/delete-donor/<int:donor_id>', methods=['POST'])
def delete_donor(donor_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # Get blood group before deleting
    cur.execute("SELECT blood_group FROM donors WHERE donor_id = ?", (donor_id,))
    result = cur.fetchone()
    if result:
        blood_group = result[0]
        cur.execute("DELETE FROM donors WHERE donor_id = ?", (donor_id,))
        cur.execute("UPDATE blood_stock SET units = units - 1 WHERE blood_group = ?", (blood_group,))
    conn.commit()
    conn.close()
    return redirect('/donors')

# ===================== REQUESTS =====================

@app.route('/add-request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        hospital = request.form['hospital']
        blood_group = request.form['blood_group']
        units = int(request.form['units'])
        request_date = request.form['request_date']
        status = "Pending"

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT units FROM blood_stock WHERE blood_group = ?", (blood_group,))
        available = cur.fetchone()[0]

        if available >= units:
            status = "Fulfilled"
            cur.execute("UPDATE blood_stock SET units = units - ? WHERE blood_group = ?", (units, blood_group))

        cur.execute('''INSERT INTO requests (hospital_name, blood_group, units_required, request_date, status)
                       VALUES (?, ?, ?, ?, ?)''',
                    (hospital, blood_group, units, request_date, status))
        conn.commit()
        conn.close()
        return redirect('/requests')
    return render_template('request_form.html')

@app.route('/requests')
def view_requests():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests")
    requests_data = cur.fetchall()
    conn.close()
    return render_template('requests.html', requests=requests_data)

@app.route('/delete-request/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM requests WHERE request_id = ?", (request_id,))
    conn.commit()
    conn.close()
    return redirect('/requests')

# ===================== STOCK =====================

@app.route('/stock')
def stock():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM blood_stock")
    stock_data = cur.fetchall()
    conn.close()
    return render_template('stock.html', stock=stock_data)

# ===================== RUN =====================
if __name__ == '__main__':
    app.run(debug=True)
