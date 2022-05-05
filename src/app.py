from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Song, Artist, Genre


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'keyy'

    app.run()
