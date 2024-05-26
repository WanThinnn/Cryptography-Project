import sys
import os

# Thêm thư mục 'src' vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from database.db import connect_to_db

import unittest

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        conn = connect_to_db()
        self.assertIsNotNone(conn)
        conn.close()

if __name__ == "__main__":
    unittest.main()
