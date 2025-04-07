from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL,
                    stock INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT,
                    quantity INTEGER,
                    total_price REAL,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---
@app.route('/')
def dashboard():
    conn = sqlite3.connect('database.db')
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('dashboard.html', products=products)

@app.route('/add-fake-sale')
def add_fake_sale():
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO transactions (product_name, quantity, total_price, date) VALUES (?, ?, ?, ?)",
                 ('Brand A', 2, 80.0, '2025-04-07'))
    conn.commit()
    conn.close()
    return "Fake sale added!"

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect('database.db')
    product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])

        conn.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?", (name, price, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/transactions')
def transactions():
    conn = sqlite3.connect('database.db')
    sales = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return render_template('transactions.html', sales=sales)

if __name__ == '__main__':
    app.run(debug=True)
