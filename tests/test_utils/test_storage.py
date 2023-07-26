import unittest

from utils.storage import generate_psql_connection_string


class TestFunctions(unittest.TestCase):
    def test_generate_psql_connection_string(self):
        conn_str = generate_psql_connection_string(
            "user", "password", "localhost", 5432, "db_name")

        self.assertEqual(conn_str,
                         "postgresql://user:password@localhost:5432/db_name")
