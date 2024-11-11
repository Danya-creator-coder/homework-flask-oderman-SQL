from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    try:
        sqlite_connection = sqlite3.connect("pizza_db.db")
        cursor = sqlite_connection.cursor()
        print("Підключення успішне")


        create_table_query = '''CREATE TABLE IF NOT EXISTS pizzas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        );'''
        cursor.execute(create_table_query)

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error connecting to DB", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("З'єднання з SQL закрите")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']


        try:
            sqlite_connection = sqlite3.connect("pizza_db.db")
            cursor = sqlite_connection.cursor()
            cursor.execute('''
                INSERT INTO pizzas (name, description, price) VALUES (?, ?, ?)
            ''', (name, description, price))
            sqlite_connection.commit()
            cursor.close()
            return redirect(url_for('success'))

        except sqlite3.Error as error:
            print("Error inserting data into DB", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    return render_template('admin.html')

@app.route('/success/')
def success():
    return render_template('success.html')

@app.route('/pizzas/')
def pizzas():
    try:
        sqlite_connection = sqlite3.connect("pizza_db.db")
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM pizzas")
        pizza_list = cursor.fetchall()
        cursor.close()
        return render_template('pizzas.html', pizzas=pizza_list)

    except sqlite3.Error as error:
        print("Error fetching data from DB", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

if __name__ == '__main__':
    init_db()
    app.run(port=5002, debug=True)