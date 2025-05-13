from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database URI
mysql_uri = 'mysql://avnadmin:AVNS_SuiIc5LFEoPHfbK1SsG@mysql-2a8c64cb-avishkargawali07-5424.h.aivencloud.com:20013/defaultdb?ssl-mode=REQUIRED'

# Split URI into components
from urllib.parse import urlparse
url = urlparse(mysql_uri)

# Set MySQL configurations
app.config['MYSQL_HOST'] = url.hostname
app.config['MYSQL_PORT'] = url.port
app.config['MYSQL_USER'] = url.username
app.config['MYSQL_PASSWORD'] = url.password
app.config['MYSQL_DB'] = url.path[1:]  # Remove the leading '/'
app.config['MYSQL_SSL_CERT'] = '/path/to/client-cert.pem'  # Ensure SSL certificates are correct

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
    app.run(debug=True, host='0.0.0.0', port=8000)
