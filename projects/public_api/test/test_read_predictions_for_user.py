import unittest
from scipy.sparse import csr_matrix
from unittest.mock import patch
from src.server import read_predictions_for_user

predictions = csr_matrix((
    [0, 1, 3, 2, 4],
    (
    (0, 0, 0, 0, 0),
    (0, 2, 3, 4, 5),
    ),
))

def find_track_by_id(id: int):
    return ['0', '1', '2', '3', '4', '5'][id]

class TestPredictions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        patch('src.server.predictions', predictions).start()
        patch('src.server.find_track_by_id', find_track_by_id).start()
        cls.addClassCleanup(patch.stopall)

    def test_read_predictions_for_user(self):
        result = read_predictions_for_user(0, 3)
        expected = ['0', '2', '4']
        self.assertListEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
