import json

import pyodbc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request
import urllib.parse
from sqlalchemy import *

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=ngocnghiademo.database.windows.net;DATABASE=webdemo;UID=ngocnghia;PWD=123456789aA@")
cnxn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};Server=ngocnghiademo.database.windows.net,1433;Database=webdemo;Uid=ngocnghia;Pwd=123456789aA@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class companys(db.Model):
    id = db.Column('company_id', db.Integer, primary_key=True)
    namecompany = db.Column(db.String(100))
    citycompany = db.Column(db.String(50))
    address = db.Column(db.String(200))
    email = db.Column(db.String(10))

    def __init__(self, namecompany, citycompany, address, email):
        self.namecompany = namecompany
        self.citycompany = citycompany
        self.address = address
        self.email = email


class comments(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    body = db.Column(db.String(100))
    customer = db.Column(db.String(50))
    address = db.Column(db.String(200))
    email = db.Column(db.String(10))


engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

db.create_all()

q = """
SELECT * FROM companys
"""


@app.route('/')
def home():
    try:
        cursor = cnxn.cursor()
        cursor.execute(q)
        row = cursor.fetchone()
        return render_template('index.html', content=row, mes='Kết nối đến DB thành công')
    except Exception as e:
        return render_template('index.html')


# @app.route('/home')
# def template():
#     return render_template('index-2.html', content=[], err='Chưa kết nối đến DB')


@app.route('/home',methods=['GET','POST'])
def template():
    try:
        if request.method == 'POST':
            a = request
            cursor = cnxn.cursor()
            body = request.form['comment']
            # cursor.execute("INSERT INTO comments (body, customer,address,email) VALUES ({0}, 'Jond','HaNoi','john@gmail.com')",body)
            cursor.execute("""
            INSERT INTO comments (body, customer,address,email) 
            VALUES (?,?,?,?)""",  body, 'Jond','HaNoi','john@gmail.com')
            cnxn.commit()
        return jsonify({'status':'OK','msg':'Succsess!'})
    except Exception as e:
        return jsonify({'status':'NOK','msg':'error!'})

if __name__ == '__main__':
    app.run()
