from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dipendra@69'
app.config['MYSQL_DB'] = 'my_database'

# File upload configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

mysql = MySQL(app)

@app.route('/')
def home():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username/password!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have successfully logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/report_pothole', methods=['GET', 'POST'])
def report_pothole():
    if 'loggedin' in session:
        if request.method == 'POST':
            aadhaar = request.form['aadhaar']
            location = request.form['location']
            severity = request.form['severity']
            image = request.files['image']
            
            # Simulate Aadhaar verification
            if len(aadhaar) != 12 or not aadhaar.isdigit():
                flash('Invalid Aadhaar number. Please enter a valid 12-digit Aadhaar number.', 'danger')
                return redirect(url_for('report_pothole'))
            
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO potholes (aadhaar, location, severity, image) VALUES (%s, %s, %s, %s)', (aadhaar, location, severity, filename))
                mysql.connection.commit()
                flash('Pothole reported successfully!', 'success')
                return redirect(url_for('report_pothole'))
        
        return render_template('report_pothole.html')
    return redirect(url_for('login'))

@app.route('/view_reports')
def view_reports():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM potholes')
        potholes = cursor.fetchall()
        return render_template('view_reports.html', potholes=potholes)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)