"""
Unit tests for the max-priority queue implementation.
"""

import unittest

from priority_queue import MaxPriorityQueue


class TestMaxPriorityQueue(unittest.TestCase):
    """Tests for MaxPriorityQueue."""

    def test_empty_queue(self):
        pq = MaxPriorityQueue()
        self.assertTrue(pq.is_empty())
        self.assertEqual(len(pq), 0)

    def test_insert_and_maximum(self):
        pq = MaxPriorityQueue()
        pq.insert(10)
        pq.insert(4)
        pq.insert(25)
        pq.insert(7)

        self.assertEqual(pq.maximum(), 25)
        self.assertFalse(pq.is_empty())
        self.assertEqual(len(pq), 4)

    def test_extract_max(self):
        pq = MaxPriorityQueue()

        for value in [12, 3, 19, 7, 25]:
            pq.insert(value)

        extracted = [
            pq.extract_max(),
            pq.extract_max(),
            pq.extract_max(),
            pq.extract_max(),
            pq.extract_max(),
        ]

        self.assertEqual(extracted, [25, 19, 12, 7, 3])
        self.assertTrue(pq.is_empty())

    def test_increase_key(self):
        pq = MaxPriorityQueue()

        for value in [10, 8, 6, 2]:
            pq.insert(value)

        pq.increase_key(3, 15)

        self.assertEqual(pq.maximum(), 15)

    def test_extract_from_empty_queue(self):
        pq = MaxPriorityQueue()

        with self.assertRaises(IndexError):
            pq.extract_max()

    def test_maximum_from_empty_queue(self):
        pq = MaxPriorityQueue()

        with self.assertRaises(IndexError):
            pq.maximum()

    def test_invalid_insert_type(self):
        pq = MaxPriorityQueue()

        with self.assertRaises(TypeError):
            pq.insert("abc")

    def test_invalid_increase_key_type(self):
        pq = MaxPriorityQueue()
        pq.insert(10)

        with self.assertRaises(TypeError):
            pq.increase_key(0, "abc")

    def test_invalid_index_in_increase_key(self):
        pq = MaxPriorityQueue()
        pq.insert(10)

        with self.assertRaises(IndexError):
            pq.increase_key(5, 20)

    def test_decreasing_key_not_allowed(self):
        pq = MaxPriorityQueue()
        pq.insert(20)

        with self.assertRaises(ValueError):
            pq.increase_key(0, 10)

    def test_duplicate_values(self):
        pq = MaxPriorityQueue()

        for value in [9, 9, 9, 9]:
            pq.insert(value)

        extracted = [pq.extract_max() for _ in range(4)]
        self.assertEqual(extracted, [9, 9, 9, 9])

    def test_negative_values(self):
        pq = MaxPriorityQueue()

        for value in [-10, -3, -25, -1]:
            pq.insert(value)

        extracted = [pq.extract_max() for _ in range(4)]
        self.assertEqual(extracted, [-1, -3, -10, -25])


if __name__ == "__main__":
    unittest.main()