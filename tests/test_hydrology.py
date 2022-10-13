
import unittest

from pyhec22.hydrology import Basin


class HydrologyTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_basin_c_1(self):
        """Example 3-1 Step 1 (English Units)"""
        shapes = [
            (22.1, 0.25),
            (21.2, 0.22)
        ]
        basin = Basin(shapes=shapes)
        produced = basin.c
        expected = 0.235  # ft
        self.assertAlmostEqual(produced, expected, 3)

    def test_basin_c_2(self):
        """Example 3-1 Step 2 (English Units)"""
        shapes = [
            (5.4, 0.90),
            (1.6, 0.15),
            (18.6, 0.25),
            (17.7, 0.22)
        ]
        basin = Basin(shapes=shapes)
        produced = basin.c
        expected = 0.315  # ft
        self.assertAlmostEqual(produced, expected, 3)
