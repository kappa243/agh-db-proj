import csv

from models import Song, Genre, Artist


def toGenre(name):
    name = name.replace(' ', '_')
    name = name.upper()

    return name


def initData(db):
    with open('data.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        Song.query.delete()
        Genre.query.delete()
        Artist.query.delete()

        artists = dict()
        genres = dict()

        for row in reader:
            if row[14] != '':

                artist_name = row[2]
                if artists.get(artist_name) is None:
                    artist = Artist(name=artist_name)
                    artists[artist_name] = artist
                    db.session.add(artist)

                genre_name = toGenre(row[3])
                if genres.get(genre_name) is None:
                    genre = Genre(
                        type=genre_name
                    )
                    genres[genre_name] = genre
                    db.session.add(genre)

                song = Song(
                    title=row[1],
                    artist=artists.get(artist_name),
                    genre=genres.get(genre_name),
                    song_url='audio/' + row[14] + '.mp3',
                    img_url='img/' + row[14] + '.jpg',
                    duration=row[10],
                )

                db.session.add(song)
    db.session.commit()

# python ./src/manage.py shell < ./scripts/load_data.py
