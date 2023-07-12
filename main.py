from flask import *
from DataBase import FDataBase
import sqlite3
import os
from email_validator import validate_email, EmailNotValidError



# Configuration
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'Gd]DfLHGk23k52q'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))



def connect_bd():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def create_db():
    db = connect_bd()
    with app.open_resource('students.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_bd()
    return g.link_db


dbase = None


@app.before_request
def connect_before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/',  methods=["POST", "GET"])
@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == 'POST':
        conn = get_db()
        user_email = request.form["tel"]
        name = request.form['nm']
        chose = request.form['ch']
        perm = request.form['permission']
        if user_email != '' or name != "":
            try:
                emailObject = validate_email(user_email)
                testEmail = emailObject.email
                conn.execute(f"INSERT INTO user VALUES (NULL,?, ?, ?, ?)", (chose, name, testEmail, perm))
                conn.commit()
                conn.close()
                return redirect(url_for('registration'))
            except EmailNotValidError as e:
                flash(e)
                return redirect(url_for('registration',  _anchor='block_form'))
        else:
            flash("Fill in all the fields")
            return redirect(url_for('registration',  _anchor='block_form'))
    return render_template('index.html')


@app.teardown_appcontext
def close_bd(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.secret_key = 'Gd]DfLHGk23k52q'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(debug=True, host='0.0.0.0', port=303)
    create_db()

