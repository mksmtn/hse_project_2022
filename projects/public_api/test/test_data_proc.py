import unittest
from scipy.sparse import csr_matrix
from unittest.mock import patch
from src.data_processing import json_to_df
from json import dumps, loads
from pandas import DataFrame, json_normalize
from pandas.testing import assert_frame_equal

test_data = {'user_id': '0', 'track_id': '0', 'count': '1'}


def test_data_to_json(test_data: dict):
    return dumps(test_data)

def test_data_to_df(test_data: dict):
    return DataFrame([test_data])

class TestDataProcessing(unittest.TestCase):
    def test_one_json(self):
        json_test_data = test_data_to_json(test_data)
        expected = test_data_to_df(test_data)
        result = json_to_df(json_test_data)
        assert_frame_equal(result, expected)


if __name__ == '__main__':
    unittest.main()