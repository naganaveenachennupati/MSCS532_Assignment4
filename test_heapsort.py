import random
import unittest

from heapsort import build_max_heap, heapsort


class TestHeapSort(unittest.TestCase):
    """Tests for the Heapsort implementation."""

    def test_empty_list(self):
        values = []
        self.assertEqual(heapsort(values), [])

    def test_single_element(self):
        values = [42]
        self.assertEqual(heapsort(values), [42])

    def test_two_elements(self):
        values = [9, 2]
        self.assertEqual(heapsort(values), [2, 9])

    def test_already_sorted(self):
        values = [1, 2, 3, 4, 5, 6]
        self.assertEqual(heapsort(values), [1, 2, 3, 4, 5, 6])

    def test_reverse_sorted(self):
        values = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(
            heapsort(values),
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        )

    def test_repeated_values(self):
        values = [4, 2, 4, 1, 2, 4, 3, 1]
        self.assertEqual(
            heapsort(values),
            [1, 1, 2, 2, 3, 4, 4, 4],
        )

    def test_all_equal_values(self):
        values = [7, 7, 7, 7, 7]
        self.assertEqual(heapsort(values), [7, 7, 7, 7, 7])

    def test_negative_values(self):
        values = [-5, -1, -8, -3, 0, 4, -2]
        self.assertEqual(
            heapsort(values),
            [-8, -5, -3, -2, -1, 0, 4],
        )

    def test_mixed_values(self):
        values = [19, -4, 0, 19, 7, -12, 3, 1]
        self.assertEqual(
            heapsort(values),
            [-12, -4, 0, 1, 3, 7, 19, 19],
        )

    def test_large_random_input(self):
        rng = random.Random(532)
        values = [rng.randint(-10_000, 10_000) for _ in range(1_000)]
        expected = sorted(values)

        heapsort(values)

        self.assertEqual(values, expected)

    def test_sort_is_in_place(self):
        values = [8, 3, 6, 1, 5]
        original_object = values

        result = heapsort(values)

        self.assertIs(result, original_object)
        self.assertEqual(values, [1, 3, 5, 6, 8])

    def test_build_max_heap_property(self):
        values = [3, 10, 5, 6, 2, 8, 1, 9, 4, 7]

        build_max_heap(values)

        for parent in range(len(values) // 2):
            left_child = 2 * parent + 1
            right_child = 2 * parent + 2

            if left_child < len(values):
                self.assertGreaterEqual(
                    values[parent],
                    values[left_child],
                )

            if right_child < len(values):
                self.assertGreaterEqual(
                    values[parent],
                    values[right_child],
                )


if __name__ == "__main__":
    unittest.main()