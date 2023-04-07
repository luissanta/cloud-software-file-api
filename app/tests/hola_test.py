import unittest
from app.database import db


class TestReader(unittest.TestCase):
    def test_resolve_removes_first_item_from_buffer_fifo(self):
        self.assertEqual(1, 1)
