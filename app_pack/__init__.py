from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
#app.config['SECRET_KEY'] = '0d3034043c078b60e6d43b5b918c0227'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/absence'
db = SQLAlchemy(app)

from app_pack import routes