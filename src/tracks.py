from init import track_index_map, tracks

def find_track_by_id(track_index: int):
    track_id = track_index_map[track_index]
    _tracks = tracks.query(f'track_id == {track_id}')
    track = _tracks.iloc[0]
    assert track_id == track.track_id
    return {
        'track_id': track_id,
        'artist_name': track['artist_name'],
        'track_name': track['track_name'],
    }

