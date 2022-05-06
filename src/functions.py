from models import Genre, Artist, Song
from app import db


def addGenre(genre_name):
    genre = Genre.query.filter_by(type=genre_name).first()

    if genre is None:
        genre = Genre(type=genre_name)
        db.session.add(genre)
        db.session.commit()


def addArtist(artist_name):
    artist = Artist.query.filter_by(name=artist_name).first()

    if artist is None:
        artist = Artist(name=artist_name)
        db.session.add(artist)
        db.session.commit()


def addSong(title, artist, genre, song_url, img_url, duration):
    song = Song(
        title=title,
        artist=artist,
        genre=genre,
        song_url=song_url,
        img_url=img_url,
        duration=duration
    )
    db.session.add(song)
    db.session.commit()

