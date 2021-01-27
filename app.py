import pyodbc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify
import urllib.parse
from sqlalchemy import *

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=ngocnghia.database.windows.net;DATABASE=ngocnghia;UID=ngocnghia;PWD=123456789aA@")
cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=ngocnghia.database.windows.net,1433;Database=ngocnghia;Uid=ngocnghia;Pwd=123456789aA@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

app = Flask(__name__)

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

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

db.create_all()
@app.route('/home', methods=['GET', 'POST'])
def template():

    return render_template('home.html')

q = """
SELECT * FROM companys
"""
@app.route('/')
def home():
    try:
        cursor = cnxn.cursor()
        cursor.execute(q)
        row = cursor.fetchone()
        a = row.namecompany
        return render_template('home.html', content=row, mes='Kết nối đến DB thành công')
    except Exception as e:
        return render_template('home.html', content=[],err='Chưa kết nối đến DB')

# if __name__ == '__main__':
#    app.run()


