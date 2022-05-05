from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db


class Song(db.Model):
    __tablename__ = 'Song'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    artist_id = db.Column(db.Integer, ForeignKey('Artist.id'))
    artist = relationship('Artist', backref=backref('parent', uselist=False))
    song_url = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    genre_id = db.Column(db.Integer, ForeignKey('Genre.id'))
    genre = relationship('Genre', backref=backref('parent', uselist=False))
    duration = db.Column(db.Integer)

    def __repr__(self):
        return f"<Song(" \
               f"title={self.title}, " \
               f"genre={self.genre}, " \
               f"duration={self.duration})" \
               f"[{self.id}]>"


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f"<Artist(" \
               f"name={self.name})" \
               f"[{self.id}]>"


class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))

    def __repr__(self):
        return f"<Genre(" \
               f"type={self.type})" \
               f"[{self.id}]>"
