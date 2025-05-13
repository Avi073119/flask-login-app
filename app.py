# File: app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors  # Replaced MySQLdb with PyMySQL
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL using pymysql
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL

# app.config['MYSQL_HOST'] = 'your-database-name.onrender.com'  # Or wherever your MySQL is hosted
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12778537'
app.config['MYSQL_PASSWORD'] = 'CzGMDraS4c'
app.config['MYSQL_DB'] = 'sql12778537'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            return redirect(url_for('welcome'))
        else:
            flash('Incorrect username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('signup.html')

        cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')
        else:
            cursor.execute('INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)',
                           (name, email, username, password))
            mysql.connection.commit()
            flash('You are now registered! Please login.')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        flash('Reset instructions sent to your email (placeholder).')
    return render_template('forgot_password.html')

@app.route('/welcome')
def welcome():
    if 'loggedin' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



# CREATE DATABASE flaskapp;
# USE flaskapp;
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100),
#     email VARCHAR(100),
#     username VARCHAR(50) UNIQUE,
#     password VARCHAR(100)
# );
