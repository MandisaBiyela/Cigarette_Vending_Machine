from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

dark_ = False

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

Admin_username = "Admin"
Admin_password = "password123"
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

        flash("Product added successfully!")
        return redirect(url_for('dashboard'))
    return render_template('add_product.html')

@app.route('/purchase/<int:id>', methods=['POST'])
def purchase(id):
    quantity = int(request.form['quantity'])
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    product = c.execute("SELECT name, stock, price FROM products WHERE id=?", (id,)).fetchone()
    if not product:
        flash("Product not found.")
        return redirect(url_for('dashboard'))

    name, stock, price = product

    if stock < quantity:
        flash(f"Not enough stock for {name}. Only {stock} left.")
        return redirect(url_for('dashboard'))

    # Update stock
    new_stock = stock - quantity
    c.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, id))

    # Add transaction
    total_price = price * quantity
    c.execute("INSERT INTO transactions (product_name, quantity, total_price, date) VALUES (?, ?, ?, ?)",
              (name, quantity, total_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()

    if new_stock < 10:
        flash(f"⚠️ Low stock alert for {name}! Only {new_stock} left.")

    return redirect(url_for('dashboard'))

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

@app.route('/delete/<int:id>')
def delete_product(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/transactions')
def transactions():
    conn = sqlite3.connect('database.db')
    sales = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return render_template('transactions.html', sales=sales)

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('database.db')
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    
    cursor = conn.cursor()
    results = cursor.execute("""
        SELECT product_name, SUM(quantity) as total
        FROM transactions
        WHERE date >= ?
        GROUP BY product_name
        ORDER BY total DESC
    """, (one_week_ago,)).fetchall()
    
    most_bought = results[0] if results else None
    least_bought = results[-1] if results else None

    conn.close()
    return render_template('analytics.html', most_bought=most_bought, least_bought=least_bought)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if(username == Admin_username and password == Admin_password):
            return redirect(url_for('dashboard'))
        
        flash("Incorrct Log in information", "wrong-details")
        return render_template('login.html')
    return render_template('login.html')
    

if __name__ == '__main__':
    app.run(debug=True)
