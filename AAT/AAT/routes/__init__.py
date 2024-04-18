from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# main app for flask
app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static',
            static_url_path='/static'
            )


# database server information
DATABASE = 'database.db'


app.config['SECRET_KEY'] = 'dQw4w9WgXcQ'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'


db = SQLAlchemy(app)
login_manager = LoginManager(app)


# import from guest.py         
from routes import guest     
from routes import logged
from routes import admin
  