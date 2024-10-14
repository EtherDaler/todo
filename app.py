import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask import flash, redirect, url_for
from .routes import bp
from .db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/todo_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'wl7iUtpDAiKo8OrJBbrGArp8bbsfP5Qj')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTcyODg3OTg1MCwiaWF0IjoxNzI4ODc5ODUwfQ.GduLPSumdCt7Ws6sY81W4h4fMVt_TXeLV7I0Exe-a-k')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(bp)
app.secret_key = app.config['SECRET_KEY']

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
