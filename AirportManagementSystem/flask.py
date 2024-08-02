from flask import Flask
import oracledb

app = Flask(__name__)

db_user = 'system'
db_password = 'system'
db_dsn = 'localhost:1521/XE'

@app.route('/',)