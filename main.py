from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)
  
  
app.secret_key = "super key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'hydax'
  
mysql = MySQL(app)
#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/AddNewUser', methods=['GET', 'POST'])
def AddNewUser():
    if request.method == 'POST':
        value = session.get('val1',None)
        
    return render_template('AddNewUser.html',companyid=value)

@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'Name' in request.form and 'Email' in request.form and 'Password' in request.form and 'Phone' in request.form and 'box1' in request.form and 'box2' in request.form and 'box3' in request.form and 'box4' in request.form and 'box5' in request.form and 'box6' in request.form and 'image' in request.form :
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['Password']
        phone = request.form['Phone']
        rosafa = request.form['box1']
        rosai = request.form['box2']
        rosac = request.form['box3']
        rosaw = request.form['box4']
        rosae = request.form['box5']
        rosahv = request.form['box6']
        image = request.form['image']
        #cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM personnel WHERE Email = % s', (email, ))
        account1 = cursor1.fetchone()
        if account1:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not name or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute("INSERT INTO personnel(Name, Email, Password, Phone, RosaFaStatus, RosaIStatus, RosaCStatus, RosaWStatus, RosaEStatus, RosaHvStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, email, password, phone, rosafa, rosai, rosac, rosaw, rosae, rosahv,  ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    

    return render_template('register.html')
    
@app.route('/ClientAdmin', methods=['GET', 'POST'])
def ClientAdmin():
    if request.method=='POST':
        val = session.get('userid',None)
        session['val1'] = val
        #print("the companyid for user:",val)
        

    return render_template('ClientAdmin.html',companyid=val)


@app.route('/Test',methods=['GET', 'POST'])
def Test():
    # rendering webpage
    return render_template('Test.html')
    
@app.route('/rosai',methods=['GET', 'POST'])
def rosai():
    # rendering webpage
    return render_template('rosai.html')

@app.route('/open',methods=['GET', 'POST'])
def open():
    # rendering webpage
    return render_template('open.html')


     
@app.route('/teach',methods=['GET', 'POST'])
def teach():
    # rendering webpage
    
    return render_template('teach.html')

@app.route('/clientsignin', methods =['GET', 'POST'])
def clientsignin():
    mesage = ''
    if request.method == 'POST' and 'loginname' in request.form and 'password' in request.form:
        loginname = request.form['loginname']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Client WHERE loginname = %s AND password = %s', (loginname, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['loginname'] = user['loginname']
            session['password'] = user['password']
            session['recoveryemail'] = user['recoveryemail']
            mesage = 'Logged in successfully !'
            session['userid'] = user['companyid']
            
            print("fetched data:", session.get('userid'))
            return redirect(url_for('ClientAdmin'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('clientsignin.html', mesage = mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('recoveryemail', None)
    return redirect(url_for('clientsignin'))


@app.route('/clientsignup', methods =['GET', 'POST'])
def clientsignup():
    mesage = ''
    if request.method == 'POST' and 'clientname' in request.form and 'loginname' in request.form and 'password' in request.form and 'recoveryemail' in request.form and 'recoveryphone' in request.form :
        clientname = request.form['clientname']
        loginname = request.form['loginname']
        password = request.form['password']
        recoveryemail = request.form['recoveryemail']
        recoveryphone = request.form['recoveryphone']
        cursor.execute('SELECT * FROM Client WHERE recoveryemail = % s', (recoveryemail, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', recoveryemail):
            mesage = 'Invalid email address !'
        elif not loginname or not password or not recoveryemail:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute("INSERT INTO Client(clientname, loginname, password, recoveryemail, recoveryphone) VALUES (%s, %s, %s, %s, %s)", (clientname, loginname, password, recoveryemail, recoveryphone, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('clientsignup.html', mesage = mesage)

if __name__ == "__main__":
    app.run()



