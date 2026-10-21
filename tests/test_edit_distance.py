"""
Unit tests for edit_distance.py 
Run with:  python -m unittest test_edit_distance -v
(or:       pytest test_edit_distance.py)

"""
import random
import unittest

from edit_distance import (
    levenshtein_distance,
    levenshtein_distance_matrix,
    levenshtein_distance_optimized,
)

ALL_IMPLEMENTATIONS = [
    levenshtein_distance,
    levenshtein_distance_matrix,
    levenshtein_distance_optimized,
]


class TestKnownExamples(unittest.TestCase):
    """Examples from the work plan plus a few classics."""

    CASES = [
        ("apple", "apple", 0),
        ("aple", "apple", 1),
        ("cat", "cut", 1),
        ("book", "books", 1),
        ("abc", "xyz", 3),
        ("kitten", "sitting", 3),
        ("flaw", "lawn", 2),
        ("sunday", "saturday", 3),
        ("recieve", "receive", 2),   # transposition counts as 2 in plain Levenshtein
        ("adress", "address", 1),
        ("programing", "programming", 1),
        ("helo", "hello", 1),
    ]

    def test_examples(self):
        for fn in ALL_IMPLEMENTATIONS:
            for a, b, expected in self.CASES:
                with self.subTest(fn=fn.__name__, a=a, b=b):
                    self.assertEqual(fn(a, b), expected)


class TestOperations(unittest.TestCase):
    def test_insertion(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("aple", "apple"), 1)
            self.assertEqual(fn("a", "abc"), 2)

    def test_deletion(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("apple", "aple"), 1)
            self.assertEqual(fn("abc", "a"), 2)

    def test_substitution(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("cat", "cut"), 1)
            self.assertEqual(fn("abc", "xyz"), 3)


class TestEdgeCases(unittest.TestCase):
    def test_both_empty(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("", ""), 0)

    def test_one_empty(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("", "hello"), 5)
            self.assertEqual(fn("hello", ""), 5)

    def test_identical(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("same", "same"), 0)

    def test_single_characters(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("a", "a"), 0)
            self.assertEqual(fn("a", "b"), 1)
            self.assertEqual(fn("a", ""), 1)

    def test_long_inputs(self):
        a = "a" * 500
        b = "b" * 500
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn(a, b), 500)
            self.assertEqual(fn(a, a + "x"), 1)

    def test_very_different_lengths(self):
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("a", "a" * 50), 49)

    def test_case_sensitive(self):
        # Normalisation is the caller's responsibility.
        for fn in ALL_IMPLEMENTATIONS:
            self.assertEqual(fn("Apple", "apple"), 1)

    def test_non_string_raises(self):
        for fn in ALL_IMPLEMENTATIONS:
            with self.assertRaises(TypeError):
                fn(None, "abc")
            with self.assertRaises(TypeError):
                fn("abc", 123)


class TestProperties(unittest.TestCase):
    def test_symmetry(self):
        pairs = [("kitten", "sitting"), ("abc", "xyzw"), ("", "abc"), ("flaw", "lawn")]
        for a, b in pairs:
            self.assertEqual(levenshtein_distance(a, b), levenshtein_distance(b, a))

    def test_bounds(self):
        # |len(a)-len(b)| <= d(a,b) <= max(len(a), len(b))
        # (this is why length-based pruning in B2 is mathematically safe)
        rng = random.Random(1)
        for _ in range(200):
            a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 8)))
            d = levenshtein_distance(a, b)
            self.assertGreaterEqual(d, abs(len(a) - len(b)))
            self.assertLessEqual(d, max(len(a), len(b)))

    def test_triangle_inequality(self):
        rng = random.Random(2)
        for _ in range(200):
            a, b, c = ("".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
                       for _ in range(3))
            self.assertLessEqual(
                levenshtein_distance(a, c),
                levenshtein_distance(a, b) + levenshtein_distance(b, c),
            )

    def test_zero_iff_equal(self):
        self.assertEqual(levenshtein_distance("abc", "abc"), 0)
        self.assertGreater(levenshtein_distance("abc", "abd"), 0)

    def test_optimized_matches_matrix_randomised(self):
        rng = random.Random(3)
        for _ in range(500):
            a = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
            b = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
            self.assertEqual(
                levenshtein_distance_optimized(a, b),
                levenshtein_distance_matrix(a, b),
                msg=f"mismatch for {a!r}, {b!r}",
            )


class TestMatrixShape(unittest.TestCase):
    def test_matrix_contents(self):
        dist, dp = levenshtein_distance_matrix("ab", "abc", return_matrix=True)
        self.assertEqual(dist, 1)
        self.assertEqual(len(dp), 3)        # m + 1 rows
        self.assertEqual(len(dp[0]), 4)     # n + 1 columns
        self.assertEqual(dp[0], [0, 1, 2, 3])            # base row
        self.assertEqual([r[0] for r in dp], [0, 1, 2])  # base column
        self.assertEqual(dp[2][3], 1)


if __name__ == "__main__":
    unittest.main()
