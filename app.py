from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector 

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost', user='Maximiliano', password='M@ximili@23', database='crud_db'
    )

# Home route
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', users=users)

# Create user
@app.route('/add', methods=['POST'])
def add_user():
    try:
        name = request.form['name']
        email = request.form['email']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        connection.commit()
        cursor.close()
        connection.close()
        flash('User added successfully!')
        return redirect(url_for('index'))
    except mysql.connector.IntegrityError as e:
        if e.errno == 1062:  # Duplicate entry error code
            return "Error: Email already exists."
        else:
            return "An unexpected error occurred."

# Update user
@app.route('/edit/<int:id>')
def edit_user(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    result = cursor.fetchone()
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    if result:
        return "Error: Email already exists."
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit.html', user=user)

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    email = request.form['email']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
    connection.commit()
    cursor.close()
    connection.close()
    flash('User updated successfully!')
    return redirect(url_for('index'))

# Delete user
@app.route('/delete/<int:id>')
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)