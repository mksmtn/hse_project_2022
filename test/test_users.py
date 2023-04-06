import unittest
from unittest.mock import patch
from src.users import get_user_index


class TestUsers(unittest.TestCase):
    @patch('init.user_id_map', return_value={'1': 0})
    def test_get_user_index(self):
        self.assertEqual(get_user_index('1'), 0)

if __name__ == '__main__':
    unittest.main()
