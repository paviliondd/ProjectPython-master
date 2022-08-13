from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 



app = Flask(__name__)

app.secret_key = '187IT20929'
 
mysql = MySQL()
   
# Connect Database
app.config['MYSQL_DATABASE_USER'] = 'WBgiOehDRJ'
app.config['MYSQL_DATABASE_PASSWORD'] = 'NQfMa49wai'
app.config['MYSQL_DATABASE_DB'] = 'WBgiOehDRJ'
app.config['MYSQL_DATABASE_HOST'] = 'remotemysql.com'
mysql.init_app(app)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
   
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    
    return render_template('index.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Xuất ra thông báo nếu có sự cố
    msg = ''
    # Kiểm tra xem các yêu cầu POST "tên người dùng", "mật khẩu" và "email" có tồn tại hay không
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
   
  #Kiểm tra account có tồn tại trong database không
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username))
        account = cursor.fetchone()
        # Nếu tài khoản tồn tại 
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Nếu tài khoản không hợp lệ
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email)) 
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Nếu để trống 
        msg = 'Please fill out the form!'
    # Hiển thị biểu mẫu đăng ký
    return render_template('register.html', msg=msg)



@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
  

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/profile')
def profile(): 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/news')
def news(): 
 
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('news.html', account=account)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)