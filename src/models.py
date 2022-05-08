from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(1000))

    registration_date = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    admin = db.Column(db.Boolean)

    playlists = relationship('PlaylistFollow', back_populates="user")

    __table_args__ = {'extend_existing': True}


class Song(db.Model):
    __tablename__ = 'Song'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    artist = relationship('Artist', backref=backref('parent', uselist=False))
    song_url = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    genre_id = db.Column(db.Integer, db.ForeignKey('Genre.id'))
    genre = relationship('Genre', backref=backref('parent', uselist=False))
    duration = db.Column(db.Integer)

    views = relationship('SongView', back_populates="song")

    def __init__(self, title, artist, song_url, img_url, genre, duration):
        self.title = title
        self.artist = artist
        self.artist_id = artist.id
        self.song_url = song_url
        self.img_url = img_url
        self.genre = genre
        self.genre_id = genre.id
        self.duration = duration

    def __repr__(self):
        return f"<Song(" \
               f"title={self.title}, " \
               f"genre={self.genre}, " \
               f"duration={self.duration})" \
               f"[{self.id}]>"

    __table_args__ = {'extend_existing': True}


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Artist(" \
               f"name={self.name})" \
               f"[{self.id}]>"

    __table_args__ = {'extend_existing': True}


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f"<Genre(" \
               f"type={self.type})" \
               f"[{self.id}]>"

    __table_args__ = {'extend_existing': True}


class SongView(db.Model):
    __tablename__ = 'SongView'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    user = relationship('User')
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'))
    song = relationship('Song', back_populates='views')
    count = db.Column(db.Integer, default=0)

    def __init__(self, user, song):
        self.user = user
        self.user_id = user.id
        self.song = song
        self.song_id = song.id
        self.count = 0

    def inc_count(self):
        self.count += 1


class Playlist(db.Model):
    __tablename__ = 'Playlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    user = relationship("User")
    playlist_details = relationship("PlaylistDetail", cascade="all, delete", back_populates="playlist")
    is_private = db.Column(db.Boolean)

    __table_args__ = {'extend_existing': True}

    def __init__(self, name, user, is_private):
        self.name = name
        self.user = user
        self.user_id = user.id
        self.is_private = is_private


class PlaylistDetail(db.Model):
    __tablename__ = 'PlaylistDetail'

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('Playlist.id', ondelete='CASCADE'))
    playlist = relationship("Playlist")
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'))
    song = relationship('Song')

    __table_args__ = {'extend_existing': True}

    def __init__(self, playlist, song):
        self.playlist = playlist
        self.playlist_id = playlist.id
        self.song = song
        self.song_id = song.id


class PlaylistFollow(db.Model):
    __tablename__ = 'PlaylistFollow'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='playlists')
    playlist_id = db.Column(db.Integer, db.ForeignKey('Playlist.id', ondelete='CASCADE'))
    playlist = relationship('Playlist')

    __table_args__ = {'extend_existing': True}

    def __init__(self, user, playlist):
        self.user = user
        self.user_id = user.id
        self.playlist = playlist
        self.playlist_id = playlist.id
