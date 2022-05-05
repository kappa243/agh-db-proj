from flask import Flask, render_template, url_for, request
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
    songs = Song.query.all()

    return render_template('index.html', songs=songs)


@app.route('/add_song', methods=['POST', 'GET'])
def add_song():
    if request.method == "POST":
        if 'add-song'in request.form:
            title = request.form['title']
            artist_n = request.form['artist']
            genre_t = request.form['genre']
            songurl = request.form['songurl']
            imgurl = request.form['imgurl']
            duration = request.form['duration']

            genre = Genre(type=genre_t)
            artist = Artist(name=artist_n)
            song = Song(
                title=title,
                artist=artist,
                song_url=songurl,
                img_url=imgurl,
                genre=genre,
                duration=duration
            )

            db.session.add(genre)
            db.session.add(artist)
            db.session.add(song)
            db.session.commit()

    return render_template('add_song.html')


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'keyy'

    app.run()
