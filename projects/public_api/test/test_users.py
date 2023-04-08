import unittest
from unittest.mock import patch
from src.users import get_user_index


class TestUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        patch('src.users.user_id_map', {'1': 0}).start()
        cls.addClassCleanup(patch.stopall)

    def test_get_user_index(self):
        self.assertEqual(get_user_index('1'), 0)

if __name__ == '__main__':
    unittest.main()
