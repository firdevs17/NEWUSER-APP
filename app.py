from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5432@localhost/newuser'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Register(db.Model):
    __tablename__ = 'register'
    userroles = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    enabled = db.Column(db.Boolean)

    def __init__(self, userroles, email,enabled):
        self.userroles = userroles
        self.email = email
        self.enabled = enabled

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        userroles = request.form['userroles']

        if userroles == '' or email == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Register).filter(Register.userroles == userroles).count() == 0:
            data = Register(userroles, email)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
        return render_template('index.html', message='Please enter required fields')

if __name__ == '__main__':
    app.run()