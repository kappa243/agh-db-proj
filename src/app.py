from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
from player import getSongsJson
from sqlalchemy.orm import Query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Song, Artist, Genre, User
from scripts.load_data import initData

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from auth import auth

app.register_blueprint(auth, url_prefix='/')
print("sfdfs")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    songs = Song.query.order_by(Song.title).all()
    variables = getSongsJson(songs)

    return render_template('index.html', songs=songs, variables=variables)


@app.route('/add_song', methods=['POST', 'GET'])
def add_song():
    if request.method == "POST":
        if 'add-song' in request.form:
            initData(db)

    return render_template('add_song.html')


@app.route('/search', methods=['GET'])
def search():
    songs = []
    artists = []
    playlists = []

    if request.method == "GET":
        if request.args.get("query") is not None:
            query = request.args["query"]

            songs = Song.query.filter(Song.title.ilike("%" + query + "%")).order_by(Song.title).all()
            artists = Artist.query.filter(Artist.name.ilike("%" + query + "%")).order_by(Artist.name).all()

    return render_template("search.html", songs=songs, artists=artists)


@app.route('/song/<id>')
def song(id):
    song = Song.query.filter_by(id=id).first()
    variables = getSongsJson([song])

    return render_template("song.html", song=song, variables=variables)


@app.route('/artist/<id>')
def artist(id):
    songs = Song.query.filter_by(artist_id=id).order_by(Song.title).all()
    artist = Artist.query.filter_by(id=id).first()

    variables = getSongsJson(songs)

    return render_template('artist.html', songs=songs, variables=variables, artist=artist.name)


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'keyy'

    app.run()
