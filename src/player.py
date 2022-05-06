import json


def getSongsJson(songs):
    songs_json = []
    for song in songs:
        minutes = str(song.duration // 60)
        seconds = song.duration % 60
        if seconds < 10:
            seconds *= 10
        seconds = str(seconds)

        ent = {
            'name':          song.title,
            'artist':        song.artist.name,
            'url':           'static/res/' + song.song_url,
            'cover_art_url': 'static/res/' + song.img_url,
            'duration':      minutes + ':' + seconds,
            'genre':         song.genre.type,
            'id':            song.id
        }

        songs_json.append(ent)

    variables = {
        'title':      'Music',
        'songs_json': json.dumps(songs_json)
    }

    return variables
