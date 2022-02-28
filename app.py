from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)


db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'super secret key'
mysql = MySQL(app)



@app.route('/', methods = ['GET','POST'])
def index():
    menu_display = 'disabled'

    if request.method == 'POST':

        user_name = request.form.get('user_name', False)
        user_pass = request.form.get('user_pass', False)


        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM py_user")
        user = cur.fetchall()

        for user_fetched in user:

            if user_fetched["user_name"] == user_name and user_fetched["user_pass"] == user_pass:
                sign_in_value = "pass"
                session["sign_in_value"] = sign_in_value
                return menu()

            else:
                sign_in_value = "nopass"
                session["sign_in_value"] = sign_in_value


    return render_template('sign-in.html', menu_display = menu_display)



@app.route('/menu', methods = ['GET','POST'])
def menu():

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        return render_template('menu.html', sign_in_value = sign_in_value)
    else:
        return index()

@app.route('/recount', methods = ['GET','POST'])
def recount():

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        return render_template('recount.html', sign_in_value = sign_in_value)
    else:
        return index()


@app.route('/form', methods = ['GET','POST'])
def form():

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        return render_template('form.html', sign_in_value = sign_in_value)
    else:
        return index()




if __name__ == '__main__':
    app.run(debug = True)
