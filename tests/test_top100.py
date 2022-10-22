import unittest
from src.top100 import get_genre, get_top_n_tracks, TrackListeningCount, count_track_listenings


class GetGenreCase(unittest.TestCase):
    def test_get_genre_killers(self):
        record = {"_id": {"artist": "The Killers", "track": "Mr. Brightside"}, "tags": {"rock": 100, "indie rock": 77, "alternative rock": 57,
                                                                                        "pop": 9, "pop rock": 6, "indie pop": 5, "britpop": 3, "new wave": 3, "punk": 2, "soundtrack": 2, "emo": 2, "dance rock": 2}, "i": 27263282}
        genre = get_genre(record)
        self.assertEqual(genre, "rock")

    def test_get_genre_mgmt(self):
        record = {"_id": {"artist": "MGMT", "track": "Kids"}, "tags": {"electro": 38, "synthpop": 14, "indietronica": 12, "pop": 11, "indie pop": 10,
                                                                       "indie rock": 9, "electronica": 8, "rock": 7, "electropop": 5, "alternative rock": 3, "new rave": 2, "psychedelic rock": 1}, "i": 22461110}
        genre = get_genre(record)
        self.assertEqual(genre, "electro")


class CountTrackListeningsCase(unittest.TestCase):
    def test_count_track_listenings(self):
        data = [
            TrackListeningCount('92915\t26719936\t1\n'),
            TrackListeningCount('92915\t4271407\t5\n'),
            TrackListeningCount('92915\t4606511\t1\n'),
            TrackListeningCount('55115\t26719936\t2\n'),
            TrackListeningCount('10101\t26719936\t1\n'),
        ]
        result = count_track_listenings(data)
        expected_result = {
            '26719936': 4,
            '4271407': 5,
            '4606511': 1
        }
        self.assertDictEqual(result, expected_result)


class GetTopNTracksCase(unittest.TestCase):
    track_listening_count_map = {
        'a': 1,
        'b': 1,
        'c': 2,
        'd': 2,
        'e': 3,
        'f': 4,
        'g': 4,
    }

    def test_1_track(self):
        result = get_top_n_tracks(
            1, GetTopNTracksCase.track_listening_count_map)
        expected_result = [('g', 4)]
        self.assertListEqual(result, expected_result)

    def test_3_tracks(self):
        result = get_top_n_tracks(
            3, GetTopNTracksCase.track_listening_count_map)
        expected_result = [
            ('g', 4),
            ('f', 4),
            ('e', 3)
        ]
        self.assertListEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
