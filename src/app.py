import time
from itertools import chain

from flask import Flask, render_template, url_for, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
from player import getSongsJson
from sqlalchemy.orm import Query

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Song, Artist, Genre, User, Playlist, PlaylistDetail, PlaylistFollow, SongView

from scripts.load_data import initData

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from auth import auth

app.register_blueprint(auth, url_prefix='/')

from admin import admin

app.register_blueprint(admin, url_prefix='/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def utility_processor():
    user = None
    if current_user.is_authenticated:
        user = User.query.get(int(current_user.get_id()))

    def length(tab):
        sum = 0
        for t in tab:
            sum += t.count
        return sum

    return dict(user=user, length=length)


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
            playlists = Playlist.query.filter(Playlist.name.ilike("%" + query + "%")).filter_by(
                is_private=False).order_by(Playlist.name).all()

            if current_user.is_authenticated:
                user = User.query.get(int(current_user.get_id()))
                playlists = set(chain(playlists, filter(lambda pl: query in pl.name,
                                                        map(lambda pl: pl.playlist, user.playlists))))
                playlists = sorted(playlists, key=lambda pl: pl.name)
                playlists = sorted(playlists, key=lambda pl: pl.is_private)

    return render_template("search.html", songs=songs, artists=artists, playlists=playlists)


@app.route('/song/<id>', methods=['GET', 'POST'])
@login_required
def song(id):
    song = Song.query.get(int(id))
    if song is None:
        return redirect(url_for('index'))
    variables = getSongsJson([song])

    user = User.query.get(int(current_user.get_id()))

    playlists = Playlist.query.filter_by(user=user)

    if request.method == "POST":
        if "add-song" in request.form:
            playlist_id = request.form['add-song']
            playlist = db.session.query(Playlist).with_for_update().get(int(playlist_id))

            if playlist.user == user:
                song = Song.query.get(int(id))
                if not PlaylistDetail.query.filter_by(playlist=playlist, song=song).first():
                    detail = PlaylistDetail(playlist, song)

                    db.session.add(detail)
                    db.session.commit()

    return render_template("song.html", song=song, variables=variables, playlists=playlists)


@app.route('/song/view', methods=['POST'])
@login_required
def song_view():
    song = Song.query.get(int(request.values.get('song')))
    if song is None:
        return Response(status=404)

    user = User.query.get(int(current_user.get_id()))

    view = db.session.query(SongView).filter(SongView.user == user).filter(SongView.song == song).with_for_update().first()
    if view:
        view.inc_count()
        db.session.commit()
    else:
        view = SongView(user=user, song=song)
        view.inc_count()
        db.session.add(view)
        db.session.commit()

    return Response(status=200)


@app.route('/artist/<id>')
def artist(id):
    songs = Song.query.filter_by(artist_id=id).order_by(Song.title).all()
    artist = Artist.query.filter_by(id=id).first()

    variables = getSongsJson(songs)

    return render_template('artist.html', songs=songs, variables=variables, artist=artist.name)


@app.route('/playlists', methods=['GET', 'POST'])
@login_required
def playlists():
    user = User.query.get(int(current_user.get_id()))

    if request.method == 'POST':
        if 'add-playlist' in request.form:
            name = request.form['name']
            is_private = True if request.form.get('is_private') is not None and request.form[
                'is_private'] == 'on' else False

            playlist = Playlist(name, user, is_private)
            follow = PlaylistFollow(user=user, playlist=playlist)

            db.session.add(playlist)
            db.session.add(follow)
            db.session.commit()

        elif 'delete-playlist' in request.form:
            playlist_id = int(request.form['delete-playlist'])

            playlist = db.session.query(Playlist).with_for_update().get(playlist_id)

            # time.sleep(10)
            if playlist.user == user:
                db.session.delete(playlist)
                db.session.commit()
                return redirect(url_for('playlists'))

        elif 'follow-playlist' in request.form:
            playlist_id = int(request.form['follow-playlist'])
            playlist = Playlist.query.get(playlist_id)

            if playlist.user != user:
                follow = PlaylistFollow(user=user, playlist=playlist)
                db.session.add(follow)
                db.session.commit()

        elif 'unfollow-playlist' in request.form:
            playlist_id = int(request.form['unfollow-playlist'])
            playlist = Playlist.query.get(playlist_id)

            if playlist.user != user:
                follow = db.session.query(PlaylistFollow).filter_by(user=user, playlist=playlist).with_for_update().first()
                db.session.delete(follow)
                db.session.commit()

        elif 'public-playlist' in request.form:
            playlist_id = int(request.form['public-playlist'])
            playlist = db.session.query(Playlist).with_for_update().get(playlist_id)

            if playlist.user == user:
                playlist.is_private = False
                db.session.commit()

        elif 'private-playlist' in request.form:
            playlist_id = int(request.form['private-playlist'])
            playlist = db.session.query(Playlist).with_for_update().get(playlist_id)

            if playlist.user == user:
                playlist.is_private = True
                db.session.commit()

    playlists = map(lambda pl: pl.playlist, user.playlists)
    playlist_debug = Playlist.query.order_by(Playlist.is_private).order_by(Playlist.name).all()

    return render_template('playlists.html', playlists=playlists, playlist_debug=playlist_debug,
                           user_id=int(current_user.get_id()))


@app.route('/playlist/<id>', methods=['GET', 'POST'])
@login_required
def playlist(id):
    user = User.query.get(int(current_user.get_id()))

    if request.method == 'POST':
        if 'delete-playlist' in request.form:
            playlist_id = int(request.form['delete-playlist'])
            playlist = db.session.query(Playlist).with_for_update().get(playlist_id)

            if playlist.user == user:
                db.session.delete(playlist)
                db.session.commit()
                return redirect(url_for('playlists'))

        elif 'follow-playlist' in request.form:
            playlist_id = int(request.form['follow-playlist'])
            playlist = Playlist.query.get(playlist_id)

            if playlist.user != user:
                follow = PlaylistFollow(user=user, playlist=playlist)
                db.session.add(follow)
                db.session.commit()

        elif 'unfollow-playlist' in request.form:
            playlist_id = int(request.form['unfollow-playlist'])
            playlist = Playlist.query.get(playlist_id)

            if playlist.user != user:
                follow = db.session.query(PlaylistFollow).filter_by(user=user, playlist=playlist).with_for_update().first()
                db.session.delete(follow)
                db.session.commit()

        elif 'public-playlist' in request.form:
            playlist_id = int(request.form['public-playlist'])
            playlist = db.session.query(Playlist).with_for_update().get(playlist_id)

            if playlist.user == user:
                playlist.is_private = False
                db.session.commit()

        elif 'private-playlist' in request.form:
            playlist_id = int(request.form['private-playlist'])
            playlist = db.session.query(Playlist).with_for_update().get(playlist_id)

            if playlist.user == user:
                playlist.is_private = True
                db.session.commit()

    followed_ids = list(map(lambda pl: pl.playlist_id, user.playlists))

    playlist = Playlist.query.get(int(id))
    if playlist is None:
        return redirect(url_for('index'))
    if playlist.is_private and playlist.id not in followed_ids:
        playlist = None

    details = playlist.playlist_details
    songs = list(map(lambda pd: pd.song, details))
    variables = getSongsJson(songs)

    return render_template('playlist.html', playlist=playlist, songs=songs, variables=variables,
                           followed_ids=followed_ids, user_id=user.id)


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'keyy'

    app.run()
