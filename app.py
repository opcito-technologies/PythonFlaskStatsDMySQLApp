from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

from werkzeug import generate_password_hash, check_password_hash
from random import randint
from statsd import StatsClient
import time
import os

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASS', 'fr3sca')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME', 'BucketList') 
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST', 'localhost')
mysql.init_app(app)

statsd = StatsClient(host=os.getenv('STATSD_SERVER', 'localhost'), port= os.getenv('STATSD_SERVER_PORT', 8125), prefix=None,  maxudpsize=512)

@app.route('/')
def main():
    statsd.incr('homepage')
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    # statsd counter incr for showSignUp page
    statsd.incr('showSignUp')
    sl = randint(0, 9)
    # statsd gauge for showSignUp page
    statsd.gauge('showSignUpt', sl)
    start = time.time()
    foo_timer = statsd.timer('ShowSignUpTime')
    foo_timer.start()
    time.sleep(sl)
    foo_timer.stop()
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002)
      
