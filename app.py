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

table = db['mysql_table']
table_deleted = db['mysql_table_deleted']
table_sign = db['mysql_table_sign']


@app.route('/', methods = ['GET','POST'])
def index():
    menu_display = 'disabled'

    if request.method == 'POST':

        user_name = request.form.get('user_name', False)
        user_pass = request.form.get('user_pass', False)


        cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM %s", (table_sign, ))
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
    selected_view = []

    if request.method == 'POST':
        selected = request.form.getlist('form-check')
        for i in selected:
            selected_view.append(i)
        session['selected'] = selected_view
        return redirect(url_for('selected'))

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM py_db_main ORDER BY created_at")
        recount_data = cur.fetchall()

        # return render_template('db.test.html', view = recount_data)
        return render_template('recount2.html', sign_in_value = sign_in_value, recount_data = recount_data)

    else:
        return index()






@app.route('/selected', methods = ['GET','POST'])
def selected():

    selected_view_ult = []

    if request.method == 'POST':
        return redirect(url_for('deleted_msg'))

    #Check for Session
    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        selected_view = session['selected']

        #Grab the data from database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM py_db_main ORDER BY created_at")
        recount_data = cur.fetchall()

        #Select the matching data with the marked items
        for i in selected_view:
            for recount_data_single in recount_data:
                if int(i) == int(recount_data_single['id']):
                    selected_view_ult.append(recount_data_single)


        return render_template('selected2.html', sing_in_value = sign_in_value, selected_view_ult = selected_view_ult)

    else:
        return index()


@app.route('/deleted', methods=['GET','POST'])
def deleted_msg():

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        selected_view = session['selected']



        for i in selected_view:
            print (i)
            cur = mysql.connection.cursor()
            cur.execute("SELECT name,email,subject,message FROM py_db_main WHERE id = %s",  (i,))
            selected_list = cur.fetchall()

            for selected in selected_list:
                name = selected['name']
                email = selected['email']
                subject = selected['subject']
                message = selected['message']

                cur.execute("INSERT INTO py_db_deleted (name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))

            cur.execute("DELETE FROM py_db_main WHERE id = %s", (i,))
            mysql.connection.commit()

        return render_template('deleted.html')











@app.route('/form', methods = ['GET','POST'])
def form():

    statement = "Enter the required data please"
    form_condition = True

    if request.method == "POST":

        name = request.form.get('name', False)
        email = request.form.get('email', False)
        subject = request.form.get('subject', False)
        message = request.form.get('message',False)


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO py_db_main (name, email, subject, message ) VALUES (%s, %s, %s, %s)",(name, email, subject, message))
        mysql.connection.commit()
        statement = "Your Message has been recorded"
        form_condition = False

    if session['sign_in_value'] == 'pass':
        sign_in_value = 'pass'
        return render_template('form.html', sign_in_value = sign_in_value, statement = statement, form_condition = form_condition)
    else:
        return index()

@app.route('/sign_out', methods = ['GET','POST'])
def sign_out():
    menu_display = 'disabled'

    session['sign_in_value'] = ''
    return render_template('sign_out.html', menu_display = menu_display)


if __name__ == '__main__':
    app.run(debug = True)
