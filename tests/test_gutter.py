

import unittest

from pyhec22.gutters import Gutter


class GutterTest(unittest.TestCase):

    def setUp(self):
        self.simple_gutter = Gutter(camber=0.02, n=0.016, slope=0.01)
        self.composite_gutter = Gutter(
            camber=0.02, n=0.016, slope=0.01, width=2.0, depth=2/12)

    def test_gutter_spread(self):
        """Example 4-1 (1) (English Units)"""
        g = self.simple_gutter
        flow = 1.8  # cfs
        produced = g.spread(flow)
        expected = 9.0  # ft
        self.assertAlmostEqual(produced, expected, 1)

    def test_gutter_flow(self):
        """Example 4-1 (2) (English Units)"""
        g = self.simple_gutter
        spread = 8.2  # ft
        produced = g.flow(spread)
        expected = 1.4  # cfs
        self.assertAlmostEqual(produced, expected, 1)

    def test_composite_gutter_depression_camber(self):
        """Example 4-2 (1) Step 1 (English Units)"""
        g = self.composite_gutter
        produced = g.depression_camber
        expected = 0.103  # cfs
        self.assertAlmostEqual(produced, expected, 3)

    def test_composite_gutter_upper_flow(self):
        """Example 4-2 (1) Step 2 (English Units)"""
        g = self.composite_gutter
        spread = 8.2  # ft
        produced = g.upper_flow(spread)
        expected = 0.67  # cfs
        self.assertAlmostEqual(produced, expected, 2)

    def test_composite_gutter_flow_ratio(self):
        """Example 4-2 (1) Step 3 (English Units)"""
        g = self.composite_gutter
        spread = 8.2  # ft
        produced = g.flow_ratio(spread)
        expected = 0.7
        self.assertAlmostEqual(produced, expected, 1)

    def test_composite_upper_flow(self):
        """Example 4-2 (2) Step 1 (English Units)"""
        g = self.composite_gutter
        flow = 4.2  # cfs
        spread = g.spread(flow)
        produced = g.upper_flow(spread)
        expected = 1.84  # cfs
        self.assertAlmostEqual(produced, expected, 2)

    def test_composite_depression_flow(self):
        """Example 4-2 (2) Step 2 (English Units)"""
        g = self.composite_gutter
        flow = 4.2  # cfs
        spread = g.spread(flow)
        produced = g.depression_flow(spread)
        expected = 2.36  # cfs
        self.assertAlmostEqual(produced, expected, 2)

    def test_composite_flow_ratio(self):
        """Example 4-2 (2) Step 3 (English Units)"""
        g = self.composite_gutter
        flow = 4.2  # cfs
        spread = g.spread(flow)
        produced = g.flow_ratio(spread)
        expected = 0.56
        self.assertAlmostEqual(produced, expected, 2)

    def test_composite_gutter_spread(self):
        """Example 4-2 (2) Step 4 (English Units)"""
        g = self.composite_gutter
        flow = 4.2  # cfs
        produced = g.spread(flow)
        expected = 11.1  # ft
        self.assertAlmostEqual(produced, expected, 1)

    def test_simple_gutter_spread_low_flow(self):
        g = self.simple_gutter
        flow = 0.01  # cfs
        produced = g.spread(flow)
        self.assertGreater(produced, 0.0)

    def test_composite_gutter_spread_low_flow(self):
        g = self.composite_gutter
        flow = 0.01  # cfs
        produced = g.spread(flow)
        self.assertGreater(produced, 0.0)

    def test_composite_gutter_spread_no_flow(self):
        g = self.composite_gutter
        flow = 0.0  # cfs
        produced = g.spread(flow)
        expected = 0.0  # ft
        self.assertEqual(produced, expected)

    def test_composite_gutter_spread_full_depression(self):
        g = self.composite_gutter
        width = g.width
        flow = g.flow(width)
        produced = g.spread(flow)
        expected = width  # ft
        self.assertAlmostEqual(produced, expected, 5)
